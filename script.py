import base64
from requests import post
from datetime import datetime
import time

from uuid import uuid4

def unix_time():
    dtime = datetime.now().timetuple()
    unix_tim = time.mktime(dtime)
    return float(unix_tim)

def get_image(prompt):
    param = {"prompt": prompt}

    Poster = post("https://bf.dallemini.ai/generate", json=param)
    try:
        j = Poster.json()["images"]
    except:
        j = None

    if j:
        L = []
        for i in range(len(j)):
            L.append(str.encode(j[i]))
        return L
    else:
        return j

def first_image(prompt):
    print(f"the prompt {prompt} has began")
    G = get_image(prompt)
    if G:

            image_64_decode = base64.decodebytes(G[0])
            file_name = f'images/{str(uuid4())}.png'
            image_result = open(file_name, 'wb')  # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            image_result.close()
            print(f"the prompt {prompt} has ended")
            return image_64_decode
    else:
        print("let the world burn")


def starter(prompt):

    G = get_image(prompt)
    if G:
        for i in range(len(G)):

            image_64_decode = base64.decodebytes(G[i])
            image_result = open(f'image{i}.png', 'wb')  # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            image_result.close()
    else:
        print("let the world burn")


if __name__ == '__main__':
    starter("house on fire")

