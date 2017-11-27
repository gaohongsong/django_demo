# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views import generic

from cbsapp.forms import MyForm, AuthorForm

# 从fbv转换到cbv
from cbsapp.models import Publisher, Book, Author


def my_view(request):
    greeting = "MyView"
    if request.method == 'GET':
        return HttpResponse(greeting)


class MyView(View):
    greeting = "MyView"

    def get(self, request):
        return HttpResponse(self.greeting)
        # return HttpResponse(self.non_exist)


class MyView1(View):
    def get(self, request):
        return HttpResponse('success')


def my_form_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/cbs/about/success/')
    else:
        form = MyForm(initial={'name': 'hongsong', 'message': 'safsdfas'})
    return render(request, 'form_template.html', {'form_test': form})


class MyFormView(View):
    form_class = MyForm
    initial = {'name': 'hongsong', 'message': 'safsdfas'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})


# 类方法的装饰器
class ProtectedView(TemplateView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class LoginRequiredMixin(object):
    # 方式一，注册到路由
    # @classmethod
    # def as_view(cls, **initkwargs):
    #     view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
    #     return login_required(view)

    # 方式一，注册到分发函数
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(next=self.request.get_full_path(), login_url=settings.LOGIN_URL)
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


# 额外登录鉴权
def is_superman(user):
    return user.is_authenticated() and user.is_superuser


class SuperRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(SuperRequiredMixin, cls).as_view(**initkwargs)
        test_decorator = user_passes_test(
            is_superman,
            # login_url=settings.LOGIN_URL
        )
        return test_decorator(view)


# class PublisherList(SuperRequiredMixin, generic.ListView):
class PublisherList(LoginRequiredMixin, generic.ListView):
    model = Publisher
    context_object_name = 'publisher_list'
    queryset = Publisher.objects.filter(name__contains='Quo')

    def get_context_data(self, **kwargs):
        context = super(PublisherList, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context


class PubBookList(generic.ListView):
    template_name = 'pub_book_list.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, pk=self.args[0])
        return Book.objects.filter(publisher=self.publisher)


class AuthorList(generic.ListView):
    queryset = Author.objects.all()


class AuthorDetailView(generic.DetailView):
    form_class = AuthorForm
    queryset = Author.objects.all()

    def get_object(self, queryset=None):
        object = super(AuthorDetailView, self).get_object()
        object.last_accessed = timezone.now()
        object.save()

        return object

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())
        return context


class AuthorCreate(generic.CreateView):
    model = Author
    fields = ('salutation', 'name', 'email')

    # user model's get_absolute_url as success_url

    # cbsapp_author.last_accessed can not be NULL
    def form_valid(self, form):
        form.instance.last_accessed = timezone.now()
        return super(AuthorCreate, self).form_valid(form)


class AuthUpdate(generic.UpdateView):
    model = Author
    fields = ('salutation', 'name', 'email')
    # user model's get_absolute_url as success_url


class AuthDelete(generic.DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')


# json mixin
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        form.instance.last_accessed = timezone.now()
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class AuthorJsonCreate(AjaxableResponseMixin, generic.CreateView):
    model = Author
    fields = ['name']
