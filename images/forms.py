from urllib import request

from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    """url будет заполняться с помощью js"""

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput}

    def clean_url(self):
        """
        Валидация url.
        Проверяем, что расширение в url соответствует ['jpg', 'jpeg'] иначе поднимаем исключение
        """

        # получает значение поля url, обращаясь к атрибуту формы cleaned_data
        # cleaned_data - это dict, а ['url'] - его ключ, из которого вытаскиваем значение.
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        # разделяем url по точке ('.', 'jpeg'), берем правую сторону [1]
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, commit=True, force_insert=False, force_update=False):
        # Создаем объект image, вызвав метод save(commit=False)
        image = super(ImageCreateForm, self).save(commit=False)
        # Получаем url
        image_url = self.cleaned_data['url']
        # Собираем имя url из заголовка и расширения
        image_name = '{}.{}.'.format(slugify(image.title),
                                     image_url.rsplit('.', 1)[1].lower())
        # Скачиваем изображение по указанному адресу.
        response = request.urlopen(image_url)
        # Сохраняем изображение в поле image модели Image
        # передавая в него объект скачанного файла ContentFile
        image.image.save(image_name, ContentFile(response.read()), save=False)
        # при переопределении метода важно оставить стандартное поведение,
        # поэтому сохраняем объект изображения в базу данных только в том случае,
        # если commit равен True.
        if commit:
            image.save()
        return image
