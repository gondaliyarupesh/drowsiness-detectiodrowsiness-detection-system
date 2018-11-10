from threading import Thread
from parameters import *
import numpy as np
import cv2
import imutils

while True:

	#grab the frame from the threadd video file stram ,resize 
	#it and convert it to grascale channels
	frame=vs.read()
	frame=imutils.resize(frame,width=680)
	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


	#Detect face in grayscals frame
	rects=detector(gray,0)

	#loop over face detecions
	for rect in rects:

		"""
			determine the facial landmarks for the face region ,then
			convert the facial landmarks(x,y)-coordinates numpy array
		"""	
		shape=predictor(gray,rect)
		shape=face_utils.shape_to_np(shape)

		

		'''
			extract the left and right eye coordinates,then use the
			coordinates to compute the eye aspect ration for both eye

		'''
		leftEye=shape[lStart:lEnd]
		rightEye=shape[rStart:rEnd]

		jaw = shape[48:61]

		
		leftEAR=eye_aspact_ratio(leftEye)
		rightEAR=eye_aspact_ratio(rightEye)

		#average the eye aspect ratio together for the both eye
		ear= (leftEAR + rightEAR) / 2.0
		mar = mouth_aspect_ratio(jaw)
		"""
			compure the convex hull for the left and right eye,then
			visulize each of the eyes 

		"""

		leftEyeHull=cv2.convexHull(leftEye)
		rightEyeHull=cv2.convexHull(rightEye)
		jawHull = cv2.convexHull(jaw)

		
		cv2.drawContours(frame,[leftEyeHull],-1,(0,255,0),1)
		cv2.drawContours(frame,[rightEyeHull],-1,(0,255,0),1)
		cv2.drawContours(frame, [jawHull], 0, (0, 255, 0), 1)
		#check to see if the eye aspact ration is below the blink
		#threshold,and if so,increment the blink frame conuter
	



		if ear < EYE_AR_THRESH:
				COUNTER +=1

				"""
					if the eyes were closed for a sufficient number of
					then sound the alarm
				"""

				if COUNTER >= EYE_AR_CONSEC_FRAMES:
						#if the alarm is not on,turn it on
						if not ALARM_ON:
							ALARM_ON = True

							"""
							check to see if an alarm file was support
							and if so,start a thread to have a alarm
							sound plyed in background 
							"""
							if args["alarm"] != "":
								t = Thread(target=alarm_sound,args=(args["alarm"],))
								t.deamon=True
								t.start()
								
						cv2.putText(frame,"YOU ARE SLEEPY... PLEASE TAKE A BREAK!",(10,30),
							cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 0, 255), 2)
						
						
						  

	    	

			#otherwise,the eye aspect ration is not below the blink
			#theresold,so reset the counter and alarm
		    
		else:
			COUNTER = 0
			ALARM_ON = False

			
		
		if mar >= MOUTH_AR_THRESH:
			COUNTER_FRAMES_MOUTH += 1

		else:
			if COUNTER_FRAMES_MOUTH > 5:
				COUNTER_MOUTH += 1
				COUNTER_FRAMES_MOUTH = 0
	

	#Print The EAR And MAR Thershold
	
	"""
			draw the computed eye aspact ration pn the frame to help 
			with debugging and setting the correct eye aspect ration
	"""
	cv2.putText(frame,"EAR: {:.2f}".format(ear),(550,30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)					


	"""
			draw the computed Mouth aspact ration pn the frame to help 
			with debugging and setting the correct eye aspect ration
	"""
	cv2.putText(frame,"MAR: {:.2f}".format(mar), (550, 90),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
	
	cv2.putText(frame,"Mouths: {}".format(COUNTER_MOUTH),(550, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	#show the frame
	
	cv2.imshow("Frame",frame)
	key=cv2.waitKey(1) & 0xFF

	#if the 'q' key was pressed,break from the loop
	if key ==ord("q"):
			break
	

#do a bit of cleaup
cv2.destroyAllWindows()
vs.stop()
