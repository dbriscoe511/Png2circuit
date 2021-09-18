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





class recognition():
    img = ''
    img_bin =''

    img_mask_txt =''
    img_annotated = ''
    img_canny = ''
    lines =''
    leads=''
    def __init__(self,img_path):
        self.img = cv2.imread(img_path)
    def prep_for_vision(self):
        #self.img_annotated = self.img
        self.img = cv2.medianBlur(self.img,3)
        self.img_bin = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        
        ret,self.img_bin = cv2.threshold(self.img_bin,200,255,cv2.THRESH_BINARY)
        
    def show_img(self):
        cv2.imshow('preview',self.img)
        cv2.imshow('bin',self.img_bin)
        cv2.imshow('annotated',self.img_annotated)
        cv2.imshow('PRE LINE DEL',self.image_t1)
        cv2.imshow('canny',self.img_canny)

    def draw_lines(self,lines,image):
        img = image.copy()
        if lines is not None:
            for line in lines:
                cv2.line(img, (line[0], line[1]), (line[2], line[3]), (0,0,255), 1, cv2.LINE_AA)
        return img

    def erode(self):
        height,width = mask.shape
        skel = np.zeros([height,width],dtype=np.uint8)      #[height,width,3]
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
        temp_nonzero = np.count_nonzero(mask)
        while(np.count_nonzero(mask) != 0 ):
            eroded = cv2.erode(mask,kernel)
            cv2.imshow("eroded",eroded)   
            temp = cv2.dilate(eroded,kernel)
            cv2.imshow("dilate",temp)
            temp = cv2.subtract(mask,temp)
            skel = cv2.bitwise_or(skel,temp)
            mask = eroded.copy()
        
        cv2.imshow("skel",skel)
        #cv2.waitKey(0)

    def find_lines(self,comp_type):
        
        self.img_canny = cv2.Canny(self.img_bin,100,200)
        self.lines = cv2.HoughLinesP(self.img_canny,1,np.pi / 180, 10, None, 5, 2) #TODO, change to canny

        #flatten inner lists (default = [ [[points]],[[points]] ]...)
        self.lines = np.ndarray.tolist(self.lines)
        self.lines = [i[0] for i in self.lines]

        self.image_t1 = self.draw_lines(self.lines,self.img)
        print(len(self.lines))

        #remove duplicate parrellel lines 
        tol = 3
        #print(self.lines)
        temp_lines = self.lines
        if temp_lines is not None:
            for l1 in temp_lines:
                for l2 in temp_lines:
                    if (abs(l1[0]-l2[0]) <= tol and abs(l1[1]-l2[1]) <= tol and abs(l1[2]-l2[2]) <= tol and abs(l1[3]-l2[3]) <= tol):
                        #print("match found  " + str(len(temp_lines)))
                        temp_lines.remove(l2)
        #remove duplicate parrellel lines. must have a slope and interccept within tol, and close by starting and ending points. 
        temp_lines = self.lines
        if temp_lines is not None:
            for l1 in temp_lines:
                for l2 in temp_lines:
                    sl1 = slopeintercept(l1)
                    sl2 = slopeintercept(l2)
                    if (abs(sl1[0]-sl2[0]) <= tol and abs(sl1[1]-sl2[1])):
                        if (abs(l1[0]-l2[0]) <= tol*2 and abs(l1[1]-l2[1]) <= tol*2 and abs(l1[2]-l2[2]) <= tol*2 and abs(l1[3]-l2[3]) <= tol*2):
                            print("match found  " + str(len(temp_lines)))
                            temp_lines.remove(l2) 

        self.lines = temp_lines
        print(len(self.lines))

        print(self.lines)
        self.img_annotated = self.draw_lines(self.lines,self.img)


        #finds component leads. This script makes me wish for death
        temp_lines = self.lines
        if comp_type['style'] == 'schematic':
            for j in range(0,comp_type['n_leads']):
                if temp_lines is not None:
                    for i in range(0, len(temp_lines)):

                        l = temp_lines[i][0]
                        min_coord = ''
                        min_line = ''
                        max_line = ''
                        max_coord = ''

                        #special case for 1 or 2 leads: only look for leads on top and bottom
                        if comp_type['n_leads'] <= 2:
                            min_coord = min(l[1,3])

                        #TODO, only perform these steps if the pin is at a right angle?
                        #tol = 5
                        #if np.arctan()

                        for n,coord in enumerate(l):
                            #special case for 1 or 2 leads: only look for leads on top and bottom
                            if comp_type['n_leads'] <= 2:
                                if not n%2 == 0:
                                    pass


                            else:
                                pass
    
    def process_training_image(self,correct_rotation,correct_size,comp_type):
        self.prep_for_vision()

        if correct_rotation:
            if self.img.shape[0] < self.img.shape[1]:
                self.img = np.rot90(self.img).copy() #TODO, will this break shit? 43892506
                self.img_bin = np.rot90(self.img_bin).copy()

        if correct_size:
            if comp_type['style'] == 'two_port': #TODO, add more preset options for scaleing
                self.img = crop_resize(self.img,0.5,500)
                self.img_bin = crop_resize(self.img_bin,0.5,500)

        self.find_lines(comp_type)




        


        pass


    def extract_mask_text(self):
        pass

    def recognize_part(self):
        pass


    

a =recognition('demos/pi_filter.jpg')
#a.show_img()
#a.prep_for_vision()
a.process_training_image(True,True,{'style':'two_port'})
a.show_img()

cv2.waitKey(0)