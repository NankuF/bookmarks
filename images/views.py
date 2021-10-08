from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm


@login_required
def image_create(request):
    if request.method == 'POST':
        # Форма отправлена
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Создаем новый объект image, но пока не сохраняем в БД.
            new_item = form.save(commit=False)
            # Добавляем объект user к созданному объекту image, чтобы узнать, кто загрузил изображение
            new_item.user = request.user
            # сохраняем объект image в БД.
            new_item.save()
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})
