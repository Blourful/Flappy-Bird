import os
import pygame
import random
pygame.init()
W , H = 288, 512
FPS = 50

IMAGES = {}
AUDIOS = {}
# 获取文件夹中的所有文件
for image in os.listdir('assets/sprites'):

    name_image, extension_image = os.path.splitext(image)
    
    if extension_image.lower() == '.png':
        
        path = os.path.join('assets/sprites', image)
        IMAGES[name_image] = pygame.image.load(path)

for audio in os.listdir('assets/audio'):

    name_audio, extension_audio = os.path.splitext(audio)
    
    if extension_audio.lower() == '.wav' or extension_audio.lower() == ".mp3":
        
        path = os.path.join('assets/audio', audio)
        AUDIOS[name_audio] = pygame.mixer.Sound(path)


    
floor_y = H - IMAGES["floor"].get_height()
guide_x = (W - IMAGES["guide"].get_width())/2
guide_y = (floor_y - IMAGES["guide"].get_height())/2

over_x = (W - IMAGES["gameover"].get_width())/2
over_y = (floor_y - IMAGES["gameover"].get_height())/2

# print(AUDIOS)