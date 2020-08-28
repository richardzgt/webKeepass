#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/7/24 16:16
# @File : api.py
# @Author : richard zhu
# @purpose :
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from django.conf import settings
import base64

class ServerError(Exception):
    pass


class PyCrypt(object):
    def __init__(self, key=settings.KEY):
        self.key = self.iv = key
        self.iv = b"8155ca7d906ad5e1"  # 偏移量可选参数
        self.mode = AES.MODE_CBC

    #加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        #这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        if(count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        ##所以这里统一把加密后的字符串转化为16进制字符串 ,当然也可以转换为base64加密的内容，可以使用b2a_base64(self.ciphertext)
        _ciphertext = b2a_hex(self.ciphertext)
        # return  _ciphertext
        return str(_ciphertext, encoding='utf-8')

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        """
        decrypt pass base the same key
        对称加密之解密，同一个加密随机数
        """
        cryptor = AES.new(self.key, self.mode, self.iv)
        try:
            plain_text = cryptor.decrypt(a2b_hex(text))
        except TypeError:
            raise ServerError('Decrypt password error, TYpe error.')
        _plain_text = plain_text.rstrip(b'\0')
        return str(_plain_text, encoding='utf-8')


    @staticmethod
    def b64en(text):
        """
        base64加密
        :param text: str or bytes
        :return: str
        """
        if isinstance(text, (str)):
            return str(base64.b64encode(str.encode(text)), encoding='utf-8')
        elif isinstance(text, (bytes)):
            return str(base64.b64encode(text), encoding='utf-8')

        raise TypeError("输入类型错误")

    @staticmethod
    def b64de(text):
        """
        base64解密
        :param text: str or bytes
        :return: str
        """
        if isinstance(text, (str)):
            return str(base64.b64decode(str.encode(text)), encoding='utf-8')
        if isinstance(text, (bytes)):
            return str(base64.b64decode(text), encoding='utf-8')

if __name__ == '__main__':
    c = PyCrypt('ohyri3e21br5m6e5')
    text = c.encrypt('ggg@2018')
    print(text)
    print(c.decrypt(text))
    # x=PyCrypt.b64en('33')

    # print(PyCrypt.b64de('MzM='))
    # pass
