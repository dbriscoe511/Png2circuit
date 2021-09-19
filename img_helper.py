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
    if slope == 0:
        slope = 0.0000001
    intercept = line[1]-slope*line[0]
    dist = np.sqrt((line[3]-line[1])**2+(line[0]-line[2])**2)
    angle = np.arctan(slope)
    return [slope,intercept,dist,angle]

def getangle(l1,l2):
    sl1 = slopeintercept(l1)
    sl2 = slopeintercept(l2)

    angle = np.arctan((sl1[0]-sl2[0])/(1+sl1[0]*sl2[0]))
    return angle

def getintersect(l1,l2):
    # sl1 = slopeintercept(l1)
    # sl2 = slopeintercept(l2)
    # inter = [(-1*l2[1]-)
    xdiff = (l1[0]-l1[2],l2[0]-l2[2])
    ydiff = (l1[1]-l1[3],l2[1]-l2[3])
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return [(1000000,10000000),100000000000]

    d = (det(l1[0:2],l1[2:4]), det(l2[0:2],l2[2:4]))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    mind = 10000000000
    
    dist_tointersect = [np.sqrt((l1[0]-x)**2+(l1[1]-y)**2),np.sqrt((l1[2]-x)**2+(l1[3]-y)**2),np.sqrt((l2[0]-x)**2+(l2[1]-y)**2),np.sqrt((l2[2]-x)**2+(l2[3]-y)**2)]
    

    return [(x,y),min(dist_tointersect)]

def combineparrellellines(l1,l2):
    xpoints = [l1[0] ,l1[2] , l2[0] , l2[2]]
    ypoints = [l1[1] ,l1[3] , l2[1] , l2[3]]
    l3 =  [max(xpoints),max(ypoints),min(xpoints),min(ypoints)]
    if slopeintercept(l3)[0]>0 and slopeintercept(l1)[0]<0:
        l3 =  [max(xpoints),min(ypoints),min(xpoints),max(ypoints)]
    return l3


def randomcolor():
    #makes a color beteween 50 and 200 rgb value for debugging 
    return( np.random.randint(50,high=150),np.random.randint(50,high=150),np.random.randint(50,high=200))

#print(slopeintercept([-5,10,-3,4]))  = (-3,-5)