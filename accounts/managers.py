from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password):
        if not phone_number:
            raise ValueError('user must have phone number')
        if not email:
            raise ValueError('user must have email')
        if not username:
            raise ValueError('user must have username')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, phone_number, password):
        user = self.create_user(email, username, phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
        