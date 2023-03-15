from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import NewsForm
from .filters import NewsFilter
from django.contrib.auth.mixins import PermissionRequiredMixin

class NewsList(ListView):
    model = Post
    template_name = 'allnews.html'
    context_object_name = 'allnews'
    queryset = Post.objects.order_by('-id')
    paginate_by = 5

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class NewsDetail(DetailView):
    template_name = 'post.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'post'
    queryset = Post.objects.all()

class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'newsSearch'
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class NewsAdd(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_post',)
    template_name = 'add.html'
    form_class = NewsForm
    success_url = '/news/'

class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.edit_post',)
    template_name = 'edit.html'
    form_class = NewsForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

