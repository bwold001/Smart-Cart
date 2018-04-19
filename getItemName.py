import requests
import json


#String barcode
def getName(barcode):
    token = '694EB7FD7813813965261DD7ED5EA00F'
    r = requests.get('https://api.upcdatabase.org/product/{}/{}'.format(barcode,token))
    info = r.json()
    status = info ['status']
    if status == 400:
        return 'Bad Request'
    elif status == 404:
        return 'Product not found'

    name = info['title']
    description = info['description']
    if name is '':
        return description
    else:
        return name

#print(getName('0049000001327'))