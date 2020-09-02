import random

import cv2
import numpy as np

from arkanoid.ball import Ball
from arkanoid.platform import Platform
from arkanoid.block import Block



def generate_blocks(frame):
    size = 20
    blocks = []
    x = [i for i in range(10, frame.shape[1] - size, size)]
    y = [[j for j in range(10, frame.shape[0] // 3, size)] for i in range(10, frame.shape[1] - size, size)]

    for i in range(int(len(x) * len(y[0]) * 0.9)):
        # Getting coordinates
        x_need = random.choice(x)
        y_need = random.choice(y[x.index(x_need)])

        # Removing them
        y[x.index(x_need)].remove(y_need)
        if (len(y[x.index(x_need)]) == 0):
            del y[x.index(x_need)]
            x.remove(x_need)

        blocks.append(Block(x_need, y_need))

    return blocks


if __name__ == "__main__":
    font = cv2.FONT_HERSHEY_COMPLEX
    l_h = 0
    l_s = 0
    l_v = 80
    u_h = 255
    u_s = 255
    u_v = 255

    cap = cv2.VideoCapture(0)
    played = False
    while True:
        # Intro
        key = cv2.waitKey(1)
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Introduction text or end of game text
        if (not played):
            cv2.putText(frame, "HELLO !!!", (240, 240), font, 1, (0, 0, 255))
            cv2.putText(frame, "PRESS 'SPACE' TO START", (100, 280), font, 1, (0, 0, 255))
        else:
            cv2.putText(frame, "GAME OVER", (240, 240), font, 1, (0, 0, 255))
            cv2.putText(frame, "SCORE : " + str(ball.points), (240, 280), font, 1, (0, 0, 255))

        print(frame)
        cv2.imshow("Arkanoid", frame)

        # If SPACE pressed (32 - code of SPACE)
        if key == 32:
            played = True

            ball = Ball(frame, 3)
            platform = Platform(frame)
            blocks = generate_blocks(frame)

            while True:
                _, frame = cap.read()
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # Showing figures
                cv2.putText(frame, "SCORE : " + str(ball.points), (30, 30), font, 1, (255, 0, 0))
                ball.show(frame)
                platform.show(frame)
                for block in blocks:
                    block.show(frame)

                # Moving objects
                # -----------------------------------------------------------------------------------------------

                lower_red = np.array([l_h, l_s, l_v])
                upper_red = np.array([u_h, u_s, u_v])

                mask = cv2.inRange(hsv, lower_red, upper_red)
                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.erode(mask, kernel)

                # Contours detection
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                font = cv2.FONT_HERSHEY_COMPLEX

                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
                    x = approx.ravel()[0]
                    y = approx.ravel()[1]

                    if 8000 > area > 400:
                        if len(approx) == 4:
                            platform.move_with_contour(frame, approx)

                cv2.putText(frame, "SCORE : " + str(ball.points), (30, 30), font, 1, (255, 255, 255))
                cv2.imshow("Arcanoid", frame)
                cv2.imshow("Mask", mask)
                # ----------------------------------------------------------------------------------------------------

                # If ESC was pressed or ball gone out -> GAME OVER
                key = cv2.waitKey(1)
                if key == 27 or ball.out:
                    ball.out = True
                    break

                ball.move(frame, platform, blocks)
                platform.move(frame, key)

                for block in blocks:
                    if block.x1 == block.x1 == block.x2 == block.x2 == block.y1 == block.y1 == block.y2 == block.y2 == 0:
                        blocks.remove(block)

        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
