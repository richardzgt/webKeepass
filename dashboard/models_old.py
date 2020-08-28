from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import logging
import pyotp
import traceback
# Create your models here.

logger = logging.getLogger(__name__)

class UserManager(DjangoUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given secret_key, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          **extra_fields)
        user.set_password(password)
        return user.save(using=self._db)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email,
                                 password=password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username=username, email=email,
                                 password=password, **extra_fields)


# class User_2(AbstractBaseUser, PermissionsMixin):
#     # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#
#     username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         # help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         # validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         }
#     )
#
#     email = models.EmailField(_('email address'), blank=False, null=False,
#                               unique=True, db_index=True)
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_('Designates whether the user can log into this admin site.')
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#
#     objects = UserManager()
#
#     secret_key = models.CharField(_('secret_key'),
#                                   max_length=150,
#                                   unique=True,
#                                   editable=False,
#                                   blank=False, null=False,
#                                   default=pyotp.random_base32(64),
#                                   help_text="wfa的唯一key")
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#
#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         super().save(force_insert=force_insert,
#                      force_update=force_update,
#                      using=using, update_fields=update_fields)
#         try:
#             pass
#             # if not (self.is_staff or self.secret_key):
#             #     self.secret_key = pyotp.random_base32(64)
#             #     super().save()
#         except Exception as e:
#             logger.error(f'failed to create zabbix user or hostgroup for {self.id}: {traceback.format_exc()}')
#             raise e
#         return self
#
#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)
#
#     def get_full_name(self):
#         return str(self.username)
#
#     def get_username(self):
#         return str(self.username)
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    secret_key = models.CharField(_('secret_key'),
                              max_length=150,
                              unique=True,
                              editable=False,
                              blank=False, null=False,
                              default=pyotp.random_base32(64),
                              help_text="wfa的唯一key")
