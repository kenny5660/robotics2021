import cv2
import numpy as np

low = np.array((0,0,70), np.uint8)
high = np.array((180,61,250), np.uint8)

def g_count(img):
    l = np.array((0,0,70), np.uint8)
    h = np.array((180,61,250), np.uint8)
    mask = cv2.inRange(img,l,h) 
    count = cv2.countNonZero(mask)
    print(count, ":g ")

    return count


def b_count(img):
    l = np.array((94,128,64), np.uint8)
    h = np.array((114,255,255), np.uint8)
    mask = cv2.inRange(img,l,h) 
    count = cv2.countNonZero(mask)
    print(count, ":b ")
 
    return count

def y_count(img):
    l = np.array((10,200,20), np.uint8)
    h = np.array((28,255,255), np.uint8)
    mask = cv2.inRange(img,l,h) 
    count = cv2.countNonZero(mask)
    print(count, ":y ")

    return count


def low_change_h(x):
    low[0] = x

def low_change_s(x):
    low[1] = x

def low_change_v(x):
    low[2] = x

def high_change_h(x):
    high[0] = x

def high_change_s(x):
    high[1] = x

def high_change_v(x):
    high[2] = x


def fun():
    cv2.namedWindow("test")
    cap = cv2.VideoCapture(0)
    cv2.createTrackbar("l_h","test", low[0], 180, low_change_h)
    cv2.createTrackbar("l_s","test", low[1], 255, low_change_s)
    cv2.createTrackbar("l_v","test", low[2], 255, low_change_v)
    cv2.createTrackbar("h_h","test", high[0], 180, high_change_h)
    cv2.createTrackbar("h_s","test", high[1], 255, high_change_s)
    cv2.createTrackbar("h_v","test", high[2], 255, high_change_v)
    
    while True:
        flag, img = cap.read()
        
        try:
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(img_hsv,low,high) 
            

            cv2.imshow('test',mask)
        except:
            cap.release()
            raise
        ch = cv2.waitKey(5)
        if (ch == 27):
            break
        if (ch == ord('a')):
            low[0]+= 5
    cap.release()
    cv2.destroyAllWindows()

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def test(img1 ):
    cv2.namedWindow("test2")
    cv2.createTrackbar("l_h","test2", low[0], 180, low_change_h)
    cv2.createTrackbar("l_s","test2", low[1], 255, low_change_s)
    cv2.createTrackbar("l_v","test2", low[2], 255, low_change_v)
    cv2.createTrackbar("h_h","test2", high[0], 180, high_change_h)
    cv2.createTrackbar("h_s","test2", high[1], 255, high_change_s)
    cv2.createTrackbar("h_v","test2", high[2], 255, high_change_v)
    
    while True:
        img = rotate_image (img1, -28)
        img = img[400:720]
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv,low,high) 
        cv2.imshow('test2',img)
        ch = cv2.waitKey(5)
        if (ch == 27):
            break
        if (ch == ord('a')):
            low[0]+= 5
    cv2.destroyAllWindows()




def to_qeue(image):
    img = rotate_image (image, -27)
    img = img[400:720]
    cv2.imwrite("croped_.jpg",img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgs = []
    imgs.append(img[:,0:360])
    imgs.append(img[:,360:680])
    imgs.append(img[:,680:950])
    imgs.append(img[:,950:1230])
    imgs.append(img[:,1230:1480])
    imgs.append(img[90:,1480:1650])
    imgs.append(img[90:,1650:1880])

    for a in imgs:
        y_count(a.copy())
        b_count(a.copy())
        g_count(a.copy())
        print()
    




if __name__ == "__main__":
    import os
    if os.name == 'nt':
        img1 = cv2.imread ("a00.jpg")
    else:
        os.system('libcamera-jpeg -o main1080.jpg -t 10 --width 2592  --height 1944')
        img1 = cv2.imread("main1080.jpg")
    
    to_qeue(img1)
    #test(img1)

    

    pass