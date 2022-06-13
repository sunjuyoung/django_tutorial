from django.shortcuts import render, redirect
from . models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'hook_text', 'head_image', 'file_upload', 'category']

    #form valid함수 재정의 , author필드 자동으로 채우기
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog')

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        #기존에 제공했던 기능을 그대로 가져와 context에 저장
        context = super(PostList, self).get_context_data()
        #모든 카테고리를 가져와 categories라는 키에 연결해 저장
        context['categories'] = Category.objects.all()
        #카테고리가 지정되지않은 포스트의 개수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context



class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        #기존에 제공했던 기능을 그대로 가져와 context에 저장
        context = super(PostDetail, self).get_context_data()
        #모든 카테고리를 가져와 categories라는 키에 연결해 저장
        context['categories'] = Category.objects.all()
        #카테고리가 지정되지않은 포스트의 개수
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context





def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category' : category,
        }
    )



def tag_page(request, slug):

    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category' : Category.objects.all(),
            'tag':tag,
        }
    )