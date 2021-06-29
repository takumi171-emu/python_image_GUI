from tkinter import * 
from tkinter import ttk
import numpy as np
from PIL import ImageTk, Image
import tkinter.filedialog 
import os
import cv2



class img(tkinter.Frame):
   
    def __init__(self, master):
        super().__init__(master, height=800, width=1200)
        self.pack()
        self.create_widgets()
        self.img_tk = None
        self.cv_file= None
        self.savefile = None
    
    def create_widgets(self):
        
        menubar = tkinter.Menu(self)
        menu1 = tkinter.Menu(menubar,tearoff=False)
        menu1.add_command(label="open", command=self.load_file)
        menu1.add_command(label="save", command=self.save_img)
        menubar.add_cascade(label='File',menu=menu1)
        self.master["menu"] = menubar 

        
        img_frame = tkinter.Frame(self, width=640, height=480)
        img_frame.propagate(False)
        img_frame.place(x=100,y=50)
        b_menu_frame = tkinter.Frame(self, width=300, height=480)
        b_menu_frame.propagate(False)
        b_menu_frame.place(x=800, y=50)
        log_frame = tkinter.Frame(self, width=640, height= 100)
        log_frame.propagate(False)
        log_frame.place(x=100, y=650)

        image_yscrollbar = tkinter.Scrollbar(img_frame)
        image_yscrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
        image_xscrollbar = tkinter.Scrollbar(img_frame,orient=tkinter.HORIZONTAL)
        image_xscrollbar.pack(side=tkinter.BOTTOM,fill=tkinter.X)
        self.image_canvas = tkinter.Canvas(img_frame,\
        xscrollcommand=image_xscrollbar.set,yscrollcommand=image_yscrollbar.set)
        self.image_canvas.pack(side=tkinter.TOP, fill=tkinter.BOTH)
        image_xscrollbar["command"] =self.image_canvas.xview
        image_yscrollbar["command"] =self.image_canvas.yview
        
        thre_button = tkinter.Button(b_menu_frame , text='二値化（THRESHOLD_BINARY）')
        thre_button.bind('<Button-1>', imgthrashhold)
        thre_button.pack(fill = 'x', padx=10)

        mos_button = tkinter.Button(b_menu_frame, text='モザイク')
        mos_button.bind('<Button-1>', imgMosaic)
        mos_button.pack(fill = 'x', padx=10)

        orign_button = tkinter.Button(b_menu_frame , text='元の画像')
        orign_button.bind('<Button-1>', orginalimg)
        orign_button.pack(fill = 'x', padx=10)

    def load_file(self):

        ftype = [("", "*")]
        idir = "D:\PythonScripts"
    
        file_path = tkinter.filedialog.askopenfilename(filetypes=ftype, initialdir=idir)
        
        img = cv2.imread(file_path)
        
        img = cv2.resize(img, dsize=(640,480))
        self.cv_file = img.copy()
        img_tk = cv2pillow(img)
       
        w = img_tk.width()
        h = img_tk.height()
        self.image_on_canvas = self.image_canvas.create_image(0,0,image=img_tk,anchor='nw')

        self.image_canvas.config(width=w, height=h, scrollregion=(0,0,w,h))
        self.img_tk = img_tk

    def save_img(self):
        img = self.savefile
        print(img)
        savepath = tkinter.filedialog.asksaveasfilename()
        img.save(savepath + ".jpg")
        
        
def imgthrashhold(event):
         
         src = app.cv_file.copy()
         
         dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
         _, dst_thre = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)
         
         dst_im = dst_thre.copy()
        
         dst_ = Image.fromarray(dst_im)
         set_img(event, dst_)

def  orginalimg(event):
     
     src = app.cv_file
     src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
     dst_ = Image.fromarray(src)
     set_img(event, dst_)

def mosaic(src, ratio=0.1):
  dst = cv2.resize(src, dsize=None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
  return cv2.resize(dst, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def imgMosaic(event):
    
    dst = app.cv_file.copy()
    dst = mosaic(dst)
    dst_ = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    dst_mos = Image.fromarray(dst_)
    set_img(event, dst_mos)

         
def set_img(event, img):
    app.savefile = img
    app.img_tk = ImageTk.PhotoImage(img)
    app.image_canvas.itemconfig(app.image_on_canvas, image= app.img_tk)



def cv2pillow(img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        return img_tk


root = Tk()
app = img(root)
    
app.mainloop()