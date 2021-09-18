import cv2
import numpy as np

#img = cv2.imread('demos/VCO.png')
#cv2.imshow('preview',img)
#cv2.waitKey(0)

def crop_resize(image,sizeratio,pixels):
    #gets a image to the correct aspect ratio and size without image distortion. white padding is used if needed, else the image is cropped
    im25 = int(image.shape[0]/(sizeratio*2))
    centered = int(image.shape[1]/2)
    #print(centered, im25)
    #self.img = self.img[:,0:im25*3]

    #adds whitespace or crops image depending on size
    if im25+centered < image.shape[0]:
        image = image[:,int(centered-im25):int(im25+centered)]
    else:
        padding_needed = int(abs(im25+centered - image.shape[1]))
        #print(padding_needed)
        image = cv2.copyMakeBorder(image,0,0,padding_needed,padding_needed,cv2.BORDER_CONSTANT,value = [255,255,255] )

    image = cv2.resize(image,(int(pixels/sizeratio),pixels), interpolation = cv2.INTER_AREA)
    return image

def slopeintercept(line): 
    if line[2]-line[0] == 0:
        line[2] +=1
    slope = (line[3]-line[1])/(line[2]-line[0])
    intercept = line[1]-slope*line[0]
    return [slope,intercept]

#print(slopeintercept([-5,10,-3,4]))  = (-3,-5)