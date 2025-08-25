from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Category Name')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

class VideoContent(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    content = models.TextField( verbose_name='Description')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Preview')
    video = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name='Video')
    views = models.ManyToManyField('Ip', related_name="content_views", blank=True, verbose_name='IP views')
    created_ad = models.DateTimeField(auto_now_add=True, verbose_name='Date of Publication')
    updated_ad = models.DateTimeField(auto_now=True, verbose_name='Last modified date')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Author')


    def __str__(self):
        return self.title

    def total_views(self):
        return self.views.count()

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def get_absolute_url(self):
        return reverse('content', kwargs={'pk': self.pk})

    def get_image(self):
        if self.image:
            try:
                return self.image.url
            except:
                return 'https://static.mtml.ru/images/video_soon.jpg'
        else:
            return 'https://static.mtml.ru/images/video_soon.jpg'


    def get_video(self):
        if self.video:
            try:
                return self.video.url
            except:
                return ''
        else:
            return ''


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='comments_as_user')
    content = models.ForeignKey(VideoContent, on_delete=models.CASCADE, verbose_name='Content', related_name='comments')
    text = models.CharField(max_length=1000, verbose_name='Comment text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Comment date')


    def __str__(self):
        return f'Comment from {self.user.username} on {self.content.title}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Name')
    name = models.CharField(max_length=150, default='User', verbose_name='Profile name')
    nick_name = models.CharField(max_length=150, default='@user', verbose_name='Nickname ')
    photo = models.ImageField(upload_to='profiles/', verbose_name='Profile picture ', null=True, blank=True)

    def __str__(self):
        return f'Profile of a user {self.user.username}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def get_profile_photo(self):
        if self.photo:
            try:
                return self.photo.url
            except:
                return 'https://cs13.pikabu.ru/avatars/3082/x3082321-1315382014.png'
        else:
            return 'https://cs13.pikabu.ru/avatars/3082/x3082321-1315382014.png'


from django.db import models

class Ip(models.Model): # наша таблица где будут айпи адреса
    ip = models.CharField(max_length=100, verbose_name='user IP')

    def __str__(self):
        return self.ip

