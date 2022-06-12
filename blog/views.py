from django.shortcuts import render
from . models import Post, Category
from django.views.generic import ListView, DetailView


# Create your views here.

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