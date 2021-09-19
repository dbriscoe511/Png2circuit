import cv2
import numpy as np
import img_helper as ih

#img = cv2.imread('demos/VCO.png')
#cv2.imshow('preview',img)
#cv2.waitKey(0)


class recognition():
    img = ''
    img_bin =''

    img_mask_txt =''
    img_annotated = ''
    img_canny = ''
    lines =''
    lines_noparrellel =''
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

    def draw_lines(self,lines,image,randomcolor):
        img = image.copy()
        if lines is not None:
            for line in lines:
                if randomcolor:
                    cv2.line(img, (line[0], line[1]), (line[2], line[3]), ih.randomcolor(), 2, cv2.LINE_AA)
                else:
                    cv2.line(img, (line[0], line[1]), (line[2], line[3]), (0,0,255), 2, cv2.LINE_AA)
        return img


    def find_lines(self,comp_type):
        
        self.img_canny = cv2.Canny(self.img_bin,100,200)
        self.lines = cv2.HoughLinesP(self.img_canny,1,np.pi / 180, 30, None, 15, 2) #TODO, change to canny

        #flatten inner lists (default = [ [[points]],[[points]] ]...)
        self.lines = np.ndarray.tolist(self.lines)
        self.lines = [i[0] for i in self.lines]

        self.image_t1 = self.draw_lines(self.lines,self.img,False)
        print(len(self.lines))

         
        tol = 1.5
        #remove duplicate parrellel lines. must have a slope and interccept within tol, and close by starting and ending points.
        # temp_lines = []
        # temp_lines2 = self.lines.copy()
        # if temp_lines2 is not None:
        #     for l1 in temp_lines2:
        #         for l2 in temp_lines2:
        #             sl1 = ih.slopeintercept(l1)
        #             sl2 = ih.slopeintercept(l2)
        #             if (abs(1-sl1[0]/sl2[0]) <= tol/10 and abs(sl1[1]-sl2[1])<= tol):
        #                 if l2 in temp_lines2 and l1 in temp_lines2 and not l1 ==l2:
        #                     #shorter = l2 if sl1[2]>sl2[2] else l1
        #                     #print(shorter)
        #                     # temp_lines2.remove(shorter)
        #                     #temp_lines2.remove(l1)
        #                     #temp_lines2.remove(l2)
        #                     l1 = [0,0,0,1]
        #                     l2 = (ih.combineparrellellines(l1,l2))
        #                     # temp_lines2.append(ih.combineparrellellines(l1,l2))
        #                 # if (abs(l1[0]-l2[0]) <= tol*2 and abs(l1[1]-l2[1]) <= tol*2 and abs(l1[2]-l2[2]) <= tol*2 and abs(l1[3]-l2[3]) <= tol*2):
        #                 #     #print("match found  " + str(len(temp_lines)))
        #                 #     temp_lines.remove(l2) 
        tol = 3
        slopediv = 1
        interdiv = 500

        if self.lines is not None:
            change = True
            i = 0 
            al = []
            while change:
                mintol = tol*5
                minlines = []
                for l1 in self.lines:
                    for l2 in self.lines:
                        if not l1 == l2:
                            sl1 = ih.slopeintercept(l1)
                            sl2 = ih.slopeintercept(l2)
                            #dif = abs(1-sl1[0]/sl2[0])/slopediv + abs(sl1[1]-sl2[1])/(interdiv*abs(sl1[0]*sl2[0]))
                            dif = abs(sl1[3]-sl2[3])/slopediv + ih.getintersect(l1,l2)[1]/interdiv
                            if mintol>dif:
                                mintol = dif
                                #print(dif)
                                minlines = [l1,l2]

                change = mintol<tol
                i +=1
                if change:
                    self.lines.remove(minlines[0])
                    self.lines.remove(minlines[1])
                    self.lines.append(ih.combineparrellellines(minlines[0],minlines[1]))
                    print('loop')
                    temp = self.draw_lines(self.lines[0:len(self.lines)-1],self.img,False)
                    temp = self.draw_lines([self.lines[len(self.lines)-1]],temp,True)
                    cv2.imshow(str(i),temp)
                    #al.append(ih.combineparrellellines(minlines[0],minlines[1]))
            #print (al)
            #for line in al:
             #   self.lines.append(line)
            print(self.lines)
            #cv2.imshow(str(i),self.draw_lines(self.lines,self.img))


        
        #self.lines = temp_lines
        #self.lines_noparrellel = temp_lines2
        print(len(self.lines))
        #print(len(self.lines_noparrellel))

        #print(self.lines)
        self.img_annotated = self.draw_lines(self.lines,self.img,False)


        # #finds component leads. This script makes me wish for death
        
        # temp_lines = self.lines
        # if comp_type['style'] == 'schematic':
        #     for j in range(0,comp_type['n_leads']):
        #         if temp_lines is not None:
        #             for i in range(0, len(temp_lines)):

        #                 l = temp_lines[i][0]
        #                 min_coord = ''
        #                 min_line = ''
        #                 max_line = ''
        #                 max_coord = ''

        #                 #special case for 1 or 2 leads: only look for leads on top and bottom
        #                 if comp_type['n_leads'] <= 2:
        #                     min_coord = min(l[1,3])

        #                 #TODO, only perform these steps if the pin is at a right angle?
        #                 #tol = 5
        #                 #if np.arctan()

        #                 for n,coord in enumerate(l):
        #                     #special case for 1 or 2 leads: only look for leads on top and bottom
        #                     if comp_type['n_leads'] <= 2:
        #                         if not n%2 == 0:
        #                             pass
        #                     else:
        #                         pass
    
    def process_training_image(self,correct_rotation,correct_size,comp_type):
        self.prep_for_vision()

        if correct_rotation:
            if self.img.shape[0] < self.img.shape[1]:
                self.img = np.rot90(self.img).copy() #TODO, will this break shit? 43892506
                self.img_bin = np.rot90(self.img_bin).copy()

        if correct_size:
            if comp_type['style'] == 'two_port': #TODO, add more preset options for scaleing
                self.img = ih.crop_resize(self.img,0.5,500)
                self.img_bin = ih.crop_resize(self.img_bin,0.5,500)

        self.find_lines(comp_type)




        


        pass


    def extract_mask_text(self):
        pass

    def recognize_part(self):
        pass


    

a =recognition('components/rs.png')
#a.show_img()
#a.prep_for_vision()
a.process_training_image(True,True,{'style':'two_port'})
a.show_img()

cv2.waitKey(0)