"""snippet_mkdir.py
Makes the needed directories to
store segmented images 

Logan Sowards
BYU Record Linking Lab
Computer Vision Team
"""
import os
from sys import argv

# This script assumes you are using a dataset with multiple years
year = argv[1]
parent = "segmented/snippets/{}/".format(year)
num_directories = 1000

os.mkdir(parent)

for digit in range(num_directories):
    os.mkdir(parent + "d{}".format(digit))

