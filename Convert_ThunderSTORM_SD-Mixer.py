import numpy as np
from tkinter.filedialog import askopenfilenames
from tkinter import *
from tkinter import IntVar
from os import path
from os import makedirs11
import pandas as pd
from csv import writer
from csv import reader




###############get Files
root = Tk()
PathList = askopenfilenames(filetypes=(("CSV", "*.csv"),("Text files", "*.txt"),
                                           ("All files", "*.*") ))
root.destroy()


files=[]
for thisfile in PathList:
    folder, file = path.split(thisfile)
    files=files+[file]
    
folder=folder+"/"
    
    
##############get Pixelsize of original Image   

from tkinter import *

def show_entry_fields():
    global PixSize
    PixSize=e1.get()
    master.destroy()

master = Tk()
master.title("ThunderSTORM csv to SD-Mixer")
Label(master, text="Enter Pixelsize \n of original Image (nm)").grid(row=0)
Label(master, text="niclas.gimber@charite.de").grid(row=4, column=1)
e1 = Entry(master)
e1.grid(row=0, column=1)
Button(master, text='Convert ThunderSTORM .csv \n for SD-Mixer', command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=4)
mainloop()

PixSize=float(PixSize)



################define convertion function
def ThunderToDemix(folder,inputfile,PixSize):
    thunderCSV=pd.read_csv(folder+inputfile)
    xy=thunderCSV[["x [nm]","y [nm]"]]
    xy.columns=["x[nm]","y[nm]"]
    s=thunderCSV[["sigma [nm]"]]/PixSize
    s.columns=["sigma"]
    i_f=thunderCSV[["intensity [photon]","frame"]]
    i_f.columns=["intensity","frame"]
    thunderCSV.reset_index()
    xy.reset_index()
    saveMe=pd.concat([xy,thunderCSV[["frame"]],thunderCSV[["intensity [photon]"]],s,thunderCSV.drop(['id',"intensity [photon]","frame"], 1)], axis=1)
    
    saveMe=saveMe.round(3)#reduce size

    #####create header

    blankHead="# <localizations><field identifier=\"Position-0-0\" min=\"0 m\" max=\"xmax m\" /><field identifier=\"Position-1-0\" min=\"0 m\" max=\"ymax m\" /><field identifier=\"ImageNumber-0-0\" /><field identifier=\"Amplitude-0-0\" /></localizations>"

    xmax=str(saveMe["x[nm]"].max()/1000000000)
    ymax=str(saveMe["y[nm]"].max()/1000000000/2)

    blankHead=blankHead.replace("xmax",xmax).replace("ymax",ymax)


    #### save file
    newPath=folder+"/SD-Mixer_input"
    if (path.exists(newPath)==False):
        makedirs(newPath)

    name=newPath+"/SDMixInput_"+inputfile[0:-4]+".txt"
    saveMe[saveMe.columns[0:4].tolist()].to_csv(name, index=False,header=False,sep=" ")
    pd.DataFrame(["Pixel Size = "+str(PixSize)+"nm"]).to_csv(newPath+"/log.txt", index=False,header=False,sep=" ")

    ####add header
    with open(name,newline='') as f:
        r = reader(f)
        data = [line for line in r]
    with open(name,'w',newline='') as f:
        w = writer(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='',escapechar='\\')
        w.writerow([blankHead])
        w.writerows(data) 
    
    
    return (saveMe)
        
    
    
    
###############batch processing    

for i in files:
    inputfile=i
    ThunderToDemix(folder,inputfile,PixSize)

