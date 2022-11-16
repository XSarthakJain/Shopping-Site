from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self,username,password=None,**extra_fields):
        if not username:
            raise ValueError('Username is required')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,username, password=None,**extra_fields):
        user = self.create_user(username,password,**extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

