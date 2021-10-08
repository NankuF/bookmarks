Социальная сеть. Антонио Меле

### Фичи для разработчиков:

- Аутентификация??
- env
- Авторизация (Вход и Выход из аккаунта)
- Переадресация на страницу `dashboard`
- Смена пароля
- Восстановление пароля
- Регистрация пользователей
- Расширение модели пользователя (добавим Profile к User)
- Подключение системы уведомлений (messages)
- Реализация бэкэнда аутентификации (вход по email)
- Аутентификация через сторонние приложения (соц.сети)
- Сохранение изображения с других сайтов в закладки
- Самоподписанный сертификат django_extensions (`python manage.py runserver_plus --cert-file cert.crt`)

Первое что необходимо сделать - в `INSTALLED_APPS` разместить account на самом верху, чтобы использовать мои шаблоны.

### Авторизация

Вход:

1. Form - По умолчанию Django использует форму `AuthenticationForm` из модуля `django. contrib.auth.forms`
2. URL-шаблон c `LoginView`
3. HTML-шаблон `templates/registration/login.html` (стандартный путь для `LoginView`)
4. View не используем, тк `LoginView` взят из коробки и сразу размещен в URL-шаблоне

Выход:

1. URL-шаблон c `LogoutView`
2. HTML-шаблон `templates/registration/logged_out.html` (стандартный путь для `LogoutView`)
3. View не используем, тк `LogoutView` взят из коробки и сразу размещен в URL-шаблоне

### Переадресация на страницу `dashboard`

Чтобы настроить переадресацию, используют следующее:

1. В `settings.py`
   `LOGIN_REDIRECT_URL = 'dashboard'` - указывает адрес, куда Django будет перенаправлять пользователя при успешной
   авторизации, если не указан GET-параметр `next`<br>
   `LOGIN_URL = 'login'` - адрес, куда нужно перенаправлять пользователя для входа в систему, например из обработчиков с
   декоратором `login_required`<br>
   `LOGOUT_URL = 'logout'` - адрес, перейдя по которому, пользователь выйдет из своего аккаунта.<br>
2. URL-шаблон `path('', views.dashboard, name='dashboard')`
3. HTML-шаблон `account/dashboard.html`
4. View `dashboard`
5. Decorator `@login_required`
   Если юзер авторизован - покажи ему страницу `dashboard`, иначе перенаправь на страницу `login.html`

### Смена пароля

Используем вьюхи из коробки.

1. URL-шаблоны c:

- `PasswordChangeView` - обрабатывает форму смены пароля.
- `PasswordChangeDoneView` - обработчик, на который будет перенаправлен пользователь после успешной смены пароля.
  Отображает сообщение о том, что операция выполнена успешно.

2. HTML-шаблон `templates/registration/password_change_form.html`  - отображает форму для смены пароля.
3. HTML-шаблон `templates/registration/password_change_done.html`  - содержит простое сообщение, которое говорит об
   успешной смене пароля.

### Восстановление пароля

Используем вьюхи из коробки, подключив smtp-сервер.

1. URL-шаблоны c:

- `PasswordResetView` - обработчик восстановления пароля. Он генерирует временную ссылку с токеном и отправляет ее на
  электронную почту пользователя.
- `PasswordResetDoneView` - отображает страницу с сообщением о том, что ссылка восстановления пароля была отправлена на
  электронную почту.
- `PasswordResetConfirmView` - позволяет пользователю указать новый пароль.
- `PasswordResetCompleteView` - отображает сообщение об успешной смене пароля.

2. HTML-шаблон `templates/registration/password_reset_form.html`  - отображает форму восстановления пароля. Эта форма
   отправляет сообщение на email с ссылкой для смены пароля.
3. HTML-шаблон `templates/registration/password_reset_email.html`  - в этом шаблоне формируется сообщение с той самой
   ссылкой, отправляемое пользователю на email после `password_reset_form.html`
4. HTML-шаблон `templates/registration/password_reset_done.html`  - содержит сообщение о том, что email ушел по адресу.
5. HTML-шаблон `templates/registration/password_reset_confirm.html`  - если ссылка из `password_reset_email.html` еще
   валидна, то отобразит форму восстановления пароля, иначе скажет, что ссылка уже не валидна.
6. HTML-шаблон `templates/registration/password_reset_complete.html`  - содержит сообщение об успешной смене пароля.
7. Настроить smtp-сервер, хотя бы консольный (в нашем случае достаточно заполнить
   переменную `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`), вьюхи из коробки автоматически
   отправят email в консоль.

### Регистрация пользователей

1. Form `UserRegistrationForm(forms.ModelForm)` созданная по модели User.
2. HTML-шаблоны `register` и `register_done` для регистрации и подтверждения регистрации.
3. URL-шаблон для регистрации.
4. View в которой обрабатывается логика регистрации(`GET`) и подтверждения регистрации(`POST`)

### Расширение модели пользователя (добавим Profile к User)
Когда пользователь регистрируется на сайте, мы создаем пустой профиль,
ассоциированный с ним.<br>
Для ранее зарегистрированных пользователей профиль создастся при переходе по ссылке в профиль в
view `edit`
1. Cоздаем модель `Profile` со связью 1к1 c `User`
2. Сделать миграции
3. Добавить модель в админку
4. `pip install pillow` - для поля типа `ImageField`, чтобы сохранять фотки.
5. Для встроенной модели `User` нам не нужно добавлять в `settings.AUTH_USER_MODEL`, эта модель по 
умолчанию в ней прописана, даже если `AUTH_USER_MODEL` нет в `settings.py` , однако если модель
кастомная, то необходимо это сделать `AUTH_USER_MODEL=myapp.MyUser`
6. `settings.py` -> `MEDIA_URL = '/media/'`,`MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')`
7. В URL-шаблоне `bookmarks/urls.py` добавить `if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)` тк мы сохраняем фото
8. Создать формы `UserEditForm` и `ProfileEditForm`
9. Сделать view `edit` для их отображения.
10. Добавить в view `register` код для создания профиля пользователя  `Profile.objects.create(user=new_user)`
в модели`Profile`
11. HTML-шаблон `edit.html`


###Подключение системы уведомлений (messages)
1. В HTML-шаблон `base.html` добавить код для `messages` (т.к система сообщений настраивается сразу для
всего проекта)
2. Добавить в нужный view код типа `messages.success(request, 'Profile updated successfully')`
3. Система сообщений автоматически подключает контекстный процессор
`django.contrib.messages.context_processors.messages`, который добавляет переменную message в контекст

### Реализация бэкэнда аутентификации (вход по email)

Принцип простой: если пользователь в поле username вводит свой email, то бэкенды срабатывают по очереди
и `EmailAuthBackend` запускает в систему пользователя.<br>
Создать свой бэкэнд – это значит создать Python-класс, который реализует 2 метода - `authenticate` и `get_user`<br>
Добавим бэкэнд, который даст возможность пользователям использовать
e-mail вместо логина для входа на сайт

Создаем класс `EmailAuthBackend(object)` в котором определяем эти 2 метода:
- `authenticate` - принимает в качестве параметров объект запроса request и идентификационные данные пользователя. Он
должен возвращать объект пользователя, если данные корректны; в противном случае – None.
- `get_user` - принимает ID и должен вернуть соответствующий объект пользователя.<br>

Не забываем добавить `AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',
'account.authentication.EmailAuthBackend',
]`

### Аутентификация через сторонние приложения

Для Facebook нужен https в графе `Действительные URI перенаправления для OAuth`
(https://developers.facebook.com/apps/233990812091626/fb-login/settings/)
Для Google не подтянулся редирект на mysite.com, пришлось добавить 127.0.0.1 в строку редиректа в Google.

Как подключить аутентификацию через соц.сеть?

1. `pip install social-auth-app-django`
2. `INSTALLED_APPS` -> `'social_django'`
3. `python manage.py migrate`
4. `path('social-auth/', include('social_django.urls', namespace='social'))`
5. Добавить в `/etc/hosts` -> `127.0.0.1 mysite.com`
6. `ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']`
7. В `AUTHENTICATION_BACKENDS` добавить `'social_core.backends.facebook.FacebookOAuth2'`
8. В личном кабинете разработчика создать приложение c OAuth для Web. Получить ID и Secret
9. В `settings.py` `SOCIAL_AUTH_FACEBOOK_KEY = 'XXX' # Facebook App ID, SOCIAL_AUTH_FACEBOOK_SECRET = 'XXX' # Facebook App Secret`
10. Добавить в HTML-шаблон `base.html` код для кнопки соц.сети.


