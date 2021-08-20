from mss import mss
import time
import pytesseract
import re
import glob
import sys
import websockets
import asyncio
import json
import os

try:
    from PIL import Image
except ModuleNotFoundError:
    import Image

#SCREENSHTO COOLDOWN BETWEEN EACH SCREENSHOT AND OCR (SCREENSHOTING DOESN'T TAKE MUCH PERFORMANCE)
cooldown = 0.2
#port where local websocket will be hosted
port = 5521
#max score for ocr validation
max_score = 600

pytesseract.pytesseract.tesseract_cmd = os.getenv("LOCALAPPDATA") + r"\Programs\Tesseract-OCR\tesseract"
# ^ DEFAULT TESSERACT LOCATIONL, IF YOU DON'T HAVE TESSERACT INSTALLED TYPE THIS


# 164,937
# 208,983
# 154,994
# 196,1041


#psm 10, 7, 6 working on example
config = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789"
sct = mss()

def screenshots():
    alpha = sct.grab({"top": 940, "left": 155, "width": 60, "height": 42})
    bravo = sct.grab({"top": 996, "left": 155, "width": 60, "height": 45})
    return alpha, bravo

def convert_to_pil_image(alpha, bravo):
    alpha_img = Image.frombytes("RGB", alpha.size, alpha.bgra, "raw", "BGRX").convert("L")
    bravo_img = Image.frombytes("RGB", bravo.size, bravo.bgra, "raw", "BGRX").convert("L")
    return alpha_img, bravo_img

def image_to_score(image):
    res = pytesseract.image_to_string(image, lang="splitgate", config=config).strip()
    list_of_numbers = re.findall(r'\d+', res)
    try:
        result_number = int(''.join(list_of_numbers))
        return result_number
    except ValueError:
        return 999999

def save_result(ocr_text, image):
    global existing_images
    try:
        if ocr_text not in existing_images:
            image.save(rf"Images/{str(ocr_text)}.jpg")
            print(f"Saved new image: {str(ocr_text)}.jpg")
            existing_images.append(f"{str(ocr_text)}")
            return existing_images
    except ValueError:
        pass
    #     max_number = 0
    #
    #     for IMAGE in existing_images:
    #         if IMAGE.startswith("undefined_"):
    #             max_number = IMAGE.split("undefined_")[1]
    #     existing_images.append(f"undefined_{str(int(max_number) + 1)}")
    #     image.save(rf"UndefinedImages/undefined_{str(int(max_number) + 1)}.jpg")
    #     print(f"Saved new undefined image: {str(int(max_number) + 1)}.jpg")



def without_websocket():
    prev_score = [0, 0]
    existing_images = []
    for filename in glob.glob(r"images/*.jpg"):
        existing_images.append(filename.split(".")[0][7:])

    for filename in glob.glob(r"UndefinedImages/*.jpg"):
        existing_images.append(filename.split(".")[0][16:])
    while True:
        alpha, bravo = screenshots()
        alpha_img, bravo_img = convert_to_pil_image(alpha, bravo)
        alpha_score = image_to_score(alpha_img)
        bravo_score = image_to_score(bravo_img)
        if int(alpha_score) < max_score and int(bravo_score) < max_score and int(alpha_score) > -10 and int(bravo_score) > -10:
            # any wss or anything about score do here
            if [alpha_score, bravo_score] != prev_score:
                prev_score = [alpha_score, bravo_score]
                sys.stdout.write(f"\rAlpha: {str(alpha_score)}, Bravo: {str(bravo_score)}")
        time.sleep(cooldown)


async def websocket_server(websocket, path):
    prev_score = [0, 0]
    existing_images = []
    for filename in glob.glob(r"images/*.jpg"):
        existing_images.append(filename.split(".")[0][7:])

    for filename in glob.glob(r"UndefinedImages/*.jpg"):
        existing_images.append(filename.split(".")[0][16:])
    while True:
        alpha, bravo = screenshots()
        alpha_img, bravo_img = convert_to_pil_image(alpha, bravo)
        alpha_score = image_to_score(alpha_img)
        bravo_score = image_to_score(bravo_img)
        if int(alpha_score) < max_score and int(bravo_score) < max_score and int(alpha_score) > -10 and int(bravo_score) > -10:
            # any wss or anything about score do here
            if [alpha_score, bravo_score] != prev_score:
                prev_score = [alpha_score, bravo_score]
                # sys.stdout.write(f"\rA: {str(alpha_score)}, B: {str(bravo_score)}")
                # print({"Alpha": int(alpha_score), "Bravo": int(bravo_score)})
                dicti = dict(Alpha=alpha_score, Bravo=bravo_score)
                print(dicti)
                # "{Alpha: " + str(alpha_score) + ", " + "Bravo: " + str(bravo_score) + "}"
                # print(dict)
                await websocket.send(json.dumps(dicti))

        # save_result(alpha_score, alpha_img)
        # save_result(bravo_score, bravo_img)
        await asyncio.sleep(cooldown)







# without_websocket()
#if you want to disable websockets comment theese three lines and uncommend line above
start_server = websockets.serve(websocket_server, "localhost", port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()