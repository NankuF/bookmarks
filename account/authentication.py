from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """Выполняет аутентификацию пользователя по email
        Идентификационные данные сначала будут проверены ModelBackend ( см. в settings.py).
        Если этот бэкэнд не вернет объект пользователя, Django попробует аутентифи-
        цировать его с помощью нашего класса, EmailAuthBackend"""

    def authenticate(self, request, username=None, password=None):
        try:
            # Если в форме в поле username вы ввели email, то сработает этот бэкенд
            # например вы ввели username=val@val.com, User.objects.get(email=val@val.com)
            # важно, чтобы на фронте в поле <input... name='username' - было написано username.
            # Если там написано не username, то ф-я не сработает.
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
