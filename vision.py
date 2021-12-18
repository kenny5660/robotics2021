import cv2
import numpy as np


low = np.array((84,73,11), np.uint8)
high = np.array((110,255,255), np.uint8)




def g_count(img, i):
    l = np.array((84,200,11), np.uint8)
    h = np.array((110,255,255), np.uint8)
    mask = cv2.inRange(img,l,h) 
    count = cv2.countNonZero(mask) * (((40/37)**i)**2)
    print(count, ":g ")

    return count 


def b_count(img, i):
    l = np.array((113,143,31), np.uint8)
    h = np.array((122,255,255), np.uint8)
    mask = cv2.inRange(img,l,h) 
    count = cv2.countNonZero(mask) * (((40/37)**i)**2)
    print(count, ":b ")
 
    return count

def y_count(img, i):
    l = np.array((16,192,16), np.uint8)
    h = np.array((51,248,255), np.uint8)
    mask = cv2.inRange(img,l,h) 
    count = cv2.countNonZero(mask) * (((40/37)**i)**2)
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
        img = rotate_image (img1, -15)
        img = img[600:980]
        
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img_hsv,low,high) 
        cv2.imwrite("out.jpg", mask)
        cv2.imshow('test2',mask)
        ch = cv2.waitKey(5)
        if (ch == 27):
            break
        if (ch == ord('a')):
            low[0]+= 5
    cv2.destroyAllWindows()

def color(y,b,g):
    if (y > b and y > g):
        return 'y'
    if (b > y and b > g):
        return 'b'
    if (g > b and g > y):
        return 'g'
    return 'g'

def get_type(y,b,g):
    col = color(y,b,g)
    if (col == 'b'):
        if (b > 30000):
            return "bb"
        else:
            return "mb"
    elif (col == 'g'):
        if (g < 30000):
            return "mg"
        else:
            return "bg"
    else:
        if (y < 32000):
            return "by"
        else:
            return "by"

def queue_to_st(queue):
    st = {}
    st_c = {}
    j = 0
    st[queue[0]] = j
    st_c[queue[0]] = 1
    j += 1
    st_q = []
    st_q.append(0)
    for i in range(1,7):
        if (queue[i] in st.keys()):
            if (st_c[queue[i]] > 1):
                st_q.append(j)
                j = j + 1
            else:    
                st_q.append(st[queue[i]])
                st_c[queue[i]] += 1 
        else:
            st[queue[i]] = j
            st_q.append(st[queue[i]])
            st_c[queue[i]] = 1
            j = j + 1
    return st_q

def to_qeue(image):
    img = rotate_image (image, -15)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = img[630:980]
    cv2.imwrite("cropfull.jpg",cv2.cvtColor(img, cv2.COLOR_HSV2BGR))
    imgs = []
    imgs.append(img[:,120:520])
    cv2.imwrite("crop1.jpg",cv2.cvtColor(imgs[-1], cv2.COLOR_HSV2BGR))
    imgs.append(img[:,530:900])
    cv2.imwrite("crop2.jpg",cv2.cvtColor(imgs[-1], cv2.COLOR_HSV2BGR))
    imgs.append(img[:,900:1250])
    cv2.imwrite("crop3.jpg",cv2.cvtColor(imgs[-1], cv2.COLOR_HSV2BGR))
    imgs.append(img[:,1250:1580])
    cv2.imwrite("crop4.jpg",cv2.cvtColor(imgs[-1], cv2.COLOR_HSV2BGR))
    imgs.append(img[:,1580:1890])
    cv2.imwrite("crop5.jpg",cv2.cvtColor(imgs[-1], cv2.COLOR_HSV2BGR))
    imgs.append(rotate_image (img[:,1890:2220], -25)[30:,:280])
    cv2.imwrite("crop6.jpg",cv2.cvtColor(imgs[-1], cv2.COLOR_HSV2BGR))
    imgs.append(rotate_image (img[:,2150:2490], -25)[:,35:320])
    cv2.imwrite("crop7.jpg",cv2.cvtColor(imgs[-1], cv2.COLOR_HSV2BGR))
    i = 0
    queue = []
    for a in imgs:
        y = y_count(a.copy(), i)
        b = b_count(a.copy(), i)
        g = g_count(a.copy(), i)
        type = get_type(y,b,g)
        queue.append(type)
        i = i + 1
        #print()
    print(queue)
    return queue_to_st(queue)





if __name__ == "__main__":
    import os
    if os.name == 'nt':
        img1 = cv2.imread ("t1.jpg")
    else:
        os.system('libcamera-jpeg -o main1080.jpg -t 10 --width 2592  --height 1944')
        img1 = cv2.imread("main1080.jpg")
    
    print(to_qeue(img1))
    #test(img1)

    

    pass