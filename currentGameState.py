class GameState:
    def __init__(self, lane, speed, top_pos, bottom_pos):
        self.speed = speed
        self.lane = lane
        self.position = top_pos + rand.randint(1, 100)
        self.bottom_pos = bottom_pos
        self.active = True
