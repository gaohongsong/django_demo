from django.conf.urls import url, patterns

urlpatterns = [
    url(r'^list/$', 'restapp.views.user_list'),
    url(r'^fetch/(?P<pk>\d+)/$', 'restapp.views.user_detail', name='user_detail'),
]
