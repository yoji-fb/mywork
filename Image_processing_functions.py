"""
def image_output: Outputs image
def pdf2image: Convert a PDF to IMAGEs
def pdf2image_dir: Convert all pdf to image in the dir.
def saveTiffStack: Save multi-frame tiff file
def add_image: Add an img1 to an img0
def add_image_tif: Add an img1 to an img0 (multi-frame TIFF ver.)
def add_image_all: Add all the images to the another
def pdf2tiff_compare: Execute add_image_tif to 2 pdf files
def bmp2png: Convert bmp image to png image

"""
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import os
import glob
import cv2 as cv
import matplotlib.pyplot as plt

# Global settings -----------------------------------------------------------------
cwd = os.getcwd()

dpi = 200
filename0 = 'ILSDP_Z_K503_rev00'
filename1 = 'ILSDP_Z_K003_rev00_20211105'
page_off = True
page_length = 60
separation = 10
grayscale = True

# ---------------------------------------------------------------------------------

def image_output(
        pages: list, outputDir: str, format='.tif', filename='output file name'
):
    """
    :param pages: convert_from_path()
    :param outputDir: output file directory
    :param format: .tif/.jpg/.png
    :param filename: Select output file name
    :return:
    """
    # JPEG #
    if format == '.jpg':
        cnt = 0
        for page in pages:
            myfile = outputDir + '/' + filename + '_' + str(cnt) + format
            cnt += 1
            page.save(myfile, 'JPEG')
            print('Output: ', myfile)
    # PNG #
    elif format == '.png':
        cnt = 0
        for page in pages:
            myfile = outputDir + '/' + filename + '_' + str(cnt) + format
            cnt += 1
            page.save(myfile, 'PNG')
            print('Output: ', myfile)
    # TIFF #
    elif format == '.tif':
        myfile = outputDir + '/' + filename + '.tif'
        pages[0].save(myfile, 'TIFF', compression='tiff_deflate', save_all=True, append_images=pages[1:])
        print('Output: ', myfile)


def pdf2image(
    path: str,
    dpi=300,
    filename='Receipt Python3',
    format='.tif',
    page_off=False,
    page_length=1,
    separation=10,
    grayscale=False
):
    """
    :param path: PDF file path
    :param dpi: Select resolution
    :param filename: Input filename
    :param format: '.tif'/'.png'/'.jpg'
    :param page_off: True/False. Whether manage pages or not.
    :param page_length: int. False. Convert every pages
    :param separation: Divide all pages into the selected number of pages
    :param grayscale:
    :return:
    """
    # Settings #
    path = path.replace('\\', '/')
    pdf_path = path + '/' + filename + '.pdf'
    # Create ppm dir
    ppmData = path+'/PPM files/'
    # Create dir if path does not exist
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)

    # if page_off == True ----------------------------------------------------------
    if page_off:
        print('All pdf pages will be converted')
        # Convert #
        pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData, grayscale=grayscale)
        # Output #
        image_output(pages, path, format, filename)

    # if page_off == False ---------------------------------------------------------
    elif not page_off:
        print('page_length =', page_length)
        # Parameter for page setting
        quotient = page_length // separation
        remainder = page_length % separation
        # Quotient
        for j in range(quotient):
            # Convert #
            pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData,
                                      first_page=j * separation + 1, last_page=(j + 1) * separation)
            # Output #
            image_output(pages, path, format,
                         filename+'_'+str(j*separation+1)+'_'+str((j+1)*separation))
        # Remainder
        # Convert #
        if remainder != 0:
            pages = convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=ppmData,
                                      first_page=j * separation + 1, last_page=(j + 1) * separation + remainder)

            # Output #
            image_output(pages, path, format,
                         filename + '_' + str((j+1) * separation + 1) + '_' + str((j + 1) * separation + remainder))

    else:
        raise Exception('page_length must be int')


def pdf2image_dir(
    path: str,
    dpi=300,
    format='.tif',
    page_off=True,
    grayscale=False
):
    """
    Convert all pdf to image in the dir.
    :param path: PDF file path
    :param dpi: Select resolution
    :param format: '.tif'/'.png'/'.jpg'
    :param page_off: True/False. Whether manage pages or not.
    """
    # Settings #
    # path = path.replace('\\', '/')
    filelist = os.listdir(path)
    filelist = list(filter(lambda x: x.endswith('.pdf'), filelist))
    # Create ppm dir
    ppmData = path+'/PPM files/'
    # Create dir if path does not exist
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(ppmData):
        os.mkdir(ppmData)

    # if page_off == True ----------------------------------------------------------
    if page_off:
        for f in filelist:
            print('All pdf pages will be converted')
            # Convert #
            pages = convert_from_path(pdf_path=path+'\\'+f, dpi=dpi, output_folder=ppmData, grayscale=grayscale)
            # Output #
            image_output(pages, path, format, f.split('.pdf')[0])

    else:
        raise Exception('Only work when page_off=True')


def saveTiffStack(
        save_path: str,
        imgs: 'list'
):
    stack = []
    for img in imgs:
        stack.append(Image.fromarray(img))
    stack[0].save(save_path, compression='tiff_deflate', save_all=True, append_images=stack[1:])


def add_image(
        job_dir: str,
        filename0='Receipt Excel',  # pdf, filename_t must be bigger than filename1
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
        path: str,
        filename0=filename0,  # tiff, !filename_t must be bigger than filename1 (pixel size)
        filename1=filename1, # tiff
        grayscale=True
):
    path = path.replace('\\', '/')
    """
    Add img1 on img0. img0 is changed to color:cyan.
    :param path: Working directory.
    :param filename0:
    :param filename1:
    :param grayscale: True/False. True if input image is grayscale.
    :return:
    """
    f0_list, f1_list = [], []
    for file in os.listdir(path):
        if file.startswith(filename0) and file.endswith('.tif'):
            f0_list.append(file)
        if file.startswith(filename1) and file.endswith('.tif'):
            f1_list.append(file)

    for f0, f1 in zip(f0_list, f1_list):
        # Output filename
        out_filename = '{} on {}'.format(f1.split('.')[0], f0.split('.')[0])
        # Read (Multi-frame Tiff file)
        ret0, imgs0 = cv.imreadmulti(path + '/' + f0)
        ret1, imgs1 = cv.imreadmulti(path + '/' + f1)
        # Add img1 on img0
        cnt = 0
        for img0, img1 in zip(imgs0, imgs1):
            print('page' + str(cnt) + '\nimg0', img0.shape, '\nimg1', img1.shape)
            # img0 => img0_color. Convert gray to RGB (img0)
            img0_color = np.zeros((img0.shape[0], img0.shape[1], 3), dtype='uint8')

            if grayscale:
                # Threshold select for transparent region
                ret0, mask0 = cv.threshold(img0, 240, 255, cv.THRESH_BINARY)  # white -> out
                ret1, mask1 = cv.threshold(img1, 240, 255, cv.THRESH_BINARY)  # white -> out
                # Error handling. In case of color image input.
                if len(img1.shape) == 2:
                    rows, cols = img1.shape
                else:
                    print('Something is wrong with img1.shape!! Select grayscale unchecked')
            else:
                # Error handling. In case of gray image input.
                if len(img1.shape) == 3:
                    img0gray = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
                    img1gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                    ret0, mask0 = cv.threshold(img0gray, 240, 255, cv.THRESH_BINARY)  # white -> out
                    ret1, mask1 = cv.threshold(img1gray, 240, 255, cv.THRESH_BINARY)  # white -> out
                    rows, cols, channels = img1.shape
                else:
                    print('Something is wrong with img1.shape!! Select grayscale checked')

            img0_color[:, :, 0:] = 255  # Black to White
            img0_color[:, :, 0] = mask0  # White to Color  # Color select is here

            # Create a ROI (Region of Interest)
            roi = img0_color[0:rows, 0:cols]

            # White-out the BG in ROI
            img1_on_img0 = cv.bitwise_and(roi, roi, mask=mask1)
            # Turned out to be unnecessary lines ---------------
            # img0_bg = cv.bitwise_and(roi, roi, mask=mask1)
            # Take only region of Mask from img1
            # mask_inv = cv.bitwise_not(mask1)
            # img1_fg = cv.bitwise_and(img1, img1, mask=mask_inv)
            # Put img1 in ROI and modify the img0
            # dst = cv.add(img0_bg, img1_fg)  # ROI
            # img0[0:rows, 0:cols] = dst  # Full Image
            # --------------------------------------------------
            imgs0[cnt] = img1_on_img0
            cnt += 1

        # Output #
        print('Output: ', path + '/' + out_filename + '.tif')
        saveTiffStack(save_path=path + '/' + out_filename + '.tif', imgs=imgs0)


def add_image_all(
    job_dir,
    filename0='Receipt Excel',  # pdf, filename_t must be equal/bigger than filename1
    filename1='Receipt Python3', # pdf
    out_filename='add_image_all result',
):
    """
    Add img1 on img0 (for PNG/JPEG)
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
        print('Output: ', cwd + file_dir + out_filename + '_' + str(cnt) + '.png')
        cv.imwrite(job_dir + out_filename + '_' + str(cnt) + '.png', img0)

        cnt += 1


def pdf2tiff_compare(
        path: str,
        filename0='Receipt Excel',
        filename1='Receipt Python3',
        page_off=True,
        page_length=1,
        separation=10,
        grayscale=True,
):
    # First file #
    pdf2image(path=path, filename=filename0, format='.tif',
              page_off=page_off, page_length=page_length, separation=separation,
              grayscale=grayscale)

    # Second file #
    pdf2image(path=path, filename=filename1, format='.tif',
              page_off=page_off, page_length=page_length, separation=separation,
              grayscale=grayscale)

    # Output #
    add_image_tif(path=path, filename0=filename0, filename1=filename1, grayscale=grayscale)

###########################################################################################################
###########################################################################################################


def bmp2png(out_dir: str):
    cnt = 0
    for img in glob.glob('images/*.bmp'):
        Image.open(img).resize((300,300)).save(os.path.join(out_dir, + '_' + str(cnt) + '.png'))
        cnt += 1


# Mask image for making transparent image
def mask_image(img, b_from, g_from, r_from, b_to, g_to, r_to):
    color_lower = np.array([b_from, g_from, r_from, 255])
    color_upper = np.array([b_to, g_to, r_to, 255])
    img_mask = cv.inRange(img, color_lower, color_upper)
    img_bool = cv.bitwise_not(img, img, mask=img_mask)
    return img_bool


def image2image(
        path: str,
        direct_exe0: bool,
        direct_exe1: bool,
        regional_exe0: bool,
        regional_exe1: bool,
        input='.tif',
        output='.png',
        direct_dic={'b0': 255, 'g0': 255, 'r0': 255,
                    'b1': 255, 'g1': 255, 'r1': 255,
                    },
        from_dic = {'b0_from': 255, 'g0_from': 255, 'r0_from': 255,
                    'b1_from': 255, 'g1_from': 255, 'r1_from': 255,
                    'b2_from': 255, 'g2_from': 255, 'r2_from': 255,
                    },
        to_dic = {'b0_to': 255, 'g0_to': 255, 'r0_to': 255,
                  'b1_to': 255, 'g1_to': 255, 'r1_to': 255,
                  'b2_to': 255, 'g2_to': 255, 'r2_to': 255,
                  }
):
    """
    :param path:
    :param input: .tif/.png/.jpg/.bmp
    :param output: .tif/.png/.jpg/.bmp
    :return:
    Convert all the image in the directory to arbitrary format
    """
    # Settings #
    # path = path.replace('\\', '/')
    # Job directory
    filelist = os.listdir(path)
    filelist = list(filter(lambda x: x.endswith(input), filelist))

    # Make image transparent
    if output == '.png':
        for f in filelist:
            img = cv.imread(path + '\\' + f)
            # Add alpha channel to RGB
            if img.shape[2] == 3:
                img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
            # Convert to transparent
            # direct_exe #
            if direct_exe0:
                img[:, :, 3] = np.where(np.all(img == (direct_dic['b0'], direct_dic['g0'], direct_dic['r0']),
                                               axis=-1), 0, 255)
            # regional_exe #
            if regional_exe0:
                img = mask_image(img, from_dic['b0_from'], from_dic['g0_from'], from_dic['r0_from'],
                                 from_dic['b0_to'], from_dic['g0_to'], from_dic['r0_to'],
                                 )
            # Save #
            cv.imwrite(path + '\\' + f.split('.')[0] + output, img)




