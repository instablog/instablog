from django.conf.urls import url
from blog import views
from blog import views_cbv as views_cbv

username_pattern = r'(?P<username>[a-zA-Z0-9_]+)'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<uuid>[0-9a-f]{32})/$', views.detail, name='detail'),
    # url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),

    # url(r'^new/$', views.new, name='new'),
    # url(r'^(?P<pk>\d+)/edit/$', views.edit, name='edit'),
    # url(r'^(?P<pk>\d+)/delete/$', views.delete, name='delete'),

    # url(r'^(?P<pk>\d+)/comments/new/$', views.comment_new, name='comment_new'),
    # url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),
    # url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]

urlpatterns += [
    url(r'^$', views_cbv.index, name='index'),
    url('^' + username_pattern + r'/(?P<uuid>[0-9a-f]{32})/$', views_cbv.detail, name='detail'),
    url('^' + username_pattern + r'/(?P<pk>\d+)/$', views_cbv.detail, name='detail'),

    url(r'^new/$', views_cbv.new, name='new'),
    url(r'^(?P<pk>\d+)/edit/$', views_cbv.edit, name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', views_cbv.delete, name='delete'),

    url(r'^(?P<pk>\d+)/comments/new/$', views_cbv.comment_new, name='comment_new'),
    url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/edit/$', views_cbv.comment_edit, name='comment_edit'),
    url(r'^(?P<post_pk>\d+)/comments/(?P<pk>\d+)/delete/$', views_cbv.comment_delete, name='comment_delete'),
    url(r'^author_list/$', views_cbv.author_list, name='author_list'),
    url(r'^(?P<username>[a-zA-Z0-9_]+)/$', views_cbv.author_home, name='author_home'),
]
