import cv2
import numpy as np

videoCapture = cv2.VideoCapture(0)
prevCircle = None
def dist(x1, y1, x2, y2): return (x1-x2)**2*(y1-y2)**2


while True:
    ret, frame = videoCapture.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (17, 17), 0)

    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.2,
                               100, param1=100, param2=75, minRadius=75, maxRadius=500)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None:
                chosen = i
            if prevCircle is not None:
                if (dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1])):
                    chosen = i
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
        prevCircle = chosen

    flip_img = cv2.flip(frame, 1)
    cv2.imshow("Frame", flip_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv2.destroyAllWindows()
