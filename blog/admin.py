from django.utils.html import format_html
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Requote, Like, Comment

from .models import Post




class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0   # no extra empty forms
    readonly_fields = ('author', 'text', 'created_at')


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    readonly_fields = ('user',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'author', 'like_count', 'comment_count','short_content', 'post_image_tag')
    inlines = [CommentInline, LikeInline]  # attach inlines here

    def like_count(self, obj):
        return obj.likes.count()


    def comment_count(self, obj):
        return obj.comments.count()


    def short_content(self, obj):
        return obj.content[:30]

    def post_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.image.url)
        return "-"

    like_count.short_description = 'Likes'
    short_content.short_description = 'Content'
    comment_count.short_description = 'Comments'
    post_image_tag.short_description = 'Image'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_at')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')



admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_image_tag')

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.profile_image.url)
        return "-"

    profile_image_tag.short_description = 'Image'

@admin.register(Requote)
class RequoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post_link', 'caption', 'created_at')

    def post_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj.post._meta.app_label, obj.post._meta.model_name),
                      args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)

    post_link.short_description = 'Original Post'



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

