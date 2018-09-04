import numpy as np
import cv2
import cv2.aruco as aruco
import picamera
import io

#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (640, 480)

while(True):

    camera.capture(stream, format='jpeg')

    #Convert the picture into a numpy array
    buff = np.fromstring(stream.getvalue(), dtype=np.uint8)

    #Now creates an OpenCV image
    frame = cv2.imdecode(buff, 1)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    #print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners)

    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs

    found = aruco.drawDetectedMarkers(gray, corners)

    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.waitKey(20)
    
    
# When everything done, release the capture
cv2.destroyAllWindows()
