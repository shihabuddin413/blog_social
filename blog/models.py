
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # New field

    def total_likes (self):
        if self.likes.count():
            return self.likes.count()
        else :
            return 0

    def total_comments(self):
        if self.comments.count():
            return self.comments.count()
        else:
            return 0


    def liked_by_user(self, user):
        return self.likes.filter(user=user).exists()


    def __str__(self):
        return self.title


class Like (models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # ADD THIS

    class Meta:
        unique_together = ('post', 'user')  # prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class UserProfile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png')

    def __str__(self):
        return f"{self.user.username}'s profile"

class Requote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requotes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="requotes")
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requoted {self.post.title}"




class Activity(models.Model):
    ACTION_CHOICES = [
        ('post', 'Posted'),
        ('comment', 'Commented'),
        ('like', 'Liked'),
        ('requote', 'Requoted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content = models.TextField(blank=True, null=True)  # Optional description
    related_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} {self.get_action_display()} at {self.created_at}"
