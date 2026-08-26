import random as rand


# Define a class "Item" which is any item that appears in the game
class Item:
    def __init__(self, lane, speed, top_pos, bottom_pos):
        self.speed = speed
        self.lane = lane
        self.position = top_pos + rand.randint(1, 100)
        self.bottom_pos = bottom_pos
        self.active = True

    def step(self): # Steps the item
        # If the item hits the bottom, destroy it, else move it down.
        if (self.position <= self.bottom_pos):
            self.active = False

        else:
            self.position = self.position - self.speed

    def collided(self, lane, mcqueen, vulnerable): # Checks if the item has collided
        # If vulnerable (not using Nitro), in the same lane and same position as McQueen, then it collides
        if vulnerable == True:
            if self.lane == lane:
                if self.position == mcqueen:
                    return True
        return False


        
class Tire(Item):
    def __init__(self, lane, speed, top_pos, bottom_pos):
        super().__init__(lane, speed, top_pos, bottom_pos)
        
    # If collided, decrease points and deactivate
    def collision_action(self, points, penalty):
        points = points - penalty
        self.active = False
        return points





class Nitro(Item):
    def __init__(self, lane, speed, top_pos, bottom_pos):
        super().__init__(lane, speed, top_pos, bottom_pos)

    # If collided, increase points and deactivate
    def collision_action(self, points, reward):
        points = points + reward
        self.active = False
        return points




