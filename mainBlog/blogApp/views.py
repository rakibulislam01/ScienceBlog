from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from urllib.parse import quote_plus

from .models import Post
from .forms import PostForm
# from .utils import get_read_time

from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required


# Create your views here.
# @login_required
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        # form.cleaned_data.get("")
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully create")
        return HttpResponseRedirect(instance.post_detail_url())
    # else:
    #     messages.error(request,"Not Successfully create")
    # if request.method == "POST":
    # print(request.POST)
    # request.POST.get("content")
    # title = request.POST.get("title")
    # Post.objects.create(title = title)

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)

    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    # instance = Post.objects.get(id = 1)
    share_string = quote_plus(instance.content)
    # print(get_read_time(instance.content))
    # print("time",get_read_time(instance.get_markdown()))
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")

        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )

        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    comments = Comment.objects.filter_by_instance(instance)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # .order_by("-timestamp") # filter(draft=False).filter(publish__lte=timezone.now())

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")

    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 5)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {
        "Title": "Post List",
        "object_list": queryset,
        "page_request_var": page_request_var,
        "today": today
    }

    # if request.user.is_authenticated:
    #     context = {
    #         "Title": "List is"
    #     }
    # else:
    #     context = {
    #         "Title": "List is not"
    #     }
    return render(request, "post_list.html", context)


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        # form.cleaned_data.get("")
        instance.save()
        messages.success(request, "Successfully Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request, "Not Successfully Saved")

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }

    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully Delete")

    return redirect("index")


# ===================================== Front End Part ===============================================================#


def index(request):
    instance = Post.objects.all()
    obj = Post.objects.latest('id')
    obj1 = Post.objects.order_by('id')[:2]
    old_post = Post.objects.order_by('id')[:3:]
    # try:
    # next_i = Post.objects.filter(id__gt=id).order_by('id')[:1]
    # next_id = get_object_or_404(Post, id=next_i)
    # except:
    #     next_id = None

    # last_i = Post.objects.latest('id')
    # # last_id = get_object_or_404(Post, id=last_i)
    # recent = Post.objects.filter(id_lte=last_i.id)[:1]

    # previous_i = Post.objects.filter(id__lte=id)[1:2]  # .order_by('id')[:]
    # previous_id = get_object_or_404(Post, id=previous_i)

    recent = instance[0:4]

    # print("old_post", old_post)
    context = {
        "obj": obj,
        "obj1": obj1,
        "old_post": old_post,
        "instance": instance,
        "recent": recent
    }
    return render(request, "frontend/index.html", context)


def about(request):
    return render(request, "frontend/about.html")


def author(request):
    return render(request, "frontend/author.html")


def blank(request):
    return render(request, "frontend/blank.html")


def blog_post(request, id):
    instance = get_object_or_404(Post, id=id)
    recent = Post.objects.all()
    recent_post = recent[0:4]
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    # next = Post.objects.get(id)
    share_string = quote_plus(instance.content)

    # next_id = (Post.objects
    #               .filter( id__lt=instance.id)
    #               .exclude(id=blog_post.id)
    #               .order_by('-id')
    #               .first())

    # next_id = Post.objects.order_by('id')[b]
    # next_id = Post.get_previous_by_publish().__str__()

    # def get_pre_post_title(self):
    #     return self.get_previous_by_created_time().__str__()

    # widget = Post.objects.order_by('publish')
    try:
        next_i = Post.objects.filter(id__gt=id).order_by('id')[:1]
        next_id = get_object_or_404(Post, id=next_i)
    except:
        next_id = None

    try:
        previous_i = Post.objects.filter(id__lte=id)[1:2]  # .order_by('id')[:]
        previous_id = get_object_or_404(Post, id=previous_i)
    except:
        previous_id = None

    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "next_id": next_id,
        "previous_id": previous_id,
        "recent": recent_post
    }
    return render(request, "frontend/blog-post.html", context)


def category(request):
    return render(request, "frontend/category.html")


def contact(request):
    return render(request, "frontend/contact.html")
