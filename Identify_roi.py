from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2


def draw_contour(image, c, i):
	# compute the center of the contour area and draw a circle
	# representing the center
	M = cv2.moments(c)
	if M["m00"]==0:
		return image
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
	# draw the countour number on the image
	cv2.putText(image, "#{}".format(i), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 2)
	# return the image with the contour number drawn on it
	return image


def process_image(image1):
	image1 = imutils.resize(image1)
	cv2.imshow("sized  : ",image1)
	cv2.waitKey()
	gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
	cv2.imshow("gray  : ",gray)
	cv2.waitKey()
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	cv2.imshow("blurred  : ",blurred)
	cv2.waitKey()
	edged = cv2.Canny(blurred, 20, 200) #10,50 - working
	cv2.imshow("edged",edged)
	cv2.waitKey()
	return edged


def lineCountours(image1, threshold):
	th, contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

	print ("no. of contours:")
	print(len(contours))

	#cv2.drawContours(image1, contours,-1,(0,0,255),6)
	cv2.drawContours(image1, contours,-1,(0,255,255),6)
	# cv2.namedWindow("display", cv2.WINDOW_NORMAL)
	# cv2.imshow("display",image1)
	# cv2.waitKey()
	return contours, hierarchy

def chq_amt_identification(image1):
	process_image(image1)
	blurred  = cv2.pyrMeanShiftFiltering(image1, 10,50)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	image2=image1.copy
	gray_edged = process_image(image1)
	ret, threshold=cv2.threshold(gray_edged,2,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	contours, hierarchy = lineCountours(image1, threshold)
	cnts = sorted(contours, key=cv2.contourArea, reverse=True)
	displayCnt = None
	# loop over the contours
	image2=image1.copy
	rect_count=[]
	print(len(cnts))
	high_area=0
	for i,c in enumerate(cnts):
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04  * peri, True)
		# if the contour has four vertices, then we have found
		# the thermostat display
		x,y,w,h = cv2.boundingRect(c)
		area = w * h
		print(x,y,w,h,area,peri,i, len(approx) )
		displayCnt = approx
		print(x,y,w,h,area,peri,i, len(approx) )
		#if x>0 and y>0 and w>0 and h>0 and peri>0:
		draw_contour(image1,c,(i) )
		cv2.imshow("display  ",image1)
		cv2.waitKey()
		if len(approx) == 4:
			wraped = four_point_transform(gray, displayCnt.reshape(4, 2))
			output = four_point_transform(image1, displayCnt.reshape(4, 2))
			cv2.imshow("wraped Image : ", wraped)
			cv2.waitKey(0)
			break
	return gray, displayCnt

# load the example image main program
image1 = cv2.imread("roi.jpg") # working
image1 = imutils.resize(image1, height=420)
chq_amt_identification(image1)
