Usecase: Identification of squarebox on a given image. You can test by using contours, how to identify region of interest, in this case a squarebox.

Tech Stack:  Python 3 and Python 2+ (This program tested with both the version)
Libraries: cv2 and imutils

Description: In Image roi.jpg - rectangular box is having very low intencity than other areas like straightligns and other content.

Before finding contours, we need to identify the edges. 

To identify the edge detection, we can use Canny from CV2. Canny uses a multi-stage algorithm to detect a wide range of edges in images.

Canny (image, minVal, maxVal) - min and max Val are intensity gradient values.

edged = cv2.Canny(blurred, 100, 200) --  with these values it will never identifies the rectangularbox on this specific cheque.

In code, change min and max values as given below  

edged = cv2.Canny(blurred, 10, 200)  - identifies the rectangulat box 

and first contour itself is the rectangular box.

edged = cv2.Canny(blurred, 35, 70) -get the rectangular box with 487 contours with first contour as cheque amount box.
