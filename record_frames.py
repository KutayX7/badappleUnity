import cv2
import math
import pyautogui
import time

# IMPORTANT!
#  It is recommended to use this on an empty project.
#  Unity 2022 WILL slow down at some point and only easy solution so far is to restart Unity.
#    Because of this, it is recommended to use START_FRAME_INDEX and END_FRAME_INDEX settings.
#  If you run into Unity glitches/slowdowns too quickly, try disabling UndoRetainStack and UndoSerializeStack, and restart Unity.
#  Please check and customize every settings in the config (below) before you run this program.
#  Quickly move your mouse to the top-left corner of your screen to stop the program (if things go wrong).

### CONFIG
START_DELAY = 7.0 # seconds you have until you open the Unity animator window. Be ready and good luck :)

START_FRAME_INDEX = 1 # (min: 1, default: 1)
END_FRAME_INDEX = 0 # (default: 0)
FRAME_SKIP = 0 # be careful with this setting! (min: 0, default: 0, possbile good values: [0, 1, 3, 7, 15, 31])

# default values here are for 30hz displays with default Unity settings. decrease them if you have a higher refresh rate.
PLACE_WAIT_TIME = 0.016 # (default: 0.05)
SCREENSHOT_WAIT_TIME = 0.15 # (default: 0.5)
UNDO_WAIT_TIME = 0.016 # (default: 0.035)

# you can find correct values either by experimenting or measuring the pixels. top left corner is (0, 0)
START_POSITION = {"x": 382, "y": 127} # position of the top-left corner
BLOCK_SIZE = {"x": 200, "y": 40} # size of a animator state in pixels
RESOLUTION = {"x": 6, "y": 17} # shape and amount of animator states
CONTEXT_MENU_WIDTH = 200 # average width of the context menu (default: 200)

SOURCE_PATH = "badapple.mp4"
FILE_SAVE_PATH = "frames/frame"
SCREENSHOT_SAVE_FORMAT = ".png" # (default: ".png")
NUM_OF_DIGITS = "06" # (default: "06")
CONTINIOUS_FRAME_NAMING = False # (default: False)

SHOW_END_ALERT = True # (default: True)
### END CONFIG

objectCount = 0

def sample(frame, uvx, uvy):
    height, width = frame.shape
    if frame[math.floor(uvy * height), math.floor(uvx * width)] > 128:
        return True
    return False

def placeObject():
    pyautogui.rightClick()
    pyautogui.moveRel(CONTEXT_MENU_WIDTH * 0.75, 8)
    pyautogui.click()
    pyautogui.moveRel(CONTEXT_MENU_WIDTH * 0.75, 0)
    pyautogui.click()

def render(frame):
    global objectCount
    pyautogui.PAUSE = PLACE_WAIT_TIME
    endX, endY = START_POSITION["x"] + (RESOLUTION["x"] - 1) * BLOCK_SIZE["x"], START_POSITION["y"] + (RESOLUTION["y"] - 1) * BLOCK_SIZE["y"]
    x, y = endX, endY
    for i in reversed(range(RESOLUTION["y"])):
        x = endX
        for j in reversed(range(RESOLUTION["x"])):
            if sample(frame, (j + 0.5)/RESOLUTION["x"], (i + 0.5)/RESOLUTION["y"]):
                pyautogui.moveTo(x, y)
                placeObject()
                objectCount += 1
            x -= BLOCK_SIZE["x"]
        y -= BLOCK_SIZE["y"]

def undoAll():
    global objectCount
    pyautogui.PAUSE = UNDO_WAIT_TIME
    extraWaitTime = UNDO_WAIT_TIME * 8
    while objectCount > 0:
        pyautogui.hotkey("ctrl", "z")
        objectCount -= 1
        extraWaitTime += UNDO_WAIT_TIME + 0.025 # undo operation is sometimes throttled so we have to compensate for it
    time.sleep(extraWaitTime)

def main():
    pyautogui.FAILSAFE = True
    
    cap = cv2.VideoCapture(SOURCE_PATH)
    ret, frame = cap.read()
    
    if not ret:
        raise Exception("Failed to load the video: " + SOURCE_PATH)
    
    height, width, channels = frame.shape
    currentFrameIndex = 0
    time.sleep(7.0)

    for s in range(START_FRAME_INDEX - 1):
        ret, frame = cap.read()
        currentFrameIndex += 1
        if not ret:
            raise Exception("START_FRAME_INDEX is too big")
    
    while ret:
        currentFrameIndex += 1
        ret, frame = cap.read()
        
        if not ret: # reached the end of the source
            break
        if END_FRAME_INDEX > 0 and currentFrameIndex >= END_FRAME_INDEX: # reached desired end frame
            break
        
        frame2 = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),(RESOLUTION["x"], RESOLUTION["y"]),interpolation = cv2.INTER_AREA)
        render(frame2)
        
        time.sleep(SCREENSHOT_WAIT_TIME) # waits for context menu to fade away
        
        pyautogui.screenshot(FILE_SAVE_PATH + format(currentFrameIndex, NUM_OF_DIGITS) + SCREENSHOT_SAVE_FORMAT)
        
        undoAll()
        
        for s in range(FRAME_SKIP):
            if not CONTINIOUS_FRAME_NAMING:
                currentFrameIndex += 1
            ret, frame = cap.read()
            if not ret:
                break
        if not ret: # reached the end during frame skip
            break
    undoAll()
    cap.release()
    pyautogui.alert("Complete!")

if __name__ == "__main__":
    main()
