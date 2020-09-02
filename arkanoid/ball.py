class Ball:
    # Constructor
    def __init__(self, frame, speed=4):
        # User points
        self.points = 0

        # Radius
        self.radius = 8

        # Coordinates
        self.x = frame.shape[1] // 2
        self.y = int(frame.shape[0] * 0.7) - self.radius + 1

        # Speeds on axis
        self.move_x = speed
        self.move_y = -speed

        # Whether ball on the board or not
        self.out = False

    # Printing ball on its current position
    def show(self, frame):
        cv2.circle(frame, (self.x, self.y), self.radius, (0, 0, 255), -1)

    # Whether ball hit the wall | platform or not
    def check_boundaries(self, frame, platform):
        next_x = self.x + self.move_x + self.move_x / abs(self.move_x) * self.radius
        next_y = self.y + self.move_y + self.move_y / abs(self.move_y) * self.radius

        # Check boundaries
        if (0 >= next_x or next_x >= frame.shape[1]):
            self.move_x = -self.move_x
        elif next_y <= 0:
            self.move_y = -self.move_y
        elif next_y >= frame.shape[0]:
            self.out = True

        # Check platform
        if platform.x1 <= next_x <= platform.x2:
            if platform.y1 <= next_y <= platform.y2:
                dx = min(abs(platform.x1 - next_x), abs(platform.x2 - next_x))
                dy = min(abs(platform.y1 - next_y), abs(platform.y2 - next_y))

                if (dx < dy):
                    self.move_x = -self.move_x
                elif (dx > dy):
                    self.move_y = -self.move_y
                else:
                    self.move_x = -self.move_x
                    self.move_y = -self.move_y

    # Whether ball hit the target brick
    def check_bitting(self, blocks):
        block_to_delete = Block(0, 0)
        min_dist = 10 ** 9

        next_x = self.x + self.move_x + self.move_x / abs(self.move_x) * self.radius
        next_y = self.y + self.move_y + self.move_y / abs(self.move_y) * self.radius

        for block in blocks:
            if block.x1 - 8 <= next_x <= block.x2 + 8:
                if block.y1 - 8 <= next_y <= block.y2 + 8:
                    center_x = block.x1 + 10
                    center_y = block.y1 + 10

                    dist = ((self.x - center_x) ** 2 + (self.y - center_y) ** 2) ** 0.5

                    if dist < min_dist:
                        dist = min_dist
                        block_to_delete = block

        if not ((block_to_delete.x1 == block_to_delete.y1 == 0) and \
                (block_to_delete.x2 == block_to_delete.y2)):
            center_x = block_to_delete.x1 + 10
            center_y = block_to_delete.y1 + 10

            if (self.x - center_x) > (self.y - center_y):
                self.move_x = -self.move_x
            elif (self.x - center_x) < (self.y - center_y):
                self.move_y = -self.move_y
            else:
                self.move_x = -self.move_x
                self.move_y = -self.move_y

            block_to_delete.destruct()
            self.points += 10

    # Moving ball to its next point
    def move(self, frame, platform, blocks):
        # Check rebound
        self.check_boundaries(frame, platform)

        # Check hitting the target
        self.check_bitting(blocks)

        # Move ball
        self.x += self.move_x
        self.y += self.move_y