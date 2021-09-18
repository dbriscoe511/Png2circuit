from PIL import ImageGrab 
from PIL import Image
import PIL

def get_from_clipboard(): #TODO, this doesnt work
    return(ImageGrab.grabclipboard())
    #return(ImageGrab.grab())

#image = get_from_clipboard()

#image.show()


try:
    with Image.open('VCO.png') as im:
        im.show()
except:
    print("make sure an image is in the clipboard")
