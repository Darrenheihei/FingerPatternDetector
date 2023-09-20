# detect different finger pattern you made
import cv2
import HandTrackingModule as htm


def findRaisedFingers(lmList):
    detected = []
    RHandLm = []
    LHandLm = []
    # 0 means the finger is not raised, 1 means the finger is raised
    # for both hands, leftmost element represent thumb, rightmost element represent little finger (尾指)
    RHand = [0, 0, 0, 0, 0]
    LHand = [0, 0, 0, 0, 0]

    if lmList == []: # didn't detect any hand
        return detected, RHand, LHand

    # check how many hands are detected and see if they are right or left hand/relative position of right and left hand
    if lmList[0].handID == lmList[-1].handID: # only one hand detected
        # use lm 0 and lm 1's relative position to confirm which hand is being detected
        if lmList[0].x < lmList[1].x: # detected right hand
            RHandLm = lmList
            detected = ['R']
        else: # detected left hand
            LHandLm = lmList
            detected = ['L']
    else: # detected both hand
        if lmList[0].x < lmList[1].x: # detected right hand on the left of the screen
            RHandLm = [i for i in lmList if i.handID == lmList[0].handID]
            LHandLm = [i for i in lmList if i.handID != lmList[0].handID]
        else: # detected left hand on the left of the screen
            LHandLm = [i for i in lmList if i.handID == lmList[0].handID]
            RHandLm = [i for i in lmList if i.handID != lmList[0].handID]

        if RHandLm[0].x < LHandLm[0].x: # right hand is to the left of left hand on the screen
            detected = ['R', 'L']
        else:
            detected = ['L', 'R']

    # deal with right hand first
    if RHandLm != []:
        # thumb
        if RHandLm[3].x < RHandLm[4].x:
            RHand[0] = 1
        else:
            RHand[0] = 0

        # other fingers
        for n, (i, j) in enumerate(((6, 8), (10, 12), (14, 16), (18, 20))):
            if RHandLm[i].y > RHandLm[j].y:
                RHand[n + 1] = 1
            else:
                RHand[n + 1] = 0

    # then deal with left hand
    if LHandLm != []:
        # thumb
        if LHandLm[3].x > LHandLm[4].x:
            LHand[0] = 1
        else:
            LHand[0] = 0

        # other fingers
        for n, (i, j) in enumerate(((6, 8), (10, 12), (14, 16), (18, 20))):
            if LHandLm[i].y > LHandLm[j].y:
                LHand[n + 1] = 1
            else:
                LHand[n + 1] = 0

    return detected, RHand, LHand


def drawFingers(img, detected, RHand, LHand):
    # draw rectangle frame
    cv2.rectangle(img, (0, 0), (500, 400), (255, 255, 255), 2)

    RHandStart_x = 0
    RHandStart_y = 30
    LHandStart_x = 0
    LHandStart_y = 30

    if len(detected) == 0:
        return img

    # get position of the drawing hands
    if len(detected) == 1:
        RHandStart_x = 140
        LHandStart_x = 140
    else:
        if detected[0] == 'R':
            RHandStart_x = 30
            LHandStart_x = 270
        else:
            RHandStart_x = 270
            LHandStart_x = 30

    # draw right hand
    if 'R' in detected:
        cv2.putText(img, "R", (RHandStart_x + 90, RHandStart_y + 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 0), 2)
        cv2.rectangle(img, (RHandStart_x, RHandStart_y + 180), (RHandStart_x + 200, RHandStart_y + 300), (200, 0, 0), 2)
        for n, i in enumerate(RHand[::-1]):
            if i: # finger i raising up
                if n == 4:
                    cv2.rectangle(img, (RHandStart_x + 40*n, RHandStart_y + 50), (RHandStart_x + 40*n + 40, RHandStart_y + 180), (200, 0, 0), 2)
                else:
                    cv2.rectangle(img, (RHandStart_x + 40*n, RHandStart_y), (RHandStart_x + 40*n + 40, RHandStart_y + 180), (200, 0, 0), 2)
            else: # finger i is not raising up
                cv2.rectangle(img, (RHandStart_x + 40 * n, RHandStart_y + 180), (RHandStart_x + 40 * n + 40, RHandStart_y + 280), (200, 0, 0), 2)

    # draw left hand
    if 'L' in detected:
        cv2.putText(img, "L", (LHandStart_x + 90, LHandStart_y + 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 0), 2)
        cv2.rectangle(img, (LHandStart_x, LHandStart_y + 180), (LHandStart_x + 200, LHandStart_y + 300), (200, 0, 0), 2)
        for n, i in enumerate(LHand):
            if i: # finger i raising up
                if n == 0:
                    cv2.rectangle(img, (LHandStart_x, LHandStart_y + 50), (LHandStart_x + 40, LHandStart_y + 180), (200, 0, 0), 2)
                else:
                    cv2.rectangle(img, (LHandStart_x + 40*n, LHandStart_y), (LHandStart_x + 40*n + 40, LHandStart_y + 180), (200, 0, 0), 2)
            else: # finger i is not raising up
                cv2.rectangle(img, (LHandStart_x + 40 * n, LHandStart_y + 180), (LHandStart_x + 40 * n + 40, LHandStart_y + 280), (200, 0, 0), 2)

    # cv2.rectangle(img, (30, 30), (230, 330), (255, 255, 255), 2)
    # cv2.rectangle(img, (270, 30), (470, 330), (255, 255, 255), 2)

    return img

def main():
    cap = cv2.VideoCapture(1)
    detector = htm.HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=False)
        img, lmList = detector.findPositions(img, draw=False)

        detected, RHand, LHand = findRaisedFingers(lmList)
        img = drawFingers(img, detected, RHand, LHand)

        cv2.imshow("Finger Counter", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

if __name__ == "__main__":
    main()