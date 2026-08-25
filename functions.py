import obstacles as ob
import random as rand
import cv2 as cv

speed = 5
top_pos = 200
bottom_pos = 0
number = 10
lanes = 4


# Populate: Returns a list of random items in random lanes
def populate(number, lanes):
    items = []
    for _ in range(number):
        type = rand.randint(1,2)
        lane = rand.randint(1, lanes)

        if type == 1:
            items.append(ob.Tire(lane, speed, top_pos, bottom_pos))

        else:
            items.append(ob.Nitro(lane, speed, top_pos, bottom_pos))
        cv.waitKey(rand.randint(100, 2000))
    return items
# Replace inactive items
...
# Check Position for any object (returns lane and pos)
...
# Tire: If Position == McQueen's and Vulnerability == True: Lose Nitro Points
...
# Nitro: If Position == McQueen's and Vulnerability == True: Gain Nitro Points
...