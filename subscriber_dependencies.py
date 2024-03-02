import tensorflow as tf
import numpy as np
import cv2
import db_dependencies
import base64
import datetime

img_height = 224
img_width = 224
class_names = ['Smoke', 'Fire', 'Normal']

aiModel= tf.keras.models.load_model('model.h5', compile=False)

def runThroughModel(image):
    image_resized= cv2.resize(image, (img_height,img_width))
    image=np.expand_dims(image_resized,axis=0)
    pred=aiModel.predict(image)
    print(pred)
    return class_names[np.argmax(pred)]

def receivedCoords(dataDict: dict):
    sql = f'''
        INSERT INTO `device` (id, ref, longitude, latitude, azimuth)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE `longitude` = %s, `latitude` = %s, `azimuth` = %s
    '''
    try:
        with db_dependencies.getCursor() as cursor:
            cursor.execute(sql, (dataDict['deviceId'], dataDict['deviceRef'], dataDict['longitude'], dataDict['latitude'], dataDict['azimuth'],
                                 dataDict['longitude'], dataDict['latitude'], dataDict['azimuth']))
            db_dependencies.commit()
    finally:
        cursor.close()

def receivedFeed(dataDict: dict):
    img = base64.b64decode(dataDict['feedFrame'])
    npimg = np.frombuffer(img, dtype=np.uint8)
    frame = cv2.imdecode(npimg, 1)
    supervisionStatus = runThroughModel(frame)
    sql = f'''
        SELECT `supervision`, `regionId` FROM `device` WHERE `id` = %s
    '''
    try:
        with db_dependencies.getCursor() as cursor:
            cursor.execute(sql, (dataDict['deviceId']))
            db_dependencies.commit()
            result = cursor.fetchall()
            if not result: 
                sql = f'''
                    INSERT INTO `device` (id, ref, supervision)
                    VALUES (%s, %s, %s)
                '''
                cursor.execute(sql, (dataDict['deviceId'], dataDict['deviceRef'], supervisionStatus))
            elif result:
                if result[0]['supervision'] != supervisionStatus:
                    sql = f'''
                        UPDATE `device` 
                        SET `supervision` = %s
                        WHERE `id` = %s
                    '''
                    cursor.execute(sql, (supervisionStatus, dataDict['deviceId']))
                    db_dependencies.commit()
                    sql = f'''
                        INSERT INTO `notification` (content, regionId, createdAt)
                        VALUES (%s, %s)
                    '''
                    cursor.execute(sql, (supervisionStatus, result[0]['regionId'], datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                    db_dependencies.commit()
    
    finally:
        cursor.close()

    