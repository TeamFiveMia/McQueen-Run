import random as rand
import obstacles as ob

speed = 5 # The speed at which items move
top_pos = 200 # Position at the top of the screen
bottom_pos = 0 # Position at the bottom of the screen

number = 10 # Number of items at any time
lanes = 4 # Number of lanes
items = [] # The list of all items

points = 0 # Initializing points to 0
penalty = 10 # The penalty of points when colliding with the tires
reward = 5 # The reward of points (nitro) when collecting nitro

# Get McQueen's data, from Rewan's code
mcqueen.pos = ...
mcqueen.lane = ...
mcqueen.vulnerable = ...

# new_item: Returns a list of random items in random lanes
def new_item(number, lanes):
    for _ in range(number):
        type = rand.randint(1,2)
        lane = rand.randint(1, lanes)

        if type == 1:
            return ob.Tire(lane, speed, top_pos, bottom_pos)

        else:
            return ob.Nitro(lane, speed, top_pos, bottom_pos)

# Handle losing the game
def game_lost():
    ...


def main():
    # Create the items
    for _ in range(10):
        items.append(new_item(number, lanes))

    # Start the game
    while 1:
        if points < 0:
            game_lost()
        for item in items:
            item.step()
            if item.active == False:
                item = new_item(number, lanes)
            if item.collided(item, mcqueen.lane, mcqueen.pos, mcqueen.vulnerable):
                item.collision_action(points, penalty=penalty, reward=reward)


if __name__ == "__main__":
    main()