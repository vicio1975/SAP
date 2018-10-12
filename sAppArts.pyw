# -*- coding: utf-8 -*-
"""
Created on Mon May  7 12:34:13 2018
@author: VS
"""
from tkinter import  *
from tkinter import  filedialog
from tkinter import  messagebox
from tkinter import scrolledtext
import re
#Fonts
f_8 = ("arial",8)
f_9 = ("arial",9)
f_10 = ("arial",10)
f_9b = ("arial",9,"bold")

root = Tk()
DIC={}
root.geometry("750x330+100+50")
root.title("CAD part name in SAP")
root.resizable(width=False, height=False)

EX = False

def mfile():

    file1 = filedialog.askopenfile()
    file1_ = file1.name

    if file1 is None:
        return 999

    f = open(file1_,"r+")
    text_ex = {}
    for lines in f.readlines():
        l,val = re.split('; |, |:',lines)

        l = l.strip("\t")
        l = l.strip("\n")
        l = l.strip(" ")

        val = val.strip("\n")
        val = val.strip("\t")
        val = val.strip(" ")

        l   = str(l).lower()
        val = str(val).lower()
        print(l," - ",val)
        text_ex[l] = val
    global EX, DIC
    EX = True
    DIC = text_ex
    f.close()
    if DIC != {}:
        messagebox.showwarning("Warning","Any previous list will be deleted!\n Accepted delimiters '; , :' ")

    
def ins(p1,p2):
    global DIC
    p1_ = p1.get()
    p1_ = str(p1_).lower()
    p2_ = p2.get()
    p2_ = str(p2_).lower()

    DIC_lab = p1_ 
    DIC_val = p2_
    DIC[DIC_lab] = DIC_val
   
def SH(DIC):

    if DIC != {}:
        global frameT
        frameT = Frame(root, width=100, height=100,bg='grey',
                       borderwidth=2, relief="ridge") #fill='both', expand='yes'
        frameT.place(x=270, y=43)
        editArea = scrolledtext.ScrolledText(
            master = frameT,
            wrap   = WORD,
            width  = 52,
            height = 16
        )

        editArea.pack(padx=5, pady=5, fill="both", expand=True)
        #Creation of the lists!
        textList = ""
        textListSAP = ""
        textAll = ""
        i = 0
        for key,val in DIC.items():
            textList = "{:<28s}".format(key)    
            textListSAP = "{:<25s}".format(val)    
            line = "{:4s}|{:s} ".format(str(i)," "*3) + textList + "|{:s} ".format(" "*2) + textListSAP
            textAll += line + "\n" 
            i += 1
        editArea.insert(INSERT,textAll)

    elif DIC == {}:
        messagebox.showwarning("Warning","There is not a parts' list!")
        frameTT = Frame(root, width=100, height=100,
                       borderwidth=2, relief="ridge") #fill='both', expand='yes'
        frameTT.place(x=270, y=43)
        editArea2 = scrolledtext.ScrolledText(
            master = frameTT,
            wrap   = WORD,
            width  = 52,
            height = 16
        )

        editArea2.pack(padx=5, pady=5, fill="both", expand=True)
        #Creation of the lists!
        textList = " "
        editArea.insert(INSERT,textList )

def fsave(DIC):
    if DIC != {}:
        file1 = filedialog.asksaveasfile(mode="w",defaultextension=".txt")
        textS = ""    
        if file1 is None:
            return
        for key,val in DIC.items():
            textS += "{} : {}\n".format(key,val)    
        file1.write(textS)
        file1.close()
    if DIC == {}:
        messagebox.showwarning("Warning","Please select a List or create a new one")

#Delete Dictionary
def DL():
    global DIC    
    if DIC == {}:
        messagebox.showinfo("Warning","No list to delete!")
        
    if DIC != {}:   
        DIC = {}
        frameT.grid_remove()

#find a value
def codeF(p3):
    if DIC != {}:
        p3_ = p3.get()
        p3_ = str(p3_).lower()
        #print(p3_)
        res = [DIC[i] for i,j in DIC.items() if i==p3_]
        #print(res)
        if res == []:
            messagebox.showinfo("Info","The part is not in the list!!")
        lab4 =  Label(root,text=res[0],font=f_9,bg="white",width=20,fg="red", borderwidth=1, relief="ridge")
        lab4.grid(row=12,column=1,sticky=N)
        
    if DIC == {}:
        messagebox.showwarning("Warning","Please select a List or create a new one")


#############>>> MAIN
###       
lab0 =  Label(root,text=". New Part/Assy .",font=f_9b)
lab0.grid(row=1,column=1,sticky=N,pady=2)
lab01 =  Label(root,text=".___________________________________________________________________.",font=f_9b)
lab01.place(x=255, y=16)
lab00 =  Label(root,text="Num.{:s}Part/Assy Name{:s}SAP Name".format(" "*20," "*50),font=f_9b)
lab00.place(x=264, y=9)
frameLIST = Frame(root, width=469, height=280,
               borderwidth=1, relief="ridge")
frameLIST.place(x=260, y=40)
##Input
lab1 =  Label(root,text="Part Name:",font=f_9)
lab1.grid(row=2,column=0,sticky=E)
p1 = StringVar()
e1 = Entry(root,textvariable=p1, width=20,justify="center",font=f_9)
e1.grid(row=2,column=1,sticky=W)
e1.insert(END, "max 20 characters")
#
lab2 =  Label(root,text="SAP Name:",font=f_9)
lab2.grid(row=3,column=0,sticky=E)
p2 = StringVar()
e2 = Entry(root,textvariable=p2, width=20,justify="center",font=f_9)
e2.grid(row=3,column=1,sticky=W)
e2.insert(END, " - ")

##actions on a list
b1 = Button(root,text="Update list",width=19,command=lambda:ins(p1,p2))
b1.grid(row=4,column=1,sticky=W)
b2 = Button(root,text='Show List',width=19, command=lambda:SH(DIC),font=f_9)
b2.grid(row=5,column=1,sticky=W)
b3 = Button(root,text='Delete List',width=19, command=DL,font=f_9)
b3.grid(row=6,column=1,sticky=W)

#Looking for a part
lab3_00 =  Label(root,text=". Find Part/Assy .",font=f_9b)
lab3_00.grid(row=10,column=1,sticky=N,pady=2)
lab3_0 =  Label(root,text=" ",font=f_9)
lab3_0.grid(row=10,column=1,sticky=W)

lab3 =  Label(root,text="Find Part Name:",font=f_9)
lab3.grid(row=11,column=0,sticky=E)
p3 = StringVar()
e3 = Entry(root,textvariable=p3, width=23,justify="center")
e3.grid(row=11,column=1,sticky=W)
e3.insert(END, "Name")

lab3_1 =  Label(root,text="SAP part name:",font=f_9)
lab3_1.grid(row=12,column=0,sticky=E)
lab3_2 =  Label(root,text=" ",font=f_9,justify="center",
    bg="white",width=20,fg="red", borderwidth=1, relief="ridge")
lab3_2.grid(row=12,column=1,sticky=W)

##Actions in frame
b4 = Button(root,text="Find Part Code",width=19,command=lambda:codeF(p3))
b4.grid(row=13,column=1,sticky=W)
b401 =  Label(root,text="_________",font=f_9b,pady=2)
b401.grid(row=14,column=1,sticky=N)
b5 = Button(root,text="Save List",width=19,command=lambda:fsave(DIC))
b5.grid(row=15,column=1,sticky=W,rowspan=1)
b6 = Button(root,text="EXIT",width=19,command=root.destroy)
b6.grid(row=16,column=1,sticky=W)


#list of menu1
list1 = Menu()
list1.add_command(label="Open List",command=mfile)
list1.add_command(label="Save List",command=lambda:fsave(DIC))
list1.add_command(label="Exit",command=root.destroy)

#menu1
menu1 = Menu()
menu1.add_cascade(label="Options",menu=list1) 
root.config(menu=menu1)

root.mainloop()