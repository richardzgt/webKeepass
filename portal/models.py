from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, send_mail
from utils.pyqrcode import QrCode
from django.conf import settings
import logging
import os
import traceback

# Create your models here.
logger = logging.getLogger(__name__)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_key = models.CharField(_('secret_key'),
                                  max_length=150,
                                  unique=True,
                                  editable=False,
                                  blank=False, null=False,
                                  default=0,
                                  help_text=_("wfa的唯一key"))
    qrcode_img_file = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return "[%s] <%s>" % (self.user.username, self.secret_key)

    def get_secret_key(self):
        return self.secret_key

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=force_insert,
                     force_update=force_update,
                     using=using, update_fields=update_fields)
        try:
            qc = QrCode()
            qc.gen_qrcode(self.user.username, 'webKeepass')
            self.secret_key = qc.secret_key
            self.qrcode_img_file = qc.img_file
            email_tmpl = os.path.join(settings.BASE_DIR, 'templates', 'portal','email_template.html')
            with open(email_tmpl, 'r') as tmpl:
                html = tmpl.read()

            ret = send_mail(
                subject='webKeepass MFA认证',
                message='',
                from_email='a30402104@126.com',
                recipient_list=[self.user.email],
                fail_silently=False,
                html_message=html.format(
                    username=self.user.username,
                    qrimage=qc.img_str,
                    site_url=settings.SITE_URL
                )
            )
            if not ret:
                logger.info(f"{self.user.username}发送mfa qrcode image失败")
            super().save()

        except Exception as e:
            logger.error(f"{self.user.username}创建失败，失败原因 {str(e)}")
            raise BaseException(f"创建失败,原因{e} {traceback.format_exc()}")

        return self

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

class SysLog(models.Model):
    """
    记录用户行为
    限制登陆
    """
    ACTION_CHOICE=(
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
    )

    ATTR_CHOICE = (
        ('Login', '登陆'),
        ('ItemGroup', '密码组'),
        ('Item', '密码条'),
        ('Fields', '字段')
    )

    user = models.CharField(max_length=150)
    ip = models.GenericIPAddressField()
    action = models.CharField(max_length=50, choices=ACTION_CHOICE, verbose_name="动作", default=1)
    attr = models.CharField(max_length=120, choices=ATTR_CHOICE, verbose_name="属性", blank=True, null=True)
    message = models.TextField(verbose_name="信息", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "<%s> [%s] [%s] from <%s>" % (self.user, self.action, self.message, self.ip)

    class Meta:
        verbose_name = "用户行为记录"
        verbose_name_plural = "用户行为记录"
        ordering = ['-created_at']

