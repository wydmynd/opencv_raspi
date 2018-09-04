import numpy as np
import cv2
import cv2.aruco as aruco
import picamera
import picamera.array



aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
#aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)

while(True):
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.resolution = (640, 480)
            camera.capture(stream, format='bgr')
            # At this point the image is available as stream.array
            frame = stream.array
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    parameters =  aruco.DetectorParameters_create()

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
    #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners)

    found = aruco.drawDetectedMarkers(gray, corners, ids , (255,255,255))
    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('found',found)
    cv2.waitKey(10)
    
    
# When everything done, release the capture
cv2.destroyAllWindows()
