from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    # image.user.username   и user.image.title
    # а так же image.objects.all() и user.images_created.all()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='images_created')
    # с помощью этого поля можно обращаться к связанным объектам
    # в виде image.users_like.all()
    # или из объекта пользователя user как user.images_liked.all().
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                        related_name='images_liked')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # если нет slug, то формируем его из title.
        if not self.slug:
            self.slug = slugify(self.title)
        # сохраняем объект картинки
        super(Image, self).save(*args, **kwargs)
