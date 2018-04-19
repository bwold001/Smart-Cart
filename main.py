from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import cv2
from collections import defaultdict
from imutils.video import VideoStream
import imutils
import time
import MySQLdb as mysql
import barcodeDetection
from getItemName import getName
from getItemPrice import getPrice


# Main 
if __name__ == '__main__':

#    db = mysql.connect(host="99.000webhost.io",
#                       user="root",
#                       passwd="smartcart",
#                       db="id2528699_smartcart")

#    cursor = db.cursor()

    response = input("Would you like to enter a budget?")


    if response == 'yes':
        amount = input ("How much?")
        budget = float(amount)
    elif response == 'no':
        budget = 1000000

    moneyLeft = budget

    total = 0
    virtualCart = defaultdict()

    #camera = VideoStream(usePiCamera=True).start()
    camera = cv2.VideoCapture(0)
    time.sleep(2.0)

      ### keep looping over the frames
    while True:
        # grab the current frame
        ret, frame = camera.read()
        frame = imutils.resize(frame, width=400)

        # detect the barcode in the image
        box = barcodeDetection.detect(frame)

        # if a barcode was found, draw a bounding box on the frame
        if box is not None:
            frame = cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
            decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                barcodeValue = obj.data
                barcodeValue = str(barcodeValue)
                barcode = (barcodeValue[2:-1])
                itemName = getName(barcode)
                price = getPrice(itemName)[1:]

                #Add item to virtual cart
                if itemName not in virtualCart:
                    virtualCart[str(itemName)] = float(price)
                    #print (virtualCart[str(itemName)][0])
                else:
                    print(virtualCart[str(itemName)])#.add(1)

                #sql = "INSERT INTO `user`(`item_barcode_number`, `item_name`, `item_price`, `item_quantity`) " \n
                #n      "VALUES (barcode,itemName,price,quantity)"

                #number_of_rows = cursor.execute(sql)
                #db.commit()

                print (virtualCart)
                print ("Item Added")

                total += float(price)
                moneyLeft -= float(price)
                if total >= budget:
                    overBudget = True
                    print("You're over budget")

        # show the frame and record if the user presses a key
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
 
# cleanup the camera and close any open windows
#camera.release()
cv2.destroyAllWindows()
db.close()

print(virtualCart)
print (moneyLeft)