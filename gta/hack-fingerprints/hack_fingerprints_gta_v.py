from PIL import ImageGrab, ImageOps
import pyautogui
import time
import numpy as np
from numpy import *
from pynput.keyboard import Key, Controller
keyboard = Controller()
import keyboard as kb
from directkeys import ReleaseKey, PressKey, W, A, S, D, ENTER, TAB

from skimage import measure
import matplotlib.pyplot as plt
import cv2
from skimage.metrics import structural_similarity as ssim
import os


big_fingerprint_coordinates = (1248,209,1786,895) #538x686
small_fingerprint_coordinates = [(634,362,789,517),(826,362,981,517),(634,553,789,708),(826,553,981,708),(634,746,789,901),(827,746,982,901),(635,938,790,1093),(827,938,982,1093)] #155x155



def get_big_fingerprint_class():
    fp_image = ImageGrab.grab(big_fingerprint_coordinates)
    fp_image.save("tmp_bfp/big.png")

    score_list = []
    for i in os.listdir("big_finger_prints"):
        score = compare_images("tmp_bfp/big.png","big_finger_prints/"+i)
        score_list.append(score)

    fp_class = score_list.index(max(score_list))

    return fp_class 

def get_small_fingerprint():
    for i,coord in enumerate(small_fingerprint_coordinates):
        fp_image = ImageGrab.grab(coord)
        name = "small_"+str(i)+".png"
        fp_image.save("tmp_sfp/"+name)     
    return True

def get_correct_small_fp_position(big_fingerprint):
    #compare the smalls fp obtaineds with the stored and return the 4 with max values

    scores = []

    for tmp_sfp in os.listdir("tmp_sfp"):
        temp_scores = []
        for sfp in os.listdir("small_finger_prints/"+str(big_fingerprint)):            
            score = compare_images("tmp_sfp/"+tmp_sfp,"small_finger_prints/"+str(big_fingerprint)+"/"+sfp)
            temp_scores.append(score)
            
        scores.append(max(temp_scores))

    scores_with_indx = list(enumerate(scores))
    scores_with_indx.sort(key=lambda r:r[1])
    
    #Take the 4 indexes of max score
    max_score_indexs = list(map(lambda x: x[0],scores_with_indx[len(scores_with_indx)-4:]))

    return max_score_indexs
        


def compare_images(path_imageA,path_imageB):
        imageA = cv2.imread(path_imageA)
        imageB = cv2.imread(path_imageB)
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        simm = ssim(imageA,imageB)
        return simm  

def press_enter(positions_to_press):
    positions_to_press.sort()

    t=0.05

    for pos in range(0,8):
        if(pos in positions_to_press):
            PressKey(ENTER)
            time.sleep(t)
            ReleaseKey(ENTER)
            #print('enter')
            
        if(pos%2==0):
            PressKey(D)
            time.sleep(t)
            ReleaseKey(D)
        else:
            if(pos==7):
                return
            PressKey(S)
            time.sleep(t)
            ReleaseKey(S)
            time.sleep(t)
            PressKey(A)
            time.sleep(t)
            ReleaseKey(A)
        time.sleep(t)
    

big_fingerprint = 0            
def main():
    global big_fingerprint
    global small_fingerprint
    print('READY')
    while True:
        if kb.is_pressed('q'):
            print('EXIT!')
            break
            
        if kb.is_pressed('x'):
            big_fingerprint = get_big_fingerprint_class()
            print("Big FP class = "+str(big_fingerprint))
            get_small_fingerprint()

            small_fp_pos = get_correct_small_fp_position(big_fingerprint)
            print(small_fp_pos)

            press_enter(small_fp_pos)
            
            PressKey(TAB)
            time.sleep(0.2)
            ReleaseKey(TAB)
                
            print('Done')
                
                
                
                
        time.sleep(0.01)



main()

