import cv2

START_INDEX = 1 # (default: 1)
END_INDEX = 0 # (default: 0)
STEP_SIZE = 1 # (min: 1, default: 1)
OUTPUT_FPS = 30/STEP_SIZE # (default: 30)
FRAME_SIZE = (1920, 1080)
IMAGES_PATH = "frames/frame"
IMAGE_INDEX_LENGTH = "06" # (default: "06")
IMAGE_EXTENSION = ".png" # (default: ".png")
VIDEO_CODEC = "mp4v"
VIDEO_NAME = "output.mp4"

def main():
    video = cv2.VideoWriter(VIDEO_NAME, cv2.VideoWriter_fourcc(*VIDEO_CODEC), OUTPUT_FPS, FRAME_SIZE)

    endIndex = END_INDEX
    if endIndex < 1:
        endIndex = 2 ** 32 - 1
    
    for i in range(START_INDEX, endIndex + 1, STEP_SIZE):
        filename = IMAGES_PATH + format(i, IMAGE_INDEX_LENGTH) + IMAGE_EXTENSION
        frame = cv2.imread(filename)
        if frame is None:
            break
        video.write(frame)
    
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
