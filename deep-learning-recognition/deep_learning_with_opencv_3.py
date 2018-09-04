# USAGE
# python deep_learning_with_opencv.py --image images/jemma.png --prototxt bvlc_googlenet.prototxt --model bvlc_googlenet.caffemodel --labels synset_words.txt

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera

import numpy as np
import argparse
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=(640, 480))

        
# load the input image from disk

prototxt = 'bvlc_googlenet.prototxt'
model= 'bvlc_googlenet.caffemodel'
labels='synset_words.txt'

# load the class labels from disk
labelfile=open('synset_words.txt')
rows = labelfile.read().strip().split("\n")
classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        image = frame.array
        
        # our CNN requires fixed spatial dimensions for our input image(s)
        # so we need to ensure it is resized to 224x224 pixels while
        # performing mean subtraction (104, 117, 123) to normalize the input;
        # after executing this command our "blob" now has the shape:
        # (1, 3, 224, 224)
        blob = cv2.dnn.blobFromImage(image, 1, (224, 224), (104, 117, 123))

        # set the blob as input to the network and perform a forward-pass to
        # obtain our output classification
        net.setInput(blob)
        start = time.time()
        preds = net.forward()
        end = time.time()
        print("[INFO] classification took {:.5} seconds".format(end - start))

        # sort the indexes of the probabilities in descending order (higher
        # probabilitiy first) and grab the top-5 predictions
        idxs = np.argsort(preds[0])[::-1][:5]

        # loop over the top-5 predictions and display them
        for (i, idx) in enumerate(idxs):
                # draw the top prediction on the input image
                if i == 0:
                        text = "Label: {}, {:.2f}%".format(classes[idx],
                                preds[0][idx] * 100)
                        cv2.putText(image, text, (5, 25),  cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2)

                # display the predicted label + associated probability to the
                # console	
                print("[INFO] {}. label: {}, probability: {:.5}".format(i + 1,
                        classes[idx], preds[0][idx]))

        # display the output image
        cv2.imshow("Image", image)
        cv2.waitKey(10)
        rawCapture.truncate(0)
