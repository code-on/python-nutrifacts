import random
import string
from datetime import datetime
from Crypto.Cipher import AES
from lxml import etree
import base64
import requests
import json

BS = 16
iv = "\0" * 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s),))
DecodeAES = lambda c, e: unpad(c.decrypt(base64.b64decode(e)))

api_domain = 'qa.api.nutrifacts.com'
api_url = '/getProductData.aspx'
GLN = '111111111111'
encryption_key = 'e0d!23f%3cx342e0'


def _token_generator(size=16, chars=string.letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def _data_generator(gtin, lang, token, deviceId, dateTime):
    root = etree.Element('dataPacket')

    child = etree.Element('gtin')
    child.text = gtin
    root.append(child)

    child = etree.Element('lang')
    child.text = lang
    root.append(child)

    child = etree.Element('deviceId')
    child.text = deviceId
    root.append(child)

    child = etree.Element('token')
    child.text = token
    root.append(child)

    child = etree.Element('dateTime')
    child.text = dateTime
    root.append(child)

    return etree.tostring(root, pretty_print=True)


def get_product(gtin, lang, deviceId):
    token = _token_generator()

    request_cipher = AES.new(encryption_key, mode=AES.MODE_CBC, IV=iv)
    response_cipher = AES.new(token, mode=AES.MODE_CBC, IV=iv)

    data = _data_generator(gtin=gtin, lang=lang, token=token, deviceId=deviceId, dateTime=str(datetime.utcnow()).replace(' ', 'T'))
    encoded = EncodeAES(request_cipher, data)

    params = {'gln': GLN, 'f': 'j', 'a': encoded}
    result = requests.get('http://%s%s' % (api_domain, api_url), params=params)

    response = json.loads(DecodeAES(response_cipher, result.text))
    return response
