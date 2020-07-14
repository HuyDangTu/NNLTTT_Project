# importing libraries 
import tkinter as tk 
from tkinter import *
import cv2 
import os 
import shutil 
import csv 
import numpy as np 
from PIL import Image, ImageTk 
from tkinter import messagebox
import pandas as pd 
import datetime 
import time 
import tkinter.ttk as ttk 
import tkinter.font as font 
from pathlib import Path 
import csv
import keyboard

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb   

isOpen = True

window = tk.Tk()  
window.geometry("1920x1280")
window.title("Nhận Diện Khuôn Mặt") 
window.configure(background ="white") 
window.grid_rowconfigure(0, weight = 1) 
window.grid_columnconfigure(0, weight = 1) 


img = ImageTk.PhotoImage(Image.open('./button/logo-news.png'))
panel = tk.Label(window, image=img,  bg="white")
panel.pack(side="bottom", fill="both", expand="yes")
panel.place(x=0,y=0)


message = tk.Label( 
    window, text ="ĐIỂM DANH",  
    bg ="white", fg =_from_rgb((246,110,51)), width = 50,  
    height = 3, font = ('helvetica', 28 ,'bold'),anchor="w" )      
message.place(x=50, y=100)

lbl = tk.Label(window, text = "Mã số",  
width = 20, height = 2, fg =_from_rgb((177,209,216)),  
bg = "white", font = ('helvetica', 20 ,'bold'),anchor="w" )  
lbl.place(x = 50, y = 230) 
  
txt = tk.Entry(window,  
width = 27,bg ="white",  
fg ="green", font = ('times', 15, ' bold ')) 
txt.place(x = 200, y = 245) 
  
lbl2 = tk.Label(window, text ="Tên",  
width = 20,fg= _from_rgb((177,209,216)), bg ="white",  
height = 2, font = ('helvetica', 20 ,'bold'),anchor="w")  
lbl2.place(x = 50, y = 330) 
  
txt2 = tk.Entry(window, width = 27,
bg ="white", fg ="green",  
font = ('times', 15, 'bold')) 
txt2.place(x = 200, y = 345)  

#THONG TIN SINH VIEN
message = tk.Label(
    window, text="THÔNG TIN",
    bg="white", fg=_from_rgb((246, 110, 51)), width=50,
    height=3, font=('helvetica', 20, 'bold'), anchor="w")
message.place(x=1280, y=110)

my_string_var_name = tk.StringVar(value="Tên")
my_string_var_id = tk.StringVar(value="MSSV")

lblName = tk.Label(window, textvariable=my_string_var_name,
width=20, height=2, fg=_from_rgb((177, 209, 216)),
bg="white", font=('helvetica', 20, 'bold'), anchor="w")
lblName.pack()
lblName.place(x=1200, y=200)

lblId = tk.Label(window, textvariable=my_string_var_id,
width=20, height=2, fg=_from_rgb((177, 209, 216)),
bg="white", font=('helvetica', 20, 'bold'), anchor="w")
lblId.pack()
lblId.place(x=1200, y=250)

def DisplayInfo(name,id):
    my_string_var_name.set("Tên: "+ name)
    lblName.update_idletasks()
    my_string_var_id.set("MSSV: " + id)
    lblId.update_idletasks()


#Hiển thị camera
frame = tk.Frame(window)
frame.grid()
frame.place(x=510, y=150)
# Create a label in the frame
camera = tk.Label(frame)
camera.grid()

#cap = cv2.VideoCapture(0)
#function for video streaming
# def video_stream():
#     if(isOpen):
#         _, frame = cap.read()
#         cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#         img = Image.fromarray(cv2image)
#         imgtk = ImageTk.PhotoImage(image=img)
#         camera.imgtk = imgtk
#         camera.configure(image=imgtk) 
#         camera.after(1, video_stream) 
#     else:
#         return

# video_stream()

def is_number(s): 
    try: 
        float(s) 
        return True
    except ValueError: 
        pass
    try: 
        import unicodedata 
        unicodedata.numeric(s) 
        return True
    except (TypeError, ValueError): 
        pass
    return False

def TakeImages():          
    Id =(txt.get())  
    name =(txt2.get()) 
      
    if(is_number(Id) and name.isalpha()):  

        cam = cv2.VideoCapture(0)  

        harcascadePath = "data\haarcascade_frontalface_default.xml" 
        detector = cv2.CascadeClassifier(harcascadePath)  
        sampleNum = 0 
        while(True): 
            ret, img = cam.read()  
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5) 
            for (x, y, w, h) in faces:  
                cv2.rectangle(img, (x, y), ( 
                    x + w, y + h), (255, 0, 0), 2)  
                sampleNum = sampleNum + 1
                cv2.imwrite( 
                    "Image\ "+name +"."+Id +'.'+ str( 
                        sampleNum) + ".jpg", gray[y:y + h, x:x + w]) 
                # Hiển thị các hình ảnh đã chụp
                #cv2.imshow('frame', img) 
            # đợi 100 milissecond  
            if cv2.waitKey(0) & 0xFF == ord('q'): 
                break
            # break nếu số tấm hình trên 30 
            elif sampleNum>30: 
                break

        #cam.release()  

        cv2.destroyAllWindows()  

        res = "Hình đã được lưu vào thư mục Image "  
        messagebox.showinfo("Thông báo", res)

        row = [Id, name,'','','','','','']  
        with open('User\CSVfile.csv', 'a+') as csvFile: 
            writer = csv.writer(csvFile) 
  
            writer.writerow(row)

        csvFile.close() 
    else: 
        if(is_number(Id)): 
            res = "Vui lòng Nhập số"
            messagebox.showinfo("Thông báo", res)
           
        if(name.isalpha()): 
            res = "Vui lòng nhập ký tự"
            messagebox.showinfo("Thông báo", res)
      
  
def TrainImages(): 
    # Local Binary Pattern Histogram is an Face Recognizer 
    # algorithm inside OpenCV module used for training the image dataset 
    recognizer = cv2.face.LBPHFaceRecognizer_create()   
    # Specifying the path for HaarCascade file 
    harcascadePath = "data\haarcascade_frontalface_default.xml"
    # creating detector for faces 
    detector = cv2.CascadeClassifier(harcascadePath) 
    # Saving the detected faces in variables  
    faces, Id = getImagesAndLabels("Image")  
    # Saving the trained faces and their respective ID's  
    # in a model named as "trainner.yml". 
    recognizer.train(faces, np.array(Id))      
    recognizer.save("TrainingImageLabel\Trainner.yml")  
    # Displaying the message 
    res = "Đã Train xong"
    messagebox.showinfo("Thông báo", res)
    
def getImagesAndLabels(path): 
    # get the path of all the files in the folder 
    imagePaths =[os.path.join(path, f) for f in os.listdir(path)]  
    faces =[] 
    # creating empty ID list 
    Ids =[] 
    # now looping through all the image paths and loading the 
    # Ids and the images saved in the folder 
    for imagePath in imagePaths: 
        # loading the image and converting it to gray scale 
        pilImage = Image.open(imagePath).convert('L') 
        # Now we are converting the PIL image into numpy array 
        imageNp = np.array(pilImage, 'uint8') 
        # getting the Id from the image 
        Id = int(os.path.split(imagePath)[-1].split(".")[1]) 
        # extract the face from the training image sample 
        faces.append(imageNp) 
        Ids.append(Id)         
    return faces, Ids 
# For testing phase 
def TrackImages(): 
    recognizer = cv2.face.LBPHFaceRecognizer_create() 
    # Reading the trained model 
    recognizer.read("TrainingImageLabel\Trainner.yml")  
    harcascadePath = "data\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath) 
    # getting the name from "userdetails.csv" 
    df = pd.read_csv("User\CSVfile.csv")   
    cam = cv2.VideoCapture(0) 
    font = cv2.FONT_HERSHEY_SIMPLEX         
    while True: 
        ret, im = cam.read() 
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)     
        for(x, y, w, h) in faces: 
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2) 
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])                                    
            if(conf < 50): 
                aa = df.loc[df['Id'] == Id]['Name'].values 
                tt = str(Id)+"-"+aa
            else: 
                Id ='Unknown'                
                tt = str(Id)   
            if(conf > 75): 
                noOfFile = len(os.listdir("ImageUnknown"))+1
                cv2.imwrite("ImageUnknown\Image"+ 
                str(noOfFile) + ".jpg", im[y:y + h, x:x + w])             
            cv2.putText(im, str(tt), (x, y + h),  
            font, 1, (255, 255, 255), 2)         
        cv2.imshow('im', im)  
        if (cv2.waitKey(1)== ord('q')): 
            break
        if(isOpen == False):
            break
    cam.release() 
    cv2.destroyAllWindows() 

def WriteFile(id):
    list=[]
    # Chạy for tìm vị trí cột của ngày hôm nay lưu vào biến x                                                                                                                                                                                                          
    with open('User\CSVfile.csv', 'rt',encoding='utf-8') as in_file:
        x = str(datetime.datetime.now().strftime("%x"))
        reader = csv.reader(in_file)
        list.extend(reader)
        index = 0
        for row in list:
            for i in range(2,5):
                if(str(row[i]).strip() == x.strip()):
                    count = 0
                    for row in list:
                        if(row[0].strip() == str(id)):
                            if(row[i].strip()=='x'):
                                return 'Already Checked'
                            else:
                                row[i] = 'x'
                                line_to_override = {count:row}
                                with open('User\CSVfile.csv', 'w',encoding='utf-8') as out_file:
                                    writer = csv.writer(out_file, delimiter=',', lineterminator='\n')
                                    for line, row in enumerate(list):
                                        data = line_to_override.get(line,row)
                                        writer.writerow(data)
                                return 'Successfully'
                        count = count+1   
            break

def DisplaySheet():
    isOpen = False
    root = tk.Tk()
    root.title('Danh sách điểm danh')
    with open("User/CSVfile.csv", newline="") as file:
        reader = csv.reader(file)
        # r and c tell us where to grid the labels
        r = 0
        for col in reader:
            c = 0
            for row in col:
                label = tk.Label(root, width=10, height=2, text = row, relief = tk.RIDGE)
                label.grid(row = r, column = c)
                c += 1
            r += 1
    root.mainloop()

def Absence(): 
    recognizer = cv2.face.LBPHFaceRecognizer_create() 
    # Reading the trained model 
    recognizer.read("TrainingImageLabel\Trainner.yml")  
    harcascadePath = "data\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath) 
    # getting the name from "userdetails.csv" 
    df = pd.read_csv("User\CSVfile.csv")  
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    isBreak = False         
    while True: 
        #ret, im = cam.read()
        _, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5) 
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if(conf < 50):
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id) + '-' + str(WriteFile(Id))
                DisplayInfo(str(aa[0]), str(Id))
            else:
                tt = 'Please try again'
                print(tt)

            cv2.putText(frame, str(tt), (x, y + h),font, 1, (255, 255, 255), 2)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        camera.imgtk = imgtk
        camera.configure(image=imgtk) 
        # if key 'q' is pressed
        if keyboard.is_pressed('q'):
            # finishing the loop
            print('You Pressed A Key!')
            break 

    cam.release()
    cv2.destroyAllWindows()

        # for(x, y, w, h) in faces: 
        #     cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2) 
        #     Id, conf = recognizer.predict(gray[y:y + h, x:x + w])                                    
        #     if(conf < 50): 
        #         aa = df.loc[df['Id'] == Id]['Name'].values 
        #         tt = str(Id) +'-'+ str(WriteFile(Id))
        #         DisplayInfo(str(aa[0]),str(Id))
        #     else:               
        #         tt = str('Please try again')
                
        #     cv2.putText(im, str(tt), (x, y + h),  
        #     font, 1, (255, 255, 255), 2)
        # cv2.imshow('im', im)
        # if (cv2.waitKey(1)== ord('q')):
        #     break
    # cam.release() 
    # cv2.destroyAllWindows() 
    
sampleButton = PhotoImage(file ='button/ChupAnhButton.png')
trainButton = PhotoImage(file ='button/updateButton.png')
testButton = PhotoImage(file ='button/DDButton.png')
exitButton = PhotoImage(file ='button/ExitButton.png')
DiemDanhBTN = PhotoImage(file='button/DiemDanhBTN.png')

takeImg = tk.Button(window,command = TakeImages,image=sampleButton, borderwidth=0) 
takeImg.place(x = 50, y = 430) 

trainImg = tk.Button(window,command = TrainImages,image=trainButton,borderwidth=0) 
trainImg.place(x = 300, y = 430) 

# trackImg = tk.Button(window,command = TrackImages,image=testButton,borderwidth=0) 
# trackImg.place(x = 50, y = 555) 

# quitWindow = tk.Button(window,command =  window.destroy,image=exitButton, borderwidth=0) 
# quitWindow.place(x = 50, y = 450) 

absence = tk.Button(window, command=Absence, image=DiemDanhBTN, borderwidth=0)
absence.place(x = 500, y = 680) 

absence = tk.Button(window, command=DisplaySheet,image=DiemDanhBTN, borderwidth=0)
absence.place(x=700, y=680)

absence = tk.Button(window, command=window.destroy, image=exitButton, borderwidth=0)
absence.place(x=900, y=680)

window.mainloop() 
