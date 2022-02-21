import win32api, win32con
from PIL import ImageGrab
import time

#Value will determine if the code loops after a certain time.
loopCode = True;

#Start Delay
time.sleep(5);

doorOpen = [True,True];
threatList = [False, False, False, False];



def moveMouse(x,y):
    win32api.SetCursorPos((x,y))

def click(x,y):
    time.sleep(0.0)
    win32api.SetCursorPos((x,y));
    time.sleep(0.0);
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0);
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0);
    time.sleep(0.1);

def screenGrab(x,y):
    ss_region = (x, y, x + 400 - 2*199, y + 400 - 2*199)
    ss_img = ImageGrab.grab(ss_region)
    return ss_img.getpixel((200 - 199,200 - 199))

def camera():
    time.sleep(0)
    win32api.SetCursorPos((550,640))
    time.sleep(0.05)

    for i in range(0,15):

        time.sleep(0.01);
        win32api.SetCursorPos((550,650 + i))

    for i in range(0,10):

        time.sleep(0.0);
        win32api.SetCursorPos((550,650 + 10 - i))

def lockDoor(side):

    time.sleep(0.1);
    if (side == 0):
        xButton = 50;
        threat = [threatList[1], threatList[3]];
    else:
        xButton = 1220;
        threat = [threatList[0], threatList[2]];

    if ((doorOpen[side] == True) & ((threat[0] == True) | (threat[1] == True))):
        moveMouse(xButton,340);
        click(xButton,340);
        doorOpen[side] = False;
        time.sleep(0.1);
        click(xButton,440);


    elif ((doorOpen[side] == False) & ((threat[0] == False) & (threat[1] == False))):
        moveMouse(xButton,340);
        click(xButton,340);
        doorOpen[side] = True;

    return;


def initCams():
    camera();
    moveMouse(1100,640);
    time.sleep(6.3);
    click(1100,640);
    camera();


def checkCams():
    camera();

    if (threatList[2] == True):
        checkFoxy();

    time.sleep(0.2);
    camera();

    return;


def checkFoxy():
    time.sleep(0.3);
    click(920,480);

    foxySum = 0;
    ss_region = (0 , 100, 1220, 100 + 1);
    ss_img = ImageGrab.grab(ss_region);

    for i in range(0,1219):
        foxySum += ss_img.getpixel((i,0))[2];

    foxySum = foxySum;

    if (foxySum < 32000):
        threatList[3] = True;
        print("Foxy");
        click(980,600);
        
    time.sleep(0.1);
    click(1100,640);

    return;


def checkDoor(side):
    if (side == 0):
        xButton = 50;
        xCamera = 295 + 199;
        yCamera = 95 + 199;
    else:
        xButton = 1220;
        xCamera = 660 + 199;
        yCamera = 150 + 199;

    moveMouse(xButton,440);
    time.sleep(0.475);
    click(xButton,440);
    click(xButton,600);
    doorPic = screenGrab(xCamera,yCamera)[side];
    doorPic += screenGrab(xCamera,yCamera)[side];
    doorPic += screenGrab(xCamera,yCamera)[side];

    if (side == 0):
        if (doorPic < 12):
            threatList[1] = True;
            print("Bonnie");
        else:
            threatList[1] = False;
            click(xButton,440);

    else:
        if (doorPic > 20):
            threatList[2] = True;
            print("Chica");
        else:
            threatList[2] = False;
            click(xButton,440);

    lockDoor(side);

    return;

def start(night):
    if night == 7:
        moveMouse(200,630);
        time.sleep(0.2);
        click(200,630);
        time.sleep(1);
        moveMouse(1220,675);
        time.sleep(0.2);
        click(1220,675);
        time.sleep(10);
    
    camera();
    time.sleep(0.4);
    click(920,480);
    camera();


def main():
    beginTime = time.time();
    start(7);
    initCams();

    while(time.time() < beginTime + 500):
        checkCams();
        if (threatList[3]):
            lockDoor(0);
            time.sleep(3);
            threatList[3] = False;
            lockDoor(0);

        checkDoor(0);
        checkDoor(1);

        print(threatList);
        

while(loopCode):
    main();
    time.sleep(45);