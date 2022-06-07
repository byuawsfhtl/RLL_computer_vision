"""restructure.py

Johnson Merrell and Grant White
BYU Record Linking Lab
Computer Vision Team
"""

import os
import shutil
from sys import argv

def restructure(num_directories=1000):
    # pwd is /fslhome/mjmerrel/fsl_groups/fslg_death/compute/projects/<state>_death/imgs/
    year = argv[1]
    temp = "temp/"
    parent = "orig/decompressed/{}/".format(year)
    albums = os.listdir(parent)
    os.mkdir(parent + temp) # makes temporary directory for all images from a state

    for a in albums:
        images = os.listdir(parent + a)
        for i in images:
            os.rename(parent + a + "/" + i, parent + temp + i)
        shutil.rmtree(parent + a)

    for digit in range(num_directories):
        os.mkdir(parent + "d{}".format(digit))

    all_images = os.listdir(parent + temp)
    for num, image in enumerate(all_images):
        goto = num % num_directories
        dd = "d{}/".format(goto)
        os.rename(parent + temp + image, parent + dd + image)

    shutil.rmtree(parent + temp)

if __name__ == "__main__":
    restructure()
