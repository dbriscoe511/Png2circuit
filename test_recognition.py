import opencv_recognition
import cv2

test = int(input("1 for resistor, 2 for buck, 3 for pi_filter, 4 for text sample"))
draw_lines = int(input("draw lines? (slow)"))
if test == 1:
       a =opencv_recognition.recognition('components/R/R1.png')
       a.process_training_image(True,True,draw_lines,{'style':'two_port'})
       a.show_img() 
elif test == 2:
        a =opencv_recognition.recognition('demos/L6726_buck.png')
        a.process_training_image(True,True,draw_lines,{'style':'sch'})
        a.show_img()
elif test == 3:
        a =opencv_recognition.recognition('demos/pi_filter.jpg')
        a.process_training_image(True,True,draw_lines,{'style':'sch'})
        a.show_img()
elif test == 4:
        a =opencv_recognition.recognition('demos/Lorem_Ipsum_Helvetica.png')
        a.process_training_image(False,False,draw_lines,{'style':'sch'})
        a.show_img()
       

cv2.waitKey(0)