from frameless_window import FramelessWindow
from PyQt6.QtWidgets import QApplication
import sys
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

def get_window_capture(path: str):
    # window list
    window = pygetwindow.getWindowsWithTitle(path)[0]
    #screenshot and cropping
    left, top = window.topleft
    right, bottom = window.bottomright
    print((left, top, right, bottom))
    im = pyautogui.screenshot()
    im = im.crop((left, top, right, bottom))
    
    # just checking but it's not necessary
    im.save('screenshot.png', 'PNG')

    # return screenshot as a numpy array
    return np.array(im)


def make_img_transparent(img):
    PIL_image = Image.fromarray(img.astype('uint8')).convert('RGBA')
    datas = PIL_image.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    PIL_image.putdata(newData)

    PIL_image.save("screenshot_transparent.png", "PNG")
    return PIL_image


def scan_text(img: ndarray):
    picture_results = picture_read.readtext(img, batch_size=2, paragraph=True)

    spacer = 100
    print(img.shape)
    img[:, :] = 255 #make every pixel white

    detected_texts = []
    text_idx = 1
    for detection in picture_results:
        top_left_corner = [int(value) for value in detection[0][0]]
        bottom_right_corner = [int(value) for value in detection[0][2]]
        text = detection[1]
        print(text)
        if bool(re.match('[a-z0-9]+$', text, re.IGNORECASE)) is True: continue
        try:
            if detect(text) == 'ja':
                translated = GoogleTranslator(source='ja', target='en').translate(text)
                detected_texts.append((text_idx, translated))
                img = cv2.rectangle(img, top_left_corner,
                                    bottom_right_corner, (0, 255, 0, 255))
                img = cv2.putText(img, str(text_idx), top_left_corner,
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
                spacer += 15
                text_idx += 1
        except:
            print('Skipped')

    return { 'img': img, 'texts': detected_texts }



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_title = 'Captura'
    window = pygetwindow.getWindowsWithTitle(window_title)[0]
    left, top = window.topleft
    game_frame = get_window_capture(path=window_title)
    scan_results = scan_text(game_frame)
    processed_frame = make_img_transparent(scan_results['img'])
    print(scan_results['texts'])

    window2 = FramelessWindow(is_frameless=True, top_pos=top, left_pos=left, width=window.width, height=window.height)
    window2.load_image(processed_frame)
    window2.show()

    sys.exit(app.exec())

