import sys
import numpy as np
import cvlib as cv
import cv2
sys.path.insert(0, '/Users/trac.k.y/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/cvlib')

#drawing a line on top/left of image
def draw_vert_line(image, linewidth, start, color = [0, 0, 0]):
    column = start
    while column < (linewidth + start):
        image[:, column] = color
        column += 1
    return image

def draw_horiz_line(image, linewidth, start, color = [0, 0, 0]):
    row = start
    while row < (linewidth + start):
        image[row] = color
        row += 1
    return image

'''
#pixel approach
def pixel_draw_horiz_line(image, linewidth, color = [0, 0, 0]):
    column = 0
    while column < len(image[0]):
        row = 0
        while row < linewidth:
            image[row, column] = color
            row += 1
        column += 1
    return image

def pixel_draw_vert_line(image, linewidth, color = [0, 0, 0]):
    row = 0
    while row < len(image[:, 0]):
        column = 0
        while column < linewidth:
            image[row, column] = color
            column += 1
        row += 1
    return image
'''
#flipping image upside down
def flip_vertical(image):
    start = 0
    end = len(image[:, 0]) - 1
    while start < end:
        image[[start, end]] = image[[end, start]]
        start += 1
        end -= 1
    return image

#flipping image left to right
def flip_horizontal(image):
    start = 0
    end = len(image[0]) - 1
    while start < end:
        image[: ,[start, end]] = image[: ,[end, start]] 
        start += 1
        end -= 1
    return image

#rotate image 90 degrees to the right
def rot90(image):
    height = image.shape[0]
    width = image.shape[1]
    new = 255 * np.ones(shape=[width,height,3],dtype='uint8') 
    row = 0
    column = height - 1
    while row < height and column >= 0:
        new[:, column] = image[row]
        column -= 1
        row += 1
    return new

'''
#pixel approach
def pixel_rot90(image):
    height = image.shape[0]
    width = image.shape[1]
    new = 255 * np.ones(shape=[width,height,3],dtype='uint8')
    row = 0
    column = height - 1
    while row < height and column >= 0:
        index = 0
        while index < width:
            new[index, column] = image[row, index]
            index += 1
        column -= 1
        row += 1
    return new
'''

#convert to grayscale
def grayscale(image):
    grayfactor = np.empty((3, 1))
    grayfactor[0] = 0.1140
    grayfactor[1] = 0.5870
    grayfactor[2] = 0.2989
    grayscale = image.dot(grayfactor)
    grayscale = np.array(grayscale, dtype = 'uint8')
    return grayscale

#convert to grayscale(gradual)
def grayscale_byrow(image, window = 'image', delay = 1000, width=100):
    cv2.imshow(window, image)
    for i in range(0, image.shape[0], width):
        image[i:i+width] = grayscale(image[i:i+width])
        cv2.waitKey(delay)
        cv2.imshow(window, image)

print("Enter a picture file name.")
filename = input(">>> ")
try:
    image = cv2.imread(filename)
    cv2.imshow(filename, image)
except:
    print("Error in processing image.")
    print("Your file name may be invalid or in the wrong directory.")
    print("Or maybe your image is not in the correct format.")
    print("Unfortunately I am too lazy to code out this bit properly for now,")
    print("so this vague error message is what you get lmao.")
    print("Please try again.")

while True:
    print(">>> Choose an option.")
    print("Press 1 to draw line")
    print("Press 2 to flip image")
    print("Press 3 to rotate")
    print("Press 4 to convert to grayscale")
    print("Press Q to quit program")
    choice = input(">>> ")
    if choice == "1":
        print("Choose the thickness in pixels of the line.")
        linewidth = int(input(">>> "))
        print("Choose from which pixel to start drawing the line.")
        start = int(input(">>> "))
        print("Choose the color of the line as an RGB tuple:")
        print("(format 'B G R')")
        print("Or, press enter to keep default color of black.")
        raw_color = input(">>> ")
        color = raw_color.split()
        for i in range(len(color)):
            color[i] = int(color[i])
        print("Finally, choose if you want to draw a horizontal (H) or vertical (V) line.")
        direction = input(">>> ")
        if direction == "H":
            cv2.imshow("original", image)
            result = draw_horiz_line(image, linewidth, start, color)
            cv2.imshow("with line", result)
        elif direction == "V":
            cv2.imshow("original", image)
            result = draw_vert_line(image, linewidth, start, color)
            cv2.imshow("with line", result)
        else:
            print("Invalid option.")
            print("Please try again:")
            continue
    elif choice == "2":
        print("Choose if you wish to flip the image horizontally (H) or vertically (V).")
        direction = input(">>> ")
        if direction == "H":
            cv2.imshow("original", image)
            result = flip_horizontal(image)
            cv2.imshow("flipped", result)
        elif direction == "V":
            cv2.imshow("original", image)
            result = flip_vertical(image)
            cv2.imshow("flipped", result)
        else:
            print("Invalid option.")
            print("Please try again:")
            continue
    elif choice == "3":
        cv2.imshow("original", image)
        rotated = rot90(image)
        cv2.imshow("rotated", rotated)
    elif choice == "4":
        print("Do you want the grayscale to be gradual? (Y/N)")
        decision = input(">>> ")
        if decision == "Y":
            grayscale_byrow(image, window = 'grayscale')
        elif decision == "N":
            cv2.imshow("original", image)
            grayscale = grayscale(image)
            cv2.imshow("grayscale", grayscale)
        else:
            print("Invalid option.")
            print("Please try again:")
            continue
    elif choice == "Q" or choice == "q":
        break
    else:
        print("Invalid option.")
        print("Please try again:")
        continue
    break
