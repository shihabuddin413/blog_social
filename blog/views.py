from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect, get_object_or_404, redirect
from django.urls import reverse
from itertools import chain
from .models import Activity
from django.utils.timezone import now

from django.db import models

from .models import Post, Like, Requote, Comment
from .forms import PostForm, CustomUserCreationForm, CustomLoginForm, UserForm, UserProfileForm, CommentForm, \
    RequoteForm


# Create your views here.

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'blog/login.html'

def signup (request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else :
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts':posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    return render(request, 'blog/post_detail.html', {'post':post, 'comments': comments})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm (request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html',{'form':form})


@login_required
def profile(request):
    view_type  = request.GET.get('view', 'posts')
    if view_type == 'requotes':
        items =  Requote.objects.filter (user=request.user).order_by('-created_at')
    else:
        items = Post.objects.filter(author=request.user).order_by('-created_at')

    # posts = request.user.posts.all()
    return render(request, 'blog/profile.html', {
        "view_type": view_type,
        "items": items,
    })

@login_required
def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.userprofile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    # ⚡ Trailing comma absolutely remove
    return render(request, 'blog/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect ('profile')
    else :
        form = PostForm(instance=post)



@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile')


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('post_detail', pk=post.pk)


@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # unlike
    return redirect('post_detail', pk=post.pk)

@login_required
def requote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = RequoteForm(request.POST)
        if form.is_valid():
            requote = form.save(commit=False)
            requote.user = request.user
            requote.post = post
            requote.save()
            return redirect('profile')
    else:
        form = RequoteForm()
    return render(request, 'blog/requote_modal.html', {'form': form, 'post': post})

@login_required
def delete_requote(request, pk):
    requote = get_object_or_404(Requote, pk=pk, user=request.user)
    if request.method == "POST":
        requote.delete()
        return redirect(f"{reverse('profile')}?view=requotes")  # back to profile page

@login_required
def delete_activity (request, pk, activity_type=None):

    activity_type_list = {
        'requote':Requote,
        'comment':Comment,
        'like':Like,
        'post':Post
    }


    if activity_type == 'comment' or activity_type == 'post':
        activity_obj = get_object_or_404(activity_type_list[activity_type], pk=pk, author=request.user)
    else:
        activity_obj = get_object_or_404(activity_type_list[activity_type], pk=pk, user=request.user)

    if request.method == "POST":
        activity_obj.delete()
        return redirect('activity_page')

@login_required
def activity_page(request):
    user = request.user

    # Collect activities
    posts = Post.objects.filter(author=user).annotate(activity_type=models.Value('post', output_field=models.CharField()))
    requotes = Requote.objects.filter(user=user).annotate(activity_type=models.Value('requote', output_field=models.CharField()))
    comments = Comment.objects.filter(author=user).annotate(activity_type=models.Value('comment', output_field=models.CharField()))
    likes = Like.objects.filter(user=user).annotate(activity_type=models.Value('like', output_field=models.CharField()))

    # Merge & sort by created_at
    activities = sorted(
        chain(posts, requotes, comments, likes),
        key=lambda x: x.created_at,
        reverse=True
    )

    return render(request, "blog/activity.html", {"activities": activities})




