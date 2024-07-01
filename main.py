import cv2
import face_recognition
import os,sys
import numpy as np
import math
from tkinter import messagebox
import loginInterface as li
import shutil
import time
from datetime import datetime
import csv
def face_confidence(face_distance,face_match_threshold=0.6):#checking for face tolerance and approximating matching percentage
    range=(1.0-face_match_threshold)
    linear_val=(1.0-face_distance)/(range*2.0)
    if face_distance>face_match_threshold:
        return str(round(linear_val*100,2))+'%'
    else:
        value=(linear_val+((1.0-linear_val)*math.pow((linear_val-0.5)*2,0.2)))*100
        return str(round(value,2))+'%'
def show_message_box():#function to show login successful
    dummy=li.uname
    messagebox.showinfo("Login Status", "Login Successful\n"+ dummy.upper()+ " of SPINTEG\n"+"DATE:"+ current_date+"\n"+"TIME:"+current_timer)



class FaceRecognition:#attributes of the face recognition
    face_locations=[]
    face_encodings=[]
    face_names=[]
    known_face_encoding=[]
    known_face_names=[]
    process_current_frame=True
    def __init__(self):
        self.encode_faces()
    def encode_faces(self):#fetches the image from known people folder which has the face to be rcognised by the program
        for image in os.listdir('known_people'):
            face_image=face_recognition.load_image_file(f'known_people/{image}')
            face_encoding=face_recognition.face_encodings(face_image)[0]
            self.known_face_encoding.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)
    def run_recognition(self):#starting the face recognition

        video_capture=cv2.VideoCapture(0)#the argument for this funtion depend on which camera you to use ,for default use 0. For external use 1,2,etc
        if not video_capture.isOpened():
            sys.exit('video source not found...')
        start = time.time()
        while time.time() - start < 120:#running the loop for 120 second(2 minutes) because the login needs to expire if no match is found
            ret,frame=video_capture.read()#starting to recognise the face in camera
            if self.process_current_frame:
                small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                self.face_locations=face_recognition.face_locations(rgb_small_frame)
                self.face_encodings=face_recognition.face_encodings(rgb_small_frame,self.face_locations)
                self.face_names=[]

                for face_encoding in self.face_encodings:

                    matches=face_recognition.compare_faces(self.known_face_encoding,face_encoding)
                    name='Unknown'
                    confidence='Unknown'
                    face_distances=face_recognition.face_distance(self.known_face_encoding,face_encoding)
                    best_match_index= np.argmin(face_distances)
                    if matches[best_match_index]:#match is found start, implementing the matching process
                        name=self.known_face_names[best_match_index]
                        confidence=face_confidence(face_distances[best_match_index])
                        self.face_names.append(f'{name}({confidence})')
                        video_capture.release()#stop the camera reading after match is found
                        employees = self.known_face_names.copy()#creating a copy of known face _face names
                        self.face_names.append(name)
                        if name in self.known_face_names:
                            if name in employees:
                                employees.remove(name)
                                print(employees)
                                current_time = now.strftime("%H-%M-%S")
                                lnwriter.writerow([li.uname, current_time])#writing the name of the employee and time he logged in
                        folder = 'known_people'
                        for filename in os.listdir(folder):#deleting employee face form the known_people folder after the matching is complete
                            file_path = os.path.join(folder, filename)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                print('Failed to delete %s. Reason: %s' % (file_path, e))
                        cv2.destroyAllWindows()#closing the face recognition Window
                        show_message_box()
                        break


            self.process_current_frame=not self.process_current_frame#creating a frame for the face recognised
            for(top,right,bottom,left),name in zip(self.face_locations,self.face_names):
                top*=4
                right*=4
                bottom*=4
                left*=4
                cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
                cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),-1)
                cv2.putText(frame,name,(left+6,bottom-6),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
                cv2.putText(frame,name,(left+6,bottom-6),cv2.FONT_HERSHEY_DUPLEX,0.8,(255,255,255),1)
            if ret:
                cv2.imshow('face Recognition',frame)
                if cv2.waitKey(1) == ord('q'):#to force quit the program
                    break
            else:
                break
        else:#over the time of 2 minutes
            messagebox.showinfo("Login Status", "Login expired ")
            folder = 'known_people'
            for filename in os.listdir(folder):#deleting the image from known people
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            cv2.destroyAllWindows()#destroying camera window
if __name__=='__main__':

    fr = FaceRecognition()
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")#getting present date
    current_timer=now.strftime("%H-%M-%S")#getting current timer
    f = open(current_date + '.csv', 'a+', newline='')#opening the file object
    lnwriter=csv.writer(f)
    fr.run_recognition()
    f.close()#closing the file object






