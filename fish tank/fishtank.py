"""Fish Tank, by Al Sweigart al@inventwithpython.com
A peaceful animation of a fish tank. Press Ctrl-C to stop.
Similar to ASCIIQuarium or @EmojiAquarium, but mine is based on an
older ASCII fish tank program for DOS.
https://robobunny.com/projects/asciiquarium/html/
https://twitter.com/EmojiAquarium
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: extra-large, artistic, bext"""

import random, sys, time
import pygame as pg
from pygame.locals import *
from PIL import Image

# Set up the constants:
WIDTH, HEIGHT = 1500, 900
FISH_SIZE = 75

NUM_FISH = 10  # (!) Try changing this to 2 or 100.
NUM_BUBBLERS = 1  # (!) Try changing this to 0 or 10.
NUM_CORALS = 4
FRAMES_PER_SECOND = 60  # (!) Try changing this number to 1 or 60.
# (!) Try changing the constants to create a fish tank with only kelp,
# or only bubblers.

LONGEST_FISH_LENGTH = 10  # Longest single string in FISH_TYPES.

# The x and y positions where a fish runs into the edge of the screen:
LEFT_EDGE = 0
RIGHT_EDGE = WIDTH - FISH_SIZE - 1
TOP_EDGE = 0
BOTTOM_EDGE = HEIGHT - FISH_SIZE - 1


def main():
    global FISHES, BUBBLERS, BUBBLES, STEP, FISH_TYPES, screen, BUBBLE, CORALS, CORAL

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Fish Tank')
    # NOTE: Every string in a fish dictionary should be the same length.
    FISH_TYPES = []
    for i in ('yellow', 'blue', 'green', 'red', 'tropical'):
        FISH_TYPES.append({'left': (pg.transform.scale(pg.image.load(f'fish-{i}.png').convert_alpha(), (FISH_SIZE, FISH_SIZE)),),
                        'right': (pg.transform.flip(pg.transform.scale(pg.image.load(f'fish-{i}.png').convert_alpha(), (FISH_SIZE, FISH_SIZE)), True, False),)})
    FISH_TYPES.append({'left': split_gif_into_frames('fish-pufferfish.gif'), 'right': split_gif_into_frames('fish-pufferfish.gif', True)})
    BUBBLE = pg.transform.scale(pg.image.load('bubbles.png').convert_alpha(), (75, 75))
    CORAL = pg.transform.scale(pg.image.load('coral.png').convert_alpha(), (100, 100))

    # Generate the global variables:
    FISHES = []
    for i in range(NUM_FISH):
        FISHES.append(generateFish())

    # NOTE: Bubbles are drawn, but not the bubblers themselves.
    BUBBLERS = []
    for i in range(NUM_BUBBLERS):
        # Each bubbler starts at a random position.
        BUBBLERS.append(random.randint(LEFT_EDGE, RIGHT_EDGE))
    BUBBLES = []

    CORALS = []
    for i in range(NUM_CORALS):
        # Each bubbler starts at a random position.
        CORALS.append(random.randint(LEFT_EDGE, RIGHT_EDGE))

    # Run the simulation:
    clock = pg.time.Clock()
    STEP = 1
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        simulateAquarium()
        screen.fill((100, 100, 255))
        drawAquarium()
        pg.display.update()
        clock.tick(FRAMES_PER_SECOND)
        STEP += 1


def getRandomColor():
    """Return a string of a random color."""
    return random.choice(('black', 'red', 'green', 'yellow', 'blue',
                          'purple', 'cyan', 'white'))


def generateFish():
    """Return a dictionary that represents a fish."""
    fishType = random.choice(FISH_TYPES)

    # Set up the rest of fish data structure:
    fish = {'right':            fishType['right'],
            'left':             fishType['left'],
            'hSpeed':           random.randint(1, 6),
            'vSpeed':           random.randint(5, 15),
            'timeToHDirChange': random.randint(100, 600),
            'timeToVDirChange': random.randint(20, 200),
            'goingRight':       random.choice([True, False]),
            'goingDown':        random.choice([True, False])}

    # 'x' is always the leftmost side of the fish body:
    fish['x'] = random.randint(LEFT_EDGE, RIGHT_EDGE)
    fish['y'] = random.randint(TOP_EDGE, BOTTOM_EDGE)
    return fish


def simulateAquarium():
    """Simulate the movements in the aquarium for one step."""
    global FISHES, BUBBLERS, BUBBLES, STEP

    # Simulate the fish for one step:
    for fish in FISHES:
        # Move the fish horizontally:
        if STEP % fish['hSpeed'] == 0:
            if fish['goingRight']:
                if fish['x'] != RIGHT_EDGE:
                    fish['x'] += 1  # Move the fish right.
                else:
                    fish['goingRight'] = False  # Turn the fish around.
            else:
                if fish['x'] != LEFT_EDGE:
                    fish['x'] -= 1  # Move the fish left.
                else:
                    fish['goingRight'] = True  # Turn the fish around.

        # Fish can randomly change their horizontal direction:
        fish['timeToHDirChange'] -= 1
        if fish['timeToHDirChange'] == 0:
            fish['timeToHDirChange'] = random.randint(10, 60)
            # Turn the fish around:
            fish['goingRight'] = not fish['goingRight']

        # Move the fish vertically:
        if STEP % fish['vSpeed'] == 0:
            if fish['goingDown']:
                if fish['y'] != BOTTOM_EDGE:
                    fish['y'] += 1  # Move the fish down.
                else:
                    fish['goingDown'] = False  # Turn the fish around.
            else:
                if fish['y'] != TOP_EDGE:
                    fish['y'] -= 1  # Move the fish up.
                else:
                    fish['goingDown'] = True  # Turn the fish around.

        # Fish can randomly change their vertical direction:
        fish['timeToVDirChange'] -= 1
        if fish['timeToVDirChange'] == 0:
            fish['timeToVDirChange'] = random.randint(2, 20)
            # Turn the fish around:
            fish['goingDown'] = not fish['goingDown']

    # Generate bubbles from bubblers:
    for bubbler in BUBBLERS:
        # There is a 1 in 5 chance of making a bubble:
        if random.randint(1, 250) == 1:
            BUBBLES.append({'x': bubbler, 'y': HEIGHT - 2})

    # Move the bubbles:
    for bubble in BUBBLES:
        diceRoll = random.randint(1, 6)
        if (diceRoll == 1) and (bubble['x'] != LEFT_EDGE):
            bubble['x'] -= 1  # Bubble goes left.
        elif (diceRoll == 2) and (bubble['x'] != RIGHT_EDGE):
            bubble['x'] += 1  # Bubble goes right.

        bubble['y'] -= 1  # The bubble always goes up.

    # Iterate over BUBBLES in reverse because I'm deleting from BUBBLES
    # while iterating over it.
    for i in range(len(BUBBLES) - 1, -1, -1):
        if BUBBLES[i]['y'] == TOP_EDGE:  # Delete bubbles that reach the top.
            del BUBBLES[i]

def split_gif_into_frames(gif_path, right=False):
    """
    Splits an animated GIF into individual image frames.

    Args:
        gif_path (str): The path to the input GIF file.
        output_folder (str): The folder where individual frames will be saved.
    """
    frames = []
    with Image.open(gif_path) as im:
        for i in range(im.n_frames):
            im.seek(i)
            image_data = im.tobytes()
            image_size = im.size  # (width, height)
            image_mode = im.mode  # e.g., "RGB", "RGBA", "L"
            surface = pg.transform.flip(pg.transform.scale(pg.image.frombytes(image_data, image_size, image_mode).convert_alpha(), (FISH_SIZE, FISH_SIZE)), right, False)
            frames.append(surface)
    frames.pop(0)
    return frames

def drawAquarium():
    """Draw the aquarium on the screen."""
    global FISHES, BUBBLERS, BUBBLES, STEP

    # Draw the bubbles:
    for bubble in BUBBLES:
        screen.blit(BUBBLE, (bubble['x'], bubble['y']))

    # Draw the fish:
    for fish in FISHES:

        # Get the correct right- or left-facing fish text.
        if fish['goingRight']:
            screen.blit(fish['right'][STEP % len(fish['right'])], (fish['x'], fish['y']))
        else:
            screen.blit(fish['left'][STEP % len(fish['left'])], (fish['x'], fish['y']))

    for coral in CORALS:
        screen.blit(CORAL, (coral, HEIGHT-1-100))


# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()  # When Ctrl-C is pressed, end the program.
