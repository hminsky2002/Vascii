import cv2
import numpy as np
import curses

# Set this to True to get real camera video from cv2
SHOW_REAL_VIDEO = False


ASCII_MAP = dict(enumerate([' ', '.', "'", ',', ':', ';', 'c', 'l', 'x', 'o',
                            'k', 'X', 'd', 'O', '0', 'K', 'N']))
convert_to_ascii = np.vectorize(lambda x: ASCII_MAP[int(x/15.9375)])

def main(stdscreen):
    init_curses(stdscreen)
    cap = cv2.VideoCapture("rtsp://192.168.86.46:8554/live.sdp")
    quit = False
    while not quit:
        # Get screensize for reduction
        screen_height, screen_width = stdscreen.getmaxyx()
        # Capture frame-by-frame
        # Get image data
        ret, frame = cap.read()
        # Our operations on the frame come here
        # Convert data to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        if SHOW_REAL_VIDEO:
            cv2.imshow('frame',gray)
        #Reduce grayscale array to proper resolution
        reduced = cv2.resize(gray, (int(screen_width), int(screen_height)))
        #Plug in reduced resolution numpy array for ascii converter func
        converted = convert_to_ascii(reduced)
        # Output result
        for row_num, row in enumerate(converted):
            stdscreen.addstr(row_num, 0, ''.join(row[:-1]))
        stdscreen.refresh()
        # Test for quit signal
        quit = (cv2.waitKey(1) & 0xFF == ord('q') or stdscreen.getch() == ord('q'))
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def init_curses(stdscreen):
    # Do not echo characters to terminal
    curses.noecho()
    # No input buffer, make stdscreen.getch() nonblocking
    curses.cbreak()
    stdscreen.nodelay(1)
    # Hide cursor
    curses.curs_set(0)
    # Matrix colors :)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscreen.attron(curses.color_pair(1))
    stdscreen.clear()

if __name__ == '__main__':
    curses.wrapper(main)