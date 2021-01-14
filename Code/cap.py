import numpy as np
import cv2
import time

#import the cascade for face detection
face_cascade =cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
def TakeSnapshotAndSave():
    # access the webcam (every webcam has a number, the default is 0)
    cap = cv2.VideoCapture(0)
    import time
    time.sleep(2)

    num = 1
    while num<5:
        # Capture frame-by-frame
        ret, frame = cap.read()
        time.sleep(0)

        # to detect faces in video
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)


        cv2.imwrite('test'+str(num)+'.jpg',frame)
        num = num+1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    TakeSnapshotAndSave()
