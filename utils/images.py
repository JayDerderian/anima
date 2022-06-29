'''
module for processing images to be used as data for melodic, harmonic, or rhythm generation

read up, chump:
    https://www.geeksforgeeks.org/how-to-convert-images-to-numpy-array/
    https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays


'''
from numpy import asarray
from PIL import Image


def convert_to_list(file_name):
    '''
    converts a given image into an array of integers
    
    parameters
    -----------
    file_name (str). this should be something like "image.jpg".
    it will retrieve the image from the current working directory and
    convert it to an array of integers. 

    returns
    --------
    image = [int] * n (where n is total number of pixels!)
    '''
    img = Image.open(file_name)
    return asarray(img)