"""This example starts learning about pygame"""
import pygame as pg
import sys

# Initialize Pygame
pg.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Event Handling Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize font
pg.font.init()
font = pg.font.SysFont(None, 48)

# Function to render text
def render_text(text, pos):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, pos)

# Main game loop
message = ""
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_LEFT:
                message = "Left arrow key pressed"
            elif event.key == pg.K_RIGHT:
                message = "Right arrow key pressed"
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                message = f"Mouse clicked at {event.pos}"

    # Clear the screen
    screen.fill(BLACK)

     # Draw the red line in the middle of the screen
    pg.draw.line(screen, RED, (0, HEIGHT // 2), (WIDTH, HEIGHT//2), 5)

    # Render the message
    if message:
        render_text(message, (50, 50))

    # Update the display
    pg.display.update()