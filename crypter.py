#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Sricor
# @Date: 2021-10-20
# 易班用到的加密


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
from base64 import b64encode, b64decode


def rsa_encrypt(rsa_key, data):
    """
    rsa_key: 密钥
    登录密码加密
    """
    data = bytes(data, encoding="utf8")
    encrypt = PKCS1_v1_5.new(RSA.importKey(rsa_key))
    Sencrypt = b64encode(encrypt.encrypt(data))
    return Sencrypt.decode("utf-8")

def aes_encrypt(aes_key, aes_iv, data):
    """
    aes_key: 密钥
    aes_iv: iv
    提交表单加密
    """
    aes_key = bytes(aes_key, 'utf-8')
    aes_iv = bytes(aes_iv, 'utf-8')
    data = bytes(data, 'utf-8')
    data = aes_pkcs7padding(data)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = b64encode(cipher.encrypt(data))
    return b64encode(encrypted)

def aes_decrypt(aes_key, aes_iv, data):
    """
    aes_key: 密钥
    aes_iv: iv
    提交表单解密
    """
    aes_key = bytes(aes_key, 'utf-8')
    aes_iv = bytes(aes_iv, 'utf-8')
    data = b64decode(b64decode(data))
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    decrypted = cipher.decrypt(data)
    #decrypted = aes_pkcs7unpadding(decrypted)
    return decrypted.decode('utf-8')

def aes_pkcs7padding(data):
    bs = AES.block_size
    padding = bs - len(data) % bs
    padding_text = bytes(chr(padding) * padding, 'utf-8')
    return data + padding_text

def aes_pkcs7unpadding(data):
    lengt = len(data)
    unpadding = ord(data[lengt - 1])
    return data[0:lengt-unpadding]