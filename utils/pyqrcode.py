#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/7/24 9:38
# @File : test.py
# @Author : richard zhu
# @purpose :

from qrcode import QRCode, constants
from django.conf import settings
import os
import traceback
import pyotp
import io
import base64

STATIC_PATH = os.path.join(settings.BASE_DIR, 'static', 'image', 'mfa')

class QrCode(object):
    def __init__(self):
        self.dirpath = STATIC_PATH
        self.secret_key = pyotp.random_base32(64)  # 获取随机密钥，存于用户表中,随机64位

    def gen_qrcode(self, username, issuer_name="IAM MFA Code"):
        data = pyotp.totp.TOTP(self.secret_key).provisioning_uri(username, issuer_name)
        qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=6,
            border=4, )
        try:
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image()
            self.img_file = self.dirpath + os.sep + self.secret_key + '.png'
            img.save(self.img_file)  # 保存条形码图片

            buf = io.BytesIO()
            img.save(buf, format='PNG') # 保存成字符串
            image_stream = buf.getvalue()
            heximage = base64.b64encode(image_stream)
            self.img_str = 'data:image/png;base64,' + heximage.decode()
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    @staticmethod
    def verify(secret_key, verifycode):
        res = pyotp.TOTP(secret_key)
        result = res.verify(verifycode, valid_window=1)  # 对输入验证码进行校验，正确返回True
        return result if result is True else False


if __name__ == '__main__':
    qc=QrCode()
    qid = qc.gen_qrcode('amy', 'gaotao')
    print(qc.secret_key,qc.img_str,qc.img_file)
    QrCode.verify(qc.secret_key,qid)
    # validate
    # res = Google_Verify_Result('KG73JWI4EZMZ7XOBL7E4BDNMGHZUZD34E5OV6W3U2SSE4U5C6GJQQQXI2TMETUZG', 242267)
    # print(res)


