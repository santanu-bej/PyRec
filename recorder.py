"""version: 2.0"""
import tkinter as tk
from PIL import ImageTk, Image
import cv2
from cv2 import VideoWriter 
import pyautogui
from win32api import GetSystemMetrics
import numpy as np
from datetime import datetime
import os
from multiprocessing import Process,Manager
from pathlib import Path
def Recorder(ns):
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    dim = (width , height)
    f= cv2.VideoWriter_fourcc(*"XVID")
    video_folder_path = str(Path.home()/"Videos")
    defaultVdName = f"{video_folder_path}\\PyRec\\new.mp4"
    defaultVdName = r"{}".format(defaultVdName)
    output = VideoWriter(defaultVdName,f,15.0,dim)
    while ns.k:
        image = pyautogui.screenshot()
        frame_1 = np.array(image)
        frame = cv2.cvtColor(frame_1,cv2.COLOR_BGR2RGB)
        output.write(frame)
    output.release()
def MakeWindow(ns):
    video_folder_path = str(Path.home()/"Videos")
    #functions
    def recStart():
        if ns.k:
            txt.set("RECORDER IS BUSY")
            headText.configure(fg='yellow')
            start_bt.configure(bg='red')
        else:
            txt.set("RECORDING STARTED....")
            headText.configure(fg='yellow')
            start_bt.configure(bg='green')
            global vdName
            vdName = datetime.now().strftime("%b-%d-%Y-%H-%M-%S")
            vdName = f"{video_folder_path}\\PyRec\\{vdName}.mp4"
            vdName = r'{}'.format(vdName)
            global rec
            rec = Process(name="recorder",target=Recorder, args=(ns,))
            ns.k = True
            rec.start()
    def recStop():
        defaultVdName = f"{video_folder_path}\\PyRec\\new.mp4"
        defaultVdName = r"{}".format(defaultVdName)
        headText.configure(fg='green')
        start_bt.configure(bg='grey')
        ns.k = False
        rec.join()
        os.rename(defaultVdName,vdName)
        txt.set("RECORDING SUCCESSFULLY SAVED-at:\n"+vdName)
    def srcTaken():
        defaultImgName = video_folder_path+"\\PyRec\\new.png"
        defaultImgName = r'{}'.format(defaultImgName)
        headText.configure(fg='green')
        imName = datetime.now().strftime("%b-%d-%Y-%H-%M-%S")
        imName = f"{video_folder_path}\\PyRec\\{imName}.png"
        imName = r'{}'.format(imName)
        scShot = pyautogui.screenshot()
        scShot = cv2.cvtColor(np.array(scShot),cv2.COLOR_BGR2RGB)
        cv2.imwrite(defaultImgName,scShot)
        os.rename(defaultImgName,imName)
        txt.set("SCREENSHOT SUCCESSFULLY SAVED-at:\n"+imName)
    #making the controlling window
    startImage = Image.open('start1.png')
    startImage = startImage.resize((100, 100), Image.ANTIALIAS)
    stopImage = Image.open('stop1.1.png')
    stopImage = stopImage.resize((100, 100), Image.ANTIALIAS)
    srcImage = Image.open('screenshot.png')
    srcImage = srcImage.resize((100, 100), Image.ANTIALIAS)
    root = tk.Tk()
    root.geometry('470x330') # max width = 490 st 450 heigh = 580 st=550 , min height = 330 width = 300
    root.maxsize(490,330)
    root.minsize(420,330)
    root.title("SCREEN RECORDER")
    txt = tk.StringVar()
    txt.set("HI THIS IS A SCREEN RECORDER")
    mF = tk.Frame(root,bg="grey")
    mF.pack(side=tk.RIGHT,fill=tk.Y)
    f1 = tk.Frame(root,bg='Black',borderwidth=6,relief=tk.SUNKEN)
    f1.pack(side=tk.LEFT,fill='y')
    headText = tk.Label(f1,textvariable= txt,bg='black',fg='red',padx=100,borderwidth=5)
    headText.pack(fill=tk.Y)
    strtimge = ImageTk.PhotoImage(startImage)
    stpimge = ImageTk.PhotoImage(stopImage)
    scrshotimge = ImageTk.PhotoImage(srcImage)
    start_bt = tk.Button(mF,image=strtimge,fg='black',bg='grey',command=recStart,border='0')
    end_bt = tk.Button(mF,image=stpimge,fg='black',bg='grey',command=recStop,border='0')
    srShot_bt = tk.Button(mF,image=scrshotimge,fg='black',bg='grey',command=srcTaken,border='0')
    start_bt.pack(side=tk.TOP,padx=4,pady=4)
    end_bt.pack(side=tk.TOP,padx=4,pady=4)
    srShot_bt.pack(side=tk.TOP,padx=4,pady=4)
    root.mainloop()
def managePyRecFolder():
    video_folder_path = str(Path.home()/"Videos")
    os.chdir(video_folder_path)
    if "PyRec" not in os.listdir():
        os.mkdir("PyRec")
if __name__ == '__main__':
    mng_folder_p = Process(name="folder manager",target=managePyRecFolder)
    mng_folder_p.start()
    mng_folder_p.join()
    mgr = Manager()
    ns = mgr.Namespace()
    ns.k = False
    mkw = Process(name="window_controller",target=MakeWindow,args=(ns,))
    mkw.start()
    mkw.join()