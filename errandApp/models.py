from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.templatetags.static import static
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=20,unique=True,null=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    occupation = models.CharField(max_length=30, null=True, blank=True)
    socials = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('image/smile.jpeg')
        return avatar 
    
    @property
    def name(self):
        if self.fullname:
            name = self.fullname
        else:
            name = self.user.username
        return name 
    
class Post(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the post
    description = models.TextField()  # Post description
    likes = models.ManyToManyField(User, related_name='likedposts',through='LikedPost')
    image = models.ImageField(upload_to='post_images', blank=True, null=True)  # Post image (optional)
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'

class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like by {self.user.username} on {self.post}'


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')  # User writing the review
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')  # User being reviewed
    text = models.TextField()  # Review content
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])  # Rating (1-5)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f'Review by {self.reviewer.username} for {self.reviewed_user.username}'
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_users')
    favorite_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'favorite_user')

    def __str__(self):
        return f"{self.user.username} favorites {self.favorite_user.username}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
    
