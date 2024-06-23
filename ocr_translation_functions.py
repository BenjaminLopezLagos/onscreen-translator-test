import cv2
import easyocr
import numpy as np
from numpy import ndarray
from deep_translator import GoogleTranslator
from PIL import Image, ImageQt
import pygetwindow
import pyautogui
from langdetect import detect
import re

picture_read = easyocr.Reader(['en', 'ja'], gpu=True)

def get_window_capture(window_title: str):
    # window list
    window = pygetwindow.getWindowsWithTitle(window_title)[0]
    #screenshot and cropping
    left, top = window.topleft
    right, bottom = window.bottomright
    print((left, top, right, bottom))
    im = pyautogui.screenshot()
    im = im.crop((left, top, right, bottom))
    
    # just checking but it's not necessary
    #im.save('screenshot.png', 'PNG')

    # return screenshot as a numpy array
    return np.array(im)


def make_img_transparent(img: ndarray):
    PIL_image = Image.fromarray(img.astype('uint8')).convert('RGBA')
    datas = PIL_image.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    PIL_image.putdata(newData)

    #PIL_image.save("screenshot_transparent.png", "PNG")
    return PIL_image


def get_results_from_capture(img: ndarray):
    img = cv2.resize(img, None, fx=1.15, fy=1.15, interpolation=cv2.INTER_LINEAR)

    #processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    """    # Noise removal using Gaussian Blur
        processed_img = cv2.GaussianBlur(img, (7, 7), sigmaX=2)
    """
        
        # Define a sharpening kernel
    sharpening_kernel = np.array([[0, -1, 0],
                                [-1,  5, -1],
                                [0, -1, 0]])
        
    # Apply the sharpening kernel to the blurred image
    img = cv2.filter2D(img, -1, sharpening_kernel)
    
    picture_results = picture_read.readtext(img, low_text=0.3, batch_size=16, paragraph=True, y_ths=0.02)

    spacer = 100
    print(img.shape)
    img[:, :] = 255 #make every pixel white

    detected_texts = []
    text_idx_list = []
    text_idx = 1

    translator = GoogleTranslator(source='ja', target='en')
    for detection in picture_results:
        top_left_corner = [int(value) for value in detection[0][0]]
        bottom_right_corner = [int(value) for value in detection[0][2]]
        text = detection[1]
        print(text)
        #if bool(re.match('[a-z0-9]+$', text, re.IGNORECASE)) is True: continue
        try:
            if detect(text) == 'ja':
                #translated = translator.translate(text)
                detected_texts.append(text)
                text_idx_list.append(text_idx)
                img = cv2.rectangle(img, top_left_corner,
                                    bottom_right_corner, (0, 255, 0, 255), thickness=2)
                img = cv2.putText(img, str(text_idx), top_left_corner,
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4, cv2.LINE_AA)
                spacer += 15
                text_idx += 1
        except:
            print('Line Skipped')

    translated_texts = translator.translate_batch(detected_texts)
    processed_texts = []
    for i in range(0, len(detected_texts)):
        processed_texts.append((text_idx_list[i], re.sub(r'[^a-zA-Z0-9,.;¿? ]+', '', translated_texts[i])))
    
    print(translated_texts)
    print(processed_texts)
    overlay_img = make_img_transparent(img)
    return { 'img': overlay_img, 'texts': processed_texts }


