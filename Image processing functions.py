"""
def pdf2image: Convert a PDF to IMAGEs
def saveTiffStack: Save multi-frame tiff file
def add_image: Add an img1 to an img0
def add_image_tif: Add an img1 to an img0 (multi-frame TIFF ver.)
def add_image_all: Add all the images to the another
def pdf2png_compare: Execute add_image_all to 2 pdf files
def pdf2tiff_compare: Execute add_image_tif to 2 pdf files
def bmp2png: Convert bmp image to png image

"""

# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import glob
import os
from pdf2image import convert_from_path
import cv2 as cv


# Settings ------------------------------------------------------------------------
cwd = os.getcwd()

# ---------------------------------------------------------------------------------

def pdf2image(
    path='C:/Users/fx33403/ILSDP/Drawings/ILSLD_PA_K503_rev00_draft_20210729.pdf',
    dpi=300,
    outputDir='C:/Users/fx33403/ILSDP/Drawings/',
    filename='ILSLD_PA_K503_rev00_draft_20210729',
    format='JPEG'  # TIFF/JPEG
):

    ppmData = outputDir+'PPM files/'
    outputDir = outputDir + 'image/'

    # Create dir if path does not exist #
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)

    # Convert #
    pages = convert_from_path(pdf_path=path, dpi=dpi, output_folder=ppmData)

    # Output #
    cnt = 0
    if format == 'JPEG':
        # JPEG #
        for page in pages:
            myfile = outputDir + filename + '_' + str(cnt) + '.jpg'
            cnt += 1
            page.save(myfile, 'JPEG')
            print('Output: ', myfile)
    elif format == 'TIFF':
        # TIFF #
        myfile = outputDir + filename + '.tif'
        pages[0].save(myfile, 'TIFF', compression='tiff_deflate', save_all=True, append_images=pages[1:])
        print('Output: ', myfile)


def saveTiffStack(
        save_path='pdf2png_compare wd/saveTiffStack result tiff.tif',
        imgs=[np.array([])]
):
    stack = []
    for img in imgs:
        stack.append(Image.fromarray(img))
    stack[0].save(save_path, compression='tiff_deflate', save_all=True, append_images=stack[1:])


def add_image(
        job_dir='pdf2png_compare wd/image/',
        filename0='Receipt Excel',  # pdf, filename0 must be bigger than filename1
        filename1='Receipt Python3', # pdf
        out_filename='add_image result',
):
    """
    Add img1 on img0
    """
    # Read
    img0 = cv.imread(job_dir + filename0 + '.jpg')  # flags=-1: alpha mode
    img1 = cv.imread(job_dir + filename1 + '.jpg')  # flags=-1: alpha mode

    # img0 => img0_r
    img0_r = np.zeros(img0.shape, dtype='uint8')
    img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
    ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # White-out
    img0_r[:, :, :2] = 255  # White BG
    img0_r[:, :, 2] = mask0  # img0 => img0_r

    # I want to put logo on top-left corner, So I create a ROI (Region of Interest)
    rows, cols, channels = img1.shape
    roi = img0_r[0:rows, 0:cols]

    # Now create a mask of img1 and create its inverse mask also
    img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # White-out
    mask_inv = cv.bitwise_not(mask1)

    # White-out the BG in ROI
    img0_bg = cv.bitwise_and(roi, roi, mask=mask1)

    # Take only region of Mask from img1
    img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)

    # Put img1 in ROI and modify the img0
    dst = cv.add(img0_bg, img1_fg)  # ROI
    img0[0:rows, 0:cols] = dst  # Full Image

    # Output
    print('Output: ' + cwd + out_filename)
    cv.imwrite(job_dir + out_filename + '.png', img0)

    # Show
    cv.imshow('Out', img0)
    cv.waitKey(0)

    return img0, img1


def add_image_tif(
        job_dir='pdf2png_compare wd/',
        filename0='Receipt Excel',  # pdf, filename0 must be bigger than filename1
        filename1='Receipt Python3', # pdf
        out_filename='add_image_tif result',
):
    """
    Add img1 on img0
    """
    # Read (Multi-frame Tiff file) #
    ret0, imgs0 = cv.imreadmulti(job_dir + filename0 + '.tif')
    ret1, imgs1 = cv.imreadmulti(job_dir + filename1 + '.tif')

    cnt = 0
    for img0, img1 in zip(imgs0, imgs1):

        # img0 => img0_r #
        img0_b = np.zeros(img0.shape, dtype='uint8')
        img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
        ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # White-out
        img0_b[:, :, 0:] = 255  # White BG
        img0_b[:, :, 0] = mask0  # img0 => img0_b

        # I want to put logo on top-left corner, So I create a ROI (Region of Interest) #
        rows, cols, channels = img1.shape
        roi = img0_b[0:rows, 0:cols]

        # Now create a mask of img1 and create its inverse mask also #
        img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # White-out
        mask_inv = cv.bitwise_not(mask1)

        # White-out the BG in ROI #
        img0_bg = cv.bitwise_and(roi, roi, mask=mask1)

        # Take only region of Mask from img1 #
        img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)

        # Put img1 in ROI and modify the img0 #
        dst = cv.add(img0_bg, img1_fg)  # ROI
        img0[0:rows, 0:cols] = dst  # Full Image
        imgs0[cnt] = img0

        cnt += 1

    # Output #
    print('Output: ', cwd + job_dir + out_filename + '.tif')
    saveTiffStack(save_path=job_dir + out_filename + '.tif', imgs=imgs0)


def add_image_all(
    filename0='ILSLD_PA_K502_rev00',  # pdf, filename0 must be equal/bigger than filename1
    filename1='ILSLD_PA_K503_rev00_draft_20210729', # pdf
    out_filename='add_image_all result',
    job_dir='C:/Users/fx33403/ILSDP/Drawings/'
):
    """
    Add img1 on img0
    """
    file_dir = job_dir + 'image/'
    file0s, file1s = [], []

    # Split files to file0s and file1s
    for filename in os.listdir(file_dir):
        if filename0 in filename and 'jpg' in filename:
            file0s.append(filename)
        elif filename1 in filename and 'jpg' in filename:
            file1s.append(filename)

    cnt = 0
    for i in range(len(file0s)):

        # Read
        img0 = cv.imread(file_dir + file0s[i])  # flags=-1: alpha mode
        img1 = cv.imread(file_dir + file1s[i])  # flags=-1: alpha mode

        # img0 => img0_r
        img0_r = np.zeros(img0.shape, dtype='uint8')
        img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
        ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # White-out
        img0_r[:, :, :2] = 255  # White BG
        img0_r[:, :, 2] = mask0  # img0 => img0_r

        # I want to put logo on top-left corner, So I create a ROI (Region of Interest)
        rows, cols, channels = img1.shape
        roi = img0_r[0:rows, 0:cols]

        # Now create a mask of img1 and create its inverse mask also
        img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # White-out
        mask_inv = cv.bitwise_not(mask1)

        # White-out the BG in ROI
        img0_bg = cv.bitwise_and(roi, roi, mask=mask1)

        # Take only region of Mask from img1
        img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)

        # Put img1 in ROI and modify the img0
        dst = cv.add(img0_bg, img1_fg)  # ROI
        img0[0:rows, 0:cols] = dst  # Full Image

        # Output
        print('Output: ', cwd + file_dir + out_filename + '_' + str(cnt) + '.jpg')
        cv.imwrite(job_dir + out_filename + '_' + str(cnt) + '.jpg', img0)

        cnt += 1

    # # Output #
    # print('Output: ', cwd + job_dir + out_filename + '.tif')
    # saveTiffStack(save_path=job_dir + out_filename + '.tif', imgs=imgs0)


def pdf2png_compare(
        job_dir='pdf2png_compare wd/',
        filename0='Receipt Excel',
        filename1='Receipt Python3',
        out_filename='add_image_all result'
):
    """
    Execute add_image_all to 2 pdf files
    """
    file_dir = 'pdf2png_compare wd/image/'

    # First file #
    pdf2image(path=job_dir + filename0 + '.pdf', outputDir=file_dir, filename=filename0)

    # Second file #
    pdf2image(path=job_dir + filename1 + '.pdf', outputDir=file_dir, filename=filename1)

    # Output #
    add_image_all(filename0=filename0, filename1=filename1, out_filename=out_filename, job_dir=job_dir)


def pdf2tiff_compare(
        job_dir='C:/Users/fx33403/ILSDP/Drawings/',
        filename0='ILSLD_PA_K502_rev00',
        filename1='ILSLD_PA_K503_rev00_draft_20210729',
):
    out_filename = filename1 + ' on ' + filename0

    # First file #
    pdf2image(path=job_dir + filename0 + '.pdf', outputDir=job_dir, filename=filename0, format='TIFF')

    # Second file #
    pdf2image(path=job_dir + filename1 + '.pdf', outputDir=job_dir, filename=filename1, format='TIFF')

    # Output #
    add_image_tif(job_dir=job_dir, filename0=filename0, filename1=filename1, out_filename=out_filename)


def bmp2png(out_dir=''):
    """
    out_dir: output directory name
    """
    cnt = 0
    for img in glob.glob('images/*.bmp'):
        Image.open(img).resize((300,300)).save(os.path.join(out_dir, str(cnt) + '.png'))
        cnt += 1






