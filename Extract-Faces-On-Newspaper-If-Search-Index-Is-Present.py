import zipfile
from PIL import Image
import cv2 as cv
from IPython.display import display
import numpy as np
import pytesseract

imgzip = zipfile.ZipFile("readonly/small_img.zip") # zip file address
inflist = imgzip.infolist()
aboutNewsPaper={}
for f in inflist:
    ifile = imgzip.open(f)
    pil_image = Image.open(ifile)
    numpy_array = np.array(pil_image)
    
    textFoundInImage=pytesseract.image_to_string(image = pil_image)
    aboutNewsPaper[ifile.name]={'pilImage':pil_image, 'numpyArray': numpy_array, 'textInImage':textFoundInImage }

from PIL import ImageDraw, ImageFont 
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml') #opencv haarcascade_frontalface_default.xml Location
search_index=input()
facesCanvaslst=[]
for image in aboutNewsPaper:
    print(image)
    if search_index in aboutNewsPaper[image]['textInImage']:
        print('TestFound')
        gray_img = cv.cvtColor(aboutNewsPaper[image]['numpyArray'], cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_img, 1.3, 5).tolist()
        print(faces)
        lstOfImg=[]
        if len(faces)!=0:
            text_Image = Image.new('RGB',(500,30))
            draw = ImageDraw.Draw(text_Image)
            font=ImageFont.truetype(font='readonly/fanwood-webfont.ttf', size=30)
            draw.text( (0,0), 'Result Found In {}'.format(image), font=font )
            facesCanvaslst.append( text_Image )
            print('making rectangles crop img')
            for rec in faces:
                print(rec)
                cropped_img = aboutNewsPaper[image]['pilImage'].crop((rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3])).resize((200,200))
                lstOfImg.append(cropped_img)
            print(len(lstOfImg))

            ## create a contact sheet from different brightnesses
            first_image=lstOfImg[0]
            print('mode:'+str(first_image.mode))
            print('width'+str(first_image.width*5))
            print('height'+str(first_image.height*2))
            contact_sheet=Image.new(first_image.mode, (first_image.width*5,first_image.height*2))
            x=0
            y=0

            for img in lstOfImg:
                # Lets paste the current image into the contact sheet
                contact_sheet.paste(img, (x, y) )
                # Now we update our X position. If it is going to be the width of the image, then we set it to 0
                # and update Y as well to point to the next "line" of the contact sheet.
                if x+first_image.width == contact_sheet.width:
                    x=0
                    y=y+first_image.height
                else:
                    x=x+first_image.width
            # resize and display the contact sheet
            contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
            facesCanvaslst.append( contact_sheet )
        else:
            text_Image = Image.new('RGB',(1000,30))
            draw = ImageDraw.Draw(text_Image)
            font=ImageFont.truetype(font='readonly/fanwood-webfont.ttf', size=30)
            draw.text( (0,0), 'Text Found In {} But No Faces'.format(image), font=font )
            
            facesCanvaslst.append( text_Image )
print(facesCanvaslst)
heightToKeep=0
for image in facesCanvaslst:
    heightToKeep+=image.height
result_image = Image.new('RGB',(500,heightToKeep))
y=0
for image in facesCanvaslst:
    result_image.paste(image,(0,y))
    y+=image.height
display(result_image)
