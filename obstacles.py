

# Define a class "Item" which is any item that appears in the game
class Item:
    def __init__(self, lane, speed, top_pos, bottom_pos):
        self.speed = speed
        self.lane = lane
        self.start_position = top_pos
        self.bottom_position = bottom_pos
        self.active = True





