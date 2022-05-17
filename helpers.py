import cv2


def generate_thumbnail(video_path, out_filename):
    # Opens the inbuilt camera of laptop to capture video.
    cap = cv2.VideoCapture(video_path)
    i = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        # This condition prevents from infinite looping
        # incase video ends.
        if ret == False:
            break
        # Save Frame by Frame into disk using imwrite method
        cv2.imwrite(out_filename, frame)
        i += 1
    cap.release()
    cv2.destroyAllWindows()
