import random as rand
import cv2 as cv

# Define a class "Item" which is any item that appears in the game
class Item:
    def __init__(self, lane, speed, top_pos, bottom_pos, frame):
        self.speed = speed
        self.lane = lane
        self.position = top_pos + rand.randint(1, 100)
        self.bottom_pos = bottom_pos
        self.frame = frame
        self.active = True

    def step(self): # Steps the item
        # If the item hits the bottom, destroy it, else move it down.
        if (self.position <= self.bottom_pos):
            self.active = False

        else:
            self.position = self.position - self.speed
            self.show()

    def collided(self, lane, mcqueen, vulnerable): # Checks if the item has collided
        # If vulnerable (not using Nitro), in the same lane and same position as McQueen, then it collides
        if vulnerable == True:
            if self.lane == lane:
                if self.position == mcqueen:
                    return True
        return False


    


        
class Tire(Item):
    def __init__(self, lane, speed, top_pos, bottom_pos, frame):
        super().__init__(lane, speed, top_pos, bottom_pos, frame)
        
    # If collided, decrease points and deactivate
    def collision_action(self, points, penalty):
        points = points - penalty
        self.active = False
        return points

    def show(self):
        cv.circle(self.frame, self.position, 10, (10, 10, 10), 3)
        cv.circle(self.frame, self.position, 7, (140, 140, 140), 7)




class Nitro(Item):
    def __init__(self, lane, speed, top_pos, bottom_pos):
        super().__init__(lane, speed, top_pos, bottom_pos)

    # If collided, increase points and deactivate
    def collision_action(self, points, reward):
        points = points + reward
        self.active = False
        return points

    def show(self):
        top_left = (self.position + 5, self.position + 12)
        bottom_right = (self.position - 5, self.position - 12)
        cv.rectangle(self.frame, top_left, bottom_right, (0, 200, 200), 12)



