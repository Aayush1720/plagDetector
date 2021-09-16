from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Custom account manager since we want to use our own user model
class MyAccountManager(BaseUserManager):
    def create_user(self, email , username, password = None):
        if not email :
            raise ValueError("email cant be empty")
        if not username :
            raise ValueError("username cant be empty")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email ,username, password):
        user = self.create_user(
                email = self.normalize_email(email),
                password = password,
                username = username,
                )
        user.is_admin    = True
        user.is_staff	= True
        user.is_superuser= True
        user.save(using =self._db)
        return user

#this actually define the custom user manager

class User(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=100, unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()
    def __str__(self):
        return self.email

    def has_perm(self, perm , obj =None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True