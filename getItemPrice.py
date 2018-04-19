
from amzsear import api
import json
from urllib.parse import urlparse
import amazon_scraper
from amazon_scraper import AmzonParser
import getItemName

def jdefault(o):
    return o.__dict__


# get Information of product from the bar code scanner-UPC contacting module
def getPrice(itemName):
    #itemName = 'Can of Sprite, 355ml'
    (products,url) = api.getSearchPage(itemName, page_num=1)
    productList = json.dumps(products, default=jdefault);
    formatted = json.loads(productList);
    mostRelatedItemUrl = formatted['0']['url']
    parsedUrlPath = urlparse(mostRelatedItemUrl).path

    if (parsedUrlPath.find("/dp/")):
        startIndex = parsedUrlPath.find("/dp/")	+ 1
        firstPart = parsedUrlPath[startIndex:]
        splittedArray = firstPart.split('/')	
        asin = splittedArray[1]

    extracted_data = []
    url = "http://www.amazon.com/dp/"+asin
    product_details = AmzonParser(url)
    price = product_details['ORIGINAL_PRICE']
    
    return price

#print(getItemPrice('Can of Sprite, 355ml'))
