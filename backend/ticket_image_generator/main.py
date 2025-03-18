from PIL import Image, ImageFont, ImageDraw # for the image
import os # to delete image after your done with it

###*    NOTES    *###
# This code can generate a ticket from almost scratch, 
# it just needs a starter image (which is included). 
# It can be adapted to get data from elsewhere, but 
# still needs a few things to be used properly
#todo       print the image to printer when done
#todo       get data from the database
#?          how/where will printing be handled?
#?          how do we even print stuff?
#?          is all the information needed there? (do we need a name on it for drawings?)
#?          what font will we use? (is this one ok? do we need something more accesable/easier to read?)
#! NEEDS PIL TO WORK
# im not very familiar with servers, but from what I know it is possible to get this to work on one
# also this looks better with the better comments extention for vscode if you don't have it




#* Variables for the code
# will probably be gotten from the database later in the code, but im just setting them here for example
eName = str("County Fair")
eNum = int(5)
rNum = int(7)
hNum = int(2)
refNum = int(52)
lNum = str("948673")
numOfTickets = int(10) # change this to see different amounts of tickets! (up to 10)
point = 150 # will be for 


#* Open an Image
img = Image.open('blank.png')


#* Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)
  

#* Prepare the font and size
#! you need to change the path to wherever the font is stored at (if you change the location)
font_title = ImageFont.truetype(r'fonts\\Hobbyhorse-2468.ttf', 40) 
font_reg = ImageFont.truetype(r'fonts\\Hobbyhorse-2468.ttf', 30) 
# there needs to be 2 for the different sizes of text
 

#* Add Text to an image
# (position of text, string of text, color, font used)
#! dont change the format for the color (fill=(0, 0, 0)). will mess the code up (won't be put on the image)
I1.text((350, 30), eName, fill=(0, 0, 0), font = font_title)
I1.text((165, 110), "Event No.", fill=(0, 0, 0), font = font_reg)
I1.text((315, 110), "Race No.", fill=(0, 0, 0), font = font_reg)
I1.text((465, 110), "Horse No.", fill=(0, 0, 0), font = font_reg)
I1.text((615, 110), "Ref No.", fill=(0, 0, 0), font = font_reg)

#* Handles up to 10 raffle purchases
# this would need to know how many tickets there are, then update the vars. 
# idk how this would be done yet, I think it would depend on the database. 
# also it might need to handle more, but this will work for now
#! set number of tickets
for i in range(0, numOfTickets):
    #! change variables here
    I1.text((165, point), str(eNum), fill=(0, 0, 0), font = font_reg)
    I1.text((315, point), str(rNum), fill=(0, 0, 0), font = font_reg)
    I1.text((465, point), str(hNum), fill=(0, 0, 0), font = font_reg)
    I1.text((615, point), str(refNum), fill=(0, 0, 0), font = font_reg)
    point += 30


#* Copy prev text
I1.text((350, 530), eName, fill=(0, 0, 0), font = font_title)
I1.text((165, 610), "Event No.", fill=(0, 0, 0), font = font_reg)
I1.text((315, 610), "Race No.", fill=(0, 0, 0), font = font_reg)
I1.text((465, 610), "Horse No.", fill=(0, 0, 0), font = font_reg)
I1.text((615, 610), "Ref No.", fill=(0, 0, 0), font = font_reg)

point = 650
for i in range(0, numOfTickets):
    #! change variables here
    I1.text((165, point), str(eNum), fill=(0, 0, 0), font = font_reg)
    I1.text((315, point), str(rNum), fill=(0, 0, 0), font = font_reg)
    I1.text((465, point), str(hNum), fill=(0, 0, 0), font = font_reg)
    I1.text((615, point), str(refNum), fill=(0, 0, 0), font = font_reg)
    point += 30



#* Put the license stuff at the bottom
I1.text((165, 465), ("This event is sanctioned by IGC license NO." + lNum), fill=(0, 0, 0), font = font_reg)
I1.text((165, 965), ("This event is sanctioned by IGC license NO." + lNum), fill=(0, 0, 0), font = font_reg)


#* Save the edited image
# can put in the path where it will be saved, just putting it here for now
img.save("new_ticket_example.png")
# will just overide the prev file if the name used again, so don't worry 
# about new files being made if not deleted


#* Optional, to delete the image once it has been used
# os.remove("new_ticket_example.png")

# I think that it will be printed out, then deleted
# I don't have a printer to test it out, but I will look at printing stuff later #?(should a button on the website control this part? something else?)
# this thread seems useful for printing (https://stackoverflow.com/questions/12723818/print-to-standard-printer-from-python)
