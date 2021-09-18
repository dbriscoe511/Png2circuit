# Png2circuit
Takes in an image or a PDF of a circuit and spits out an editable kicad schematic. Work in progress. 

Theory of operation:

Image_process produces a number of outputs, mostly using OpenCV built in tools. This script uses tesseract to extract any text from the image and masks it for the next steps.
Detect_parts detects parts and puts a green box around them. at this step, a user can verify and change sensitivity so most parts are detected
    - this section calls a methoud in image process that appropriatly scales the image so parts align with kicad part sizes
Recognize_part uses template matching to find the closest matched part
    - if this is recognized as an IC, it is passed to 
Write_output uses kicad's API to write a schematic that includes 
    wire_parts connects parts together

img_helper has a few stand alone methods to help process images. 