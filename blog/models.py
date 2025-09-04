from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True)

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
