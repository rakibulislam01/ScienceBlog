from django.conf.urls import url
from . import views

# This is For check
urlpatterns = [
    url('create/', views.post_create, name="create"),
    url(r'^(?P<id>\d+)/$', views.post_detail, name="detail"),
    url('postlist/', views.post_list, name="list"),
    url(r'^(?P<id>\d+)/edit/$', views.post_update, name="update"),
    url(r'^(?P<id>\d+)/delete/$', views.post_delete),
    # path('jango', views.index, name='jango'),

    # ========================================= Frontend Part ================================================

    url('index/', views.index, name='index'),
    url('about/', views.about, name='about'),
    url('author/', views.author, name='author'),
    url('blank/', views.blank, name='blank'),
    url('blog_post/(?P<id>\d+)/$', views.blog_post, name='blog_post'),
    url('category/', views.category, name='category'),
    url('contact/', views.contact, name='contact'),
    url('blog_post/(?P<id>\d+)/edit/$', views.post_update, name="update"),
    url('blog_post/(?P<id>\d+)/delete/$', views.post_delete),
]
