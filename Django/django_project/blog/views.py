from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
# from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def blog_home(request):
    # return HttpResponse("<h1>Blog-Home</h1>")
    
    #! Pass httpresponse via render function which allows us to create templates in seperate directory
    # return render(request, 'blog/home.html')

    #! How to pass data to our templates ---
    # context = {
    #     'posts':posts
    # }
    context = {
        'posts':Post.objects.all() # accessing from the database
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    #! ListView by default will look for template according to this convention
    # Convention ==> <app>/<model>_<viewtype>.html
    # as we already have the template which is home.html, so we have to modify this variable
    template_name = 'blog/home.html'

    #! By default ListView will call object_list instead of post (in template) so we have
    #! to update this as well, because in our home.html template we are call through post object
    context_object_name = 'posts'

    #! we can order the posts according to date_posted in reverse order, i.e latest post will be at the top
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5
 
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        # return super().get_queryset()

class PostDetailView(DetailView):
    model = Post

# @LoginRequired decorator works only for funcitona based views but in class based views "LoginRequiredMixin" is used
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    #! CreateView by default will look for template according to this convention
    # Convention ==> <app>/<model>_form.html ====>> post_form.html (in our website)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# To Update post we need to check few things first--
# 1) User is logged in or not.
# 2) We can update only those posts which are created by the user which is currently logged in.
# We cannot update the posts written by the other users
#! To Satisfy 2nd condition we extends "UserPassesTestMixin" class and override the test_func()
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        # return super().test_func()

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    #! DeleteView by default will look for template according to this convention
    # Convention ==> <app>/<model>_confirm_delete.html ====>> post_confirm_delete.html (in our website)
 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def blog_about(request):
    # return HttpResponse("<h1>BLog-About</h1>")
    return render(request, 'blog/about.html',{'title': 'About Blog'})


# views.py file should always return http response or an exceptions