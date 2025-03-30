from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .models import Profile,Post,Comment,Post, LikedPost,Review,Favorite,Feedback
from .forms import ProfileUpdateForm, PostForm,UserRegisterForm,CommentForm,ProfilePictureForm,ReviewForm,ChangeEmailForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.core.paginator import Paginator
from cloudinary import uploader

# Create your views here.
@login_required
def Home(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    
    # Ensure Cloudinary URLs are properly generated
    for post in page_obj:
        if hasattr(post, 'image') and post.image:
            post.image_url = post.image.url  # Explicitly get the URL
    
    if request.headers.get('HX-Request'):
        return render(request, 'partials/post_list.html', {'page_obj': page_obj})
    context = {
        'page_obj': page_obj,
        'profile': request.user.profile,  # Ensure the profile is passed

    }
    return render(request,'home.html',context)

@login_required
def ProfileView(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request,'profile.html',locals())

@login_required
def EditProfile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile = request.user.profile
        profile.fullname = request.POST.get('fullname')
        profile.occupation = request.POST.get('occupation')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.country = request.POST.get('country')
        profile.bio = request.POST.get('bio')
        profile.socials = request.POST.get('socials')
        profile.save()
        messages.success(request, "Profile as been updated")
        return redirect('profile')
    return render(request, 'editprofile.html',{'profile': profile})

@login_required
def DashboardView(request, username=None):

    
    # If no username is provided, show the logged-in user's dashboard
    if not username:
        user = request.user
        is_own_dashboard = True
        
    else:
        # Fetch the user based on the provided username
        user = get_object_or_404(User, username=username)
        is_own_dashboard = user == request.user
        reviewed_user = get_object_or_404(User, username=username)
    
    # Fetch the user's profile and posts
    profile = get_object_or_404(Profile, user=user)
    # posts = Post.objects.filter(user=user).order_by('-created_at')[:5]  # Fetch the 5 most recent posts
    posts = Post.objects.filter(author=user).order_by('-created_at')  # Fetch all posts by the author
    
    
    
        
    return render(request,'dashboard.html',locals())


@login_required
def Create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the logged-in user as the author
            post.save()
            return redirect('home')  # Redirect to the dashboard after creating the post
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create_post.html', context)

@login_required
def Delete_post(request, pk):
    # Fetch the post to be deleted
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request,'Post have been deleted ❌')
        return redirect('home')
    return render(request, 'deletepost.html',locals())

@login_required
def Edit_post(request, pk):
    # Fetch the post to be edited
    post = get_object_or_404(Post, id=pk)

    # Ensure the logged-in user is the author of the post
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('home')

    if request.method == 'POST':
        # Populate the form with the existing post data and new data
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()  # Save the updated post
            messages.success(request, 'Post updated successfully.')
            return redirect('home')
    else:
        # Display the form pre-filled with the existing post data
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'edit_post.html', context)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            # Render the new comment as a partial HTML template
            return render(request, 'partials/comment.html', {'comment': comment})
        else:
            return HttpResponse('Failed to post comment.', status=400)
    return HttpResponse('Invalid request method.', status=400)

@login_required
def delete_comment(request,comment_id):
    # Fetch the comment from the database
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Optional: Check if the user is authorized to delete the comment
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this comment.")
    return redirect('single_post', post.id)
    
    

def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exist = post.likes.filter(username=request.user.username).exists()

    if post.author != request.user:
        if user_exist:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return render(request, 'partials/like_section.html',{'post': post})

    

def Register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect to the dashboard after registration
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def Login(request):
    if request.method == 'POST':
    # Use Django's built-in AuthenticationForm
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # Redirect to the home feed after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        # Display the login form for GET requests
        form = AuthenticationForm()

    context = {
        'form': form,
    }
        
    return render(request, 'login.html',context)

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def change_profile_picture(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('profile')
    else:
        form = ProfilePictureForm(instance=profile)
    
    context = {
        'form': form,
    }
    return render(request, 'change_profile_picture.html', context)

@login_required
def Single_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all().order_by('-created_at')  # Fetch all comments for the post
    likes = post.likes.all()  # Fetch all likes for the post

    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('single_post', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'likes': likes,
        'form': form,
    }
    return render(request, 'singlepost.html', context)

def search(request):   
    if request.method =='POST':
        searched = request.POST['searched']
        datas = Profile.objects.filter(
             Q(city__icontains=searched) | Q(occupation__icontains=searched) | Q(fullname__icontains=searched) | Q(state__icontains=searched)
        )
        post_datas = Post.objects.filter(description__contains=searched)

        return render(request, 'search.html',locals())
    else:
    
        return render(request, 'search.html',)

@login_required
def review_page(request,username):
    reviewed_user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(reviewed_user=reviewed_user).order_by('-created_at')
    profile = reviewed_user.profile

    if request.method == 'POST':
        text = request.POST.get('text')  # Get text from form

        if text:  # Ensure text is provided
            Review.objects.create(
                reviewer=request.user,          # Who is writing the review
                reviewed_user=reviewed_user,    # Whose dashboard is being reviewed
                text=text                       # The actual review content
            )

        return redirect(reverse('review_page', kwargs={'username': reviewed_user.username}))

    return render(request, 'reviews.html', {'user': reviewed_user, 'reviews': reviews,'profile':profile})


@login_required
def toggle_favorite(request, username):
    favorite_user = get_object_or_404(User, username=username)
    
    if request.user == favorite_user:
        messages.error(request, "You cannot add yourself to your favorites.")
        return redirect('user_dashboard', username=username)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, favorite_user=favorite_user)
    
    if not created:
        favorite.delete()
        messages.success(request, f"Removed {favorite_user.username} from your favorites.")
    else:
        messages.success(request, f"Added {favorite_user.username} to your favorites.")
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def favorite_list(request):
    favorites = request.user.favorite_users.all()
    return render(request, 'favorite_list.html', {'favorites': favorites})

@login_required
def private_feed(request):
    favorite_users = request.user.favorite_users.values_list('favorite_user', flat=True)
    posts = Post.objects.filter(author__in=favorite_users).order_by('-created_at')
    return render(request, 'private_feed.html', {'posts': posts})


def settings(request):
    pass
    return render(request,'settings.html')


@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Your email has been updated.")
            return redirect('profile')  # Redirect to the user's profile page
    else:
        form = ChangeEmailForm(user=request.user)
    
    return render(request, 'change_email.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile')  # Redirect to the user's profile page after success

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed.")
        return super().form_valid(form)


@login_required
def write_to_us(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            # Save feedback to the database
            Feedback.objects.create(user=request.user, content=content)

            # Send email notification
            send_mail(
                subject=f"New Feedback from {request.user.username}",
                message=f"Feedback content:\n\n{content}\n\nUser email: {request.user.email}",
                from_email="noreply@errand.com",
                recipient_list=["adeshinasmart@gmail.com"],  # Replace with your admin/support email
            )
            send_mail(
                subject="Thank you for your feedback!",
                message="Hi {0},\n\nThank you for taking the time to share your thoughts with us. We value your input and will review it shortly.\n\nBest regards,\nThe MyLife Team".format(request.user.username),
                from_email="noreply@errand.com",
                recipient_list=[request.user.email],
                )

            messages.success(request, "Thank you for your feedback!")
            return redirect("thank_you")
        else:
            messages.error(request, "Feedback content cannot be empty.")
    return render(request,'write_to_us.html',locals())

def thank_you(request):
    return render(request, 'thank_you.html')

@login_required
def filter_posts(request):
    user_profile = Profile.objects.get(user=request.user)

    # Start with all posts
    posts = Post.objects.all()

    # Apply filters based on user's location or search form
    city = request.GET.get('city', user_profile.city)
    state = request.GET.get('state', user_profile.state)
    country = request.GET.get('country', user_profile.country)

    if city:
        posts = posts.filter(author__profile__city=city)
    if state:
        posts = posts.filter(author__profile__state=state)
    if country:
        posts = posts.filter(author__profile__country=country)

    context = {
        'posts': posts,
        'city': city,
        'state': state,
        'country': country,
    }
    return render(request, 'home.html', context)

# @login_required
# def get_post(request):
#     page = request.GET.get('page',1)
#     posts = Post.objects.all().order_by('-created_at')
#     paginator = Paginator(posts, 5)  # 10 posts per page

#     context = {
#         'page_obj': paginator.page(page)
#     }
#     return render(request,'home.html#post_list', context)



