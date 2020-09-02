import cv2

class Platform:

    # Constructor
    def __init__(self, frame):
        self.step = 15
        self.width = 80
        self.bound = 5

        self.x1 = frame.shape[1] // 2 - self.width // 2
        self.x2 = frame.shape[1] // 2 + self.width // 2

        self.y1 = int(frame.shape[0] * 0.9)
        self.y2 = self.y1 + 20

    # Printing ball on its current position
    def show(self, frame):
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), (0, 255, 0), -1)

    def check_boundaries(self, frame):

        if 0 >= self.x1:
            self.x1 += self.bound
            self.x2 += self.bound
            return False
        elif frame.shape[1] <= self.x2:
            self.x1 -= self.bound
            self.x2 -= self.bound
            return False
        return True

    # Moving ball to its next point (by key)
    def move(self, frame, key):
        if self.check_boundaries(frame):
            if key == 83:
                self.x1 += self.step
                self.x2 += self.step
            elif key == 81:
                self.x1 -= self.step
                self.x2 -= self.step

    # Moving ball to its next point (by visual)
    def move_with_contour(self, frame, approx):
        if self.check_boundaries(frame) and (approx[0][0][0] != approx[0][0][1]):
            self.x1 = approx[0][0][0]
            self.x2 = self.x1 + self.width