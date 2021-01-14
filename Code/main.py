#!/usr/bin/python
# -*- coding: utf-8 -*-
#special thanks to bhupender


import cv2
import os
import numpy as np
subjects = ["", "nagaraju", "bhupender","samiksha"]

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Binary data
    
    #x='dataset/'+str(image_path)+'.npy'
    #y='dataset/'+str(image_path)+'.txt'
    #np.save(x, gray)
    #Human readable data
    #np.savetxt(y, gray)
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]
def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue;
        label = int(dir_name.replace("s", ""))
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue;
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            face, rect = detect_face(image)
            if face is not None:
                faces.append(face)
                labels.append(label)
            
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels

print("Preparing data...")
count=1

faces, labels = prepare_training_data("training-data")
print("Data prepared")
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.train(faces, np.array(labels))
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)
    label, confidence = face_recognizer.predict(face)
    label_text = subjects[label]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    return label_text



def check(name):
    print("Look at the camera")
    count=0
    import cap

    cap.TakeSnapshotAndSave()
    test_img1 = cv2.imread("test1.jpg")
    test_img2 = cv2.imread("test2.jpg")
    test_img3 = cv2.imread("test3.jpg")
    test_img4 = cv2.imread("test4.jpg")
    x=0
    y=0
    z=0
    w=0
    try:
        x = predict(test_img1)
    except:
        print(" ")
    try:
        y = predict(test_img2)
    except:
        print(" ")
    try:
        z = predict(test_img3)
    except:
        print(" ")
    try:
        w = predict(test_img4)
    except:
        print(" ")
    finally:
        if(x==name):
            count=count+1
        if(y==name):
            count=count+1
        if(z==name):
            count=count+1
        if(w==name):
            count=count+1
        if(count>1):
            return 1
        else:
            return 0


  


def update(last):
    file = open("database.csv","r")
    fileop= open("new.csv","w")
    updated= last.split(",")
    fileop.write(file.readline())
    new = file.readline()
    while new != '':
        store = new.split(",")
        if store[0]==updated[0]:
            fileop.write(last)
            new = file.readline()
        else:
            fileop.write(new)
            store.clear()
            new = file.readline()
    file.close()
    fileop.close()
    fileop = open("database.csv","w")
    fileip= open("new.csv","r")
    #new=fileip.readline()
    #while new != '':
     #   fileop.write(new)
      #  new=fileip.readline()
    new = fileip.read()
    fileop.write(new)
    fileip.close()
    fileop.close()
    


def withdrawl(data):
    amount=int(input("Enter the amount to Withdrawl:"))
    print("verify your facial ID")
    #from fr import check
    val=check(data[0])
    if(val==0):
        print("ID Not Verified!! Try again")
        return 0
    else:
        print("ID verified")
    if int(data[2])>amount:
        data[2]=int(data[2])-amount
        print("Amount Withdrawl\nTotal Amount={}".format(data[2]))
        string = str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3])+","+str(data[4])+"\n"
        update(string)
        return 1
    else:
        print("Not Enough Balance")
        return 0




def deposit(data):
    amount=int(input("Enter the amount to Deposit:"))
    #from fr import check
    val=check(data[0])
    if(val==0):
        print("ID Not Verified!! Try again")
        return 0
    else:
        print("ID verified")
    data[2]=int(data[2])+amount
    print("Amount Deposited\nTotal Amount={}".format(data[2]))
    string = str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3])+","+str(data[4])+"\n"
    update(string)



def credit(data,amount):
    data[2]=int(data[2])+amount
    string = str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3])+","+str(data[4])+"\n"
    update(string)





def debit(data,amount):
    if int(data[2])>amount:
        data[2]=int(data[2])-amount
        print("Amount Transferred\nTotal Amount={}".format(data[2]))
        string = str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3])+","+str(data[4])+"\n"
        update(string)
        return 1
    else:
        print("Not Enough Balance")
        return 0
    
    

def transfer(data):
    file = open("database.csv","r")
    phone=input("Enter the Phone number to send money:")
    phone=(phone+"\n")
    amount=int(input("Enter Amount"))
    #from fr import check
    val=check(data[0])
    if(val==0):
        print("ID Not Verified!! Try again")
        return 0
    else:
        print("ID verified")
    flag=0
    new=file.readline()
    while new != '':
        store = new.split(",")
        if store[-1]==phone:
            flag=1
            if debit(data,amount):
                credit(store,amount)
            else:
                print("Unable to Transfer")
        new=file.readline()
                
    if(flag==0):
        print("Phone not exist in database")
    file.close()
        
    
    






def transaction(data):
    print("Your Account Balance is:{}".format(data[2]))
    logout=1
    while(logout):
        choice=int(input("Enter Your choice\n0.Show Data\n1.Deposit\n2.Withdrawl\n3.Change Phone number\n4.Change Email Address\n5.Change Password\n6.MONEY TRANSFER\n7.Logout\n:"))
        if(choice==0):
            print("Amount={}\nPassword={}\nEmail={}\nPhone number={}\n".format(data[2],data[1],data[3],data[4]))
        elif(choice==1):
            deposit(data)
        elif(choice==2):
            withdrawl(data)
        elif(choice==3):
            phone=int(input("Enter the Phone Number:"))
            data[4]=phone
            string = str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3])+","+str(data[4])+"\n"
            update(string)
        elif(choice==4):
            email=input("Enter the Email Address:")
            data[3]=email
            string = str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3])+","+str(data[4])+"\n"
            update(string)
        elif(choice==5):
            password=input("Enter the New Password:")
            data[1]=password
            string = str(data[0])+","+str(data[1])+","+str(data[2])+","+str(data[3])+","+str(data[4])+"\n"
            update(string)
        elif(choice==6):
            transfer(data)
        elif(choice==7):
            logout=0
            print("logout Suceessfully")
        else:
            print("Invalid Choice")
            








def startprog(data):
    i=3
    while(i>0):
        gen=check(data[0])
        if gen==1:
            print("Login Successful")
            transaction(data)
            break
        else:
            print("Invalid face")
        i=i-1
    







#initial
def atm():
    choice='y'
    while choice =='Y' or choice=='y':
        flag=0
        login=input("enter the login id:")
        password=input("enter the password:")
        file_ip = open("database.csv","r")
        #variable new contains every new line scanned fron the file
        new = file_ip.readline()
        new = file_ip.readline()
        while new != '':
                    data = new.split(",")
                    if data[0]==login and data[1]==password:
                        flag=1
                        break
                    else:
                        data.clear()
                    new = file_ip.readline()
        file_ip.close()
        if flag==1:
            print("Login details matched")
            startprog(data)
            #print(data)
            choice=0
            choice=input("Type 'Y' for reLogin:")
        else:
            choice=input("Invalid input!!try again?  type 'Y' for reenter:")

            
atm()







