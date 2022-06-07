"""snippet_mkdir.py
Makes the needed directories to
store segmented images 

Logan Sowards
BYU Record Linking Lab
Computer Vision Team

Edited by Amber Oldroyd
"""
import os

parent = "segmented/snippets/"
num_directories = 1000

for digit in range(num_directories):
    os.mkdir(parent + "d{}".format(digit))

