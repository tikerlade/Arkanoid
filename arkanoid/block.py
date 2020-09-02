import cv2


class Block:
    # Constructor
    def __init__(self, x, y):
        self.x1 = x
        self.x2 = self.x1 + 20
        self.y1 = y
        self.y2 = self.y1 + 20

    # Printing ball on its current position
    def show(self, frame):
        if not (self.x1 == self.x2 == self.y1 == self.y2 == 0):
            cv2.rectangle(frame, (self.x1 + 1, self.y1 + 1), (self.x2 - 1, self.y2 - 1), (0, 255, 255), -1)

    # Delete block
    def destruct(self):
        self.x1, self.x2 = 0, 0
        self.y1, self.y2 = 0, 0
