from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from cbsapp import views as v

urlpatterns = patterns(
    'cbsapp.views',
    url(r'success/', v.MyView1.as_view()),
    url(r'func/', 'my_view'),
    url(r'form/', 'my_form_view'),
    url(r'protect_form/', v.ProtectedView.as_view()),
    url(r'secret/', login_required(TemplateView.as_view(template_name='secret.html'))),
    url(r'permission/', permission_required('is_superuser')(TemplateView.as_view(template_name='secret.html'))),
    url(r'publishers/', v.PublisherList.as_view()),
    url(r'books/([\w-]+)/$', v.PubBookList.as_view()),
    url(r'authors/$', v.AuthorList.as_view(), name='author-list'),
    url(r'authors/(?P<pk>[0-9]+)/$', v.AuthorDetailView.as_view(), name='author-detail'),
    url(r'authors/add/$', v.AuthorCreate.as_view(), name='author-add'),
    url(r'authors/create/$', v.AuthorJsonCreate.as_view(), name='author-create'),
    url(r'authors/update/(?P<pk>[0-9]+)/$', v.AuthUpdate.as_view(), name='author-update'),
    url(r'authors/delete/(?P<pk>[0-9]+)/$', v.AuthDelete.as_view(), name='author-delete'),
)
urlpatterns += [
    # url(r'about/cls/', v.MyView.as_view()),
    url(r'about/cls/', v.MyView.as_view(greeting='as_view')),
    # url(r'about/cls/', v.MyView.as_view(non_exist='as_view')),
    # url(r'^about/func/', 'cbsapp.views.my_view')
]
