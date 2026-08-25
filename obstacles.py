

# Define a class "Item" which is any item that appears in the game
class Item:
    def __init__(self, lane, speed, top_pos, bottom_pos):
        self.speed = speed
        self.lane = lane
        self.start_position = top_pos
        self.bottom_position = bottom_pos
        self.active = True

    def step(self):
        # If the block hits the bottom, destroy it, else move it down.
        if (self.position <= self.bottom_pos):
            self.active = False

        else:
            self.position = self.position - self.speed




        
class Tire(Item):
    def __init__(self, lane, speed, top_pos, bottom_pos):
        super().__init__(lane, speed, top_pos, bottom_pos)
        
    # If collided, decrease points
    def collided(self, points):
        ...
        return points






