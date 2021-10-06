Социальная сеть. Антонио Меле

###Фичи для разработчиков:
- Аутентификация??
- Авторизация (Вход и Выход из аккаунта)
- Переадресация на страницу `dashboard`
- Смена пароля
- Восстановление пароля
- Регистрация пользователей
- Расширение модели пользователя

Первое что необходимо сделать - в `INSTALLED_APPS` разместить account на самом верху,
чтобы использовать мои шаблоны. 
###Авторизация
Вход:
1. Form - По умолчанию Django использует форму `AuthenticationForm` из модуля `django.
contrib.auth.forms`
2. URL-шаблон c `LoginView`
3. HTML-шаблон `templates/registration/login.html` (стандартный путь для `LoginView`)
4. View не используем, тк `LoginView` взят из коробки и сразу размещен в URL-шаблоне

Выход:
1. URL-шаблон c `LogoutView`
2. HTML-шаблон `templates/registration/logged_out.html` (стандартный путь для `LogoutView`)
3. View не используем, тк `LogoutView` взят из коробки и сразу размещен в URL-шаблоне

###Переадресация на страницу `dashboard`
Чтобы настроить переадресацию, используют следующее:
1. В `settings.py` 
`LOGIN_REDIRECT_URL = 'dashboard'` - указывает адрес, куда Django будет перенаправлять
пользователя при успешной авторизации, если не указан GET-параметр `next`<br>
`LOGIN_URL = 'login'` - адрес, куда нужно перенаправлять пользователя для входа
в систему, например из обработчиков с декоратором `login_required`<br>
`LOGOUT_URL = 'logout'` - адрес, перейдя по которому, пользователь выйдет из своего
аккаунта.<br>
2. URL-шаблон `path('', views.dashboard, name='dashboard')`
3. HTML-шаблон `account/dashboard.html`
4. View `dashboard`
5. Decorator `@login_required`
Если юзер авторизован - покажи ему страницу `dashboard`, иначе перенаправь на страницу `login.html`

###Смена пароля
Используем вьюхи из коробки.
1. URL-шаблоны c:
- `PasswordChangeView` - обрабатывает форму смены пароля.
- `PasswordChangeDoneView` - обработчик, на который будет перенаправлен
пользователь после успешной смены пароля. Отображает сообщение о том, что операция выполнена
успешно.
2. HTML-шаблон `templates/registration/password_change_form.html`  - отображает форму для смены пароля.
3. HTML-шаблон `templates/registration/password_change_done.html`  - содержит простое сообщение,
которое говорит об успешной смене пароля.

###Восстановление пароля
Используем вьюхи из коробки, подключив smtp-сервер.
1. URL-шаблоны c:
- `PasswordResetView` - обработчик восстановления пароля. Он генерирует временную ссылку с токеном и 
отправляет ее на электронную почту пользователя.
- `PasswordResetDoneView` - отображает страницу с сообщением о том, что ссылка восстановления пароля 
была отправлена на электронную почту.
- `PasswordResetConfirmView` - позволяет пользователю указать новый пароль.
- `PasswordResetCompleteView` - отображает сообщение об успешной смене пароля.
2. HTML-шаблон `templates/registration/password_reset_form.html`  - отображает форму восстановления пароля. Эта форма
отправляет сообщение на email с ссылкой для смены пароля.
3. HTML-шаблон `templates/registration/password_reset_email.html`  - в этом шаблоне формируется 
сообщение с той самой ссылкой, отправляемое пользователю на email после `password_reset_form.html`
4. HTML-шаблон `templates/registration/password_reset_done.html`  - содержит сообщение о том, что email ушел по адресу.
5. HTML-шаблон `templates/registration/password_reset_confirm.html`  - если ссылка из `password_reset_email.html` еще
валидна, то отобразит форму восстановления пароля, иначе скажет, что ссылка уже не валидна.
6. HTML-шаблон `templates/registration/password_reset_complete.html`  - содержит сообщение об успешной смене пароля.
7. Настроить smtp-сервер, хотя бы консольный (в нашем случае достаточно 
заполнить переменную `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`),
вьюхи из коробки автоматически отправят email в консоль.

###Регистрация пользователей
1. Form `UserRegistrationForm(forms.ModelForm)` созданная по модели User.
2. HTML-шаблоны `register` и `register_done` для регистрации и подтверждения регистрации.
3. URL-шаблон для регистрации.
4. View в которой обрабатывается логика регистрации(`GET`) и подтверждения регистрации(`POST`)

###Расширение модели пользователя