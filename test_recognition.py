import opencv_recognition
import cv2

test = int(input("1 for resistor, 2 for buck, 3 for pi_filter"))
if test == 1:
       a =opencv_recognition.recognition('components/rs.png')
       a.process_training_image(True,True,{'style':'two_port'})
       a.show_img() 
elif test == 2:
        a =opencv_recognition.recognition('demos/L6726_buck.png')
        a.process_training_image(True,True,{'style':'sch'})
        a.show_img()
else:
        a =opencv_recognition.recognition('demos/pi_filter.jpg')
        a.process_training_image(True,True,{'style':'sch'})
        a.show_img()
       

cv2.waitKey(0)