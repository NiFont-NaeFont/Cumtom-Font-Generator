# -*- coding: utf-8 -*-

import os
import argparse
from glob import glob
from PIL import Image
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Inference for unseen data')
parser.add_argument('--result_dir', dest='result_dir', required=True,
                    help='result_dir')
args = parser.parse_args()

os.system('mkdir %s' %os.path.join(args.result_dir,'1'))
os.system('mkdir %s' %os.path.join(args.result_dir,'2'))
os.system('mkdir %s' %os.path.join(args.result_dir,'3'))
os.system('mkdir %s' %os.path.join(args.result_dir,'4'))
os.system('mkdir %s' %os.path.join(args.result_dir,'5'))

file_list = os.listdir(args.result_dir)

condition = os.path.join(args.result_dir,'*.png')
pngfiles = sorted(glob(condition))


for img in pngfiles:
    print(img)
    pil_image = Image.open(img)
    pil_image = pil_image.rotate(270, expand=True)
    pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    
    open_cv_image = np.array(pil_image)
    cv2.imwrite(os.path.join(args.result_dir,'3')+'/'+os.path.basename(img),open_cv_image)
    
    kernel_size_row = 3
    kernel_size_col = 3
    kernel = np.ones((3, 3), np.uint8)
    erosion3_image = cv2.erode(open_cv_image, kernel, iterations=1)  #// make erosion image
    cv2.imwrite(os.path.join(args.result_dir,'5')+'/'+os.path.basename(img),erosion3_image)
    
    dilation3_image = cv2.dilate(open_cv_image, kernel, iterations=1)  #// make dilation image
    cv2.imwrite(os.path.join(args.result_dir,'1')+'/'+os.path.basename(img),dilation3_image)
    
    kernel_size_row = 2
    kernel_size_col = 2
    kernel = np.ones((2, 2), np.uint8)
    erosion2_image = cv2.erode(open_cv_image, kernel, iterations=1)  #// make erosion image
    cv2.imwrite(os.path.join(args.result_dir,'4')+'/'+os.path.basename(img),erosion2_image)
    dilation2_image = cv2.dilate(open_cv_image, kernel, iterations=1)  #// make dilation image
    cv2.imwrite(os.path.join(args.result_dir,'2')+'/'+os.path.basename(img),dilation2_image)
    
    os.system('rm '+img)