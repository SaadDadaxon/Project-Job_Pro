from django.db import models
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.safestring import mark_safe
from rest_framework_simplejwt.tokens import RefreshToken
from main.models import Company, State, Region


def image_path(instance, filename):
    return f'account/{instance.id}/{filename}'


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError("User should have a email")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.role = 2
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        (0, "HR"),
        (1, "Candidate"),
        (2, "Admin"),
    )
    email = models.EmailField(max_length=88, unique=True, db_index=True)
    full_name = models.CharField(max_length=228)
    bio = models.TextField()
    image = models.ImageField(upload_to=image_path, null=True, blank=True)
    role = models.IntegerField(choices=ROLE, default=1)
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_staff = models.BooleanField(default=False, verbose_name="Staff user")
    is_active = models.BooleanField(default=True, verbose_name='Active user')
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.email

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:30px;"></a>')
        else:
            return '-'

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f"{settings.LOCAL_BASE_URL}{self.image.url}"
            return f"{settings.PROD_BASE_URL}{self.image.url}"
        return None

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return data


class WorkingHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='working_history')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(Region, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.account


def account_pre_save(instance, sender, *args, **kwargs):
    if instance.role == 2:
        instance.is_staff = True
    else:
        instance.is_staff = False
    return instance


pre_save.connect(account_pre_save, sender=Account)



