import os
import argparse
import dlib
import dlib
from imutils import face_utils
from imutils.video import VideoStream
import time
from scipy.spatial import distance as dist
import playsound


#contruct the argument  parshe and parse the argument
ap=argparse.ArgumentParser()

ap.add_argument("-p","--predict_shape",required=True, help="path to facial landmark predictor")
ap.add_argument("-a","--alarm",type=str ,default="", help="path alarm .wav file")
ap.add_argument("-w","--webcam",type=int,default=0,help="index of webcam on system")


args=vars(ap.parse_args())


def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[5], mouth[8])
    B = dist.euclidean(mouth[1], mouth[11])	
    C = dist.euclidean(mouth[0], mouth[6])
    return (A + B) / (2.0 * C) 


def alarm_sound(path):
	#play alarm sound
	playsound.playsound(path)
	
def eye_aspact_ratio(eye):
	#compute the euclidean distance between the two sets
	#vertical eye landmarks(x,y)
	A=dist.euclidean(eye[1],eye[5])
	B=dist.euclidean(eye[2],eye[4])

	""" in this diagram we can see eye landmarks
		
			p2	p3
		p1			p4
			p6	p5

	 compute euclidean distance between the horizontal
	 eye landmarks (x,y)  """

	C=dist.euclidean(eye[0],eye[3])

	#compute the eye aspact ratio
	ear= (A+B) / (2.0 * C)

	#return eye aspact ratio
	return ear


"""
 define two constants, one for the eye aspect ratio to indicate
 blink and then a second constant for the number of consecutive
 frames the eye must be below the threshold for to set off the
 alarm 
"""

EYE_AR_THRESH=0.3
EYE_AR_CONSEC_FRAMES=48

"""
define two constants, one for the mouth aspect ratio to indicate
 open and then a second constant for the number of consecutive
 frames the mouth must be below the threshold

"""

MOUTH_AR_THRESH = 0.4
COUNTER_FRAMES_MOUTH = 0



#intilization the fram counter as well as a boolean used to
#indicate if the alarm is going off

COUNTER=0
ALARM_ON=False

#intilization dlib's face detection (HOG-based) and then create
#facial landmark predictor
print ("\n Real Time Doze Detection System \n")
print ("[INTO] Loading Facial Landmark Predictor......")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["predict_shape"])

#grab the indexs of facial landmarks for left and right eye ,respectively

(lStart,lEnd)=face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart,rEnd)=face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#start the video stram thread
print("[INTO] Start Video Stream")
vs=VideoStream(src=args["webcam"]).start()

time.sleep(1.0)

mar = 0
ear=0

COUNTER_MOUTH = 0





