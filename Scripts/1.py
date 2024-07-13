import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CONSTANT_VELOCITY = 0.01
ACCELERATION = 0.0001
VELOCITY_STEP = 0.001
ACCELERATION_STEP = 0.00001

# Initial positions
x1 = -1.0
x2 = -1.0
velocity1 = CONSTANT_VELOCITY
acceleration2 = ACCELERATION
velocity2 = 0.0

def draw_text(position, text_string):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_rect(x, y):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + 0.1, y)
    glVertex2f(x + 0.1, y + 0.1)
    glVertex2f(x, y + 0.1)
    glEnd()

def main():
    global x1, x2, velocity1, acceleration2, velocity2

    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    glOrtho(-1, 1, -1, 1, -1, 1)
    font = pygame.font.Font(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP:
                    velocity1 += VELOCITY_STEP
                elif event.key == K_DOWN:
                    velocity1 = max(0, velocity1 - VELOCITY_STEP)
                elif event.key == K_RIGHT:
                    acceleration2 += ACCELERATION_STEP
                elif event.key == K_LEFT:
                    acceleration2 = max(0, acceleration2 - ACCELERATION_STEP)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Update positions
        x1 += velocity1
        velocity2 += acceleration2
        x2 += velocity2

        # Draw objects
        glColor3f(1, 0, 0)  # Red
        draw_rect(x1, 0.3)
        glColor3f(0, 0, 1)  # Blue
        draw_rect(x2, -0.3)

        # Display controls and velocities
        glColor3f(1, 1, 1)
        draw_text((10, WINDOW_HEIGHT - 30), "Controls:")
        draw_text((10, WINDOW_HEIGHT - 60), "UP: Increase velocity of Red rectangle")
        draw_text((10, WINDOW_HEIGHT - 90), "DOWN: Decrease velocity of Red rectangle")
        draw_text((10, WINDOW_HEIGHT - 120), "RIGHT: Increase acceleration of Blue rectangle")
        draw_text((10, WINDOW_HEIGHT - 150), "LEFT: Decrease acceleration of Blue rectangle")

        # Display velocities at the bottom right corner
        velocity_texts = [
            f"Red Rectangle Velocity: {velocity1:.4f}",
            f"Blue Rectangle Velocity: {velocity2:.4f}",
            f"Blue Rectangle Acceleration: {acceleration2:.6f}"
        ]
        text_width = max(font.size(text)[0] for text in velocity_texts)
        draw_text((WINDOW_WIDTH - text_width - 10, 30), velocity_texts[0])
        draw_text((WINDOW_WIDTH - text_width - 10, 60), velocity_texts[1])
        draw_text((WINDOW_WIDTH - text_width - 10, 90), velocity_texts[2])

        pygame.display.flip()
        pygame.time.wait(10)

        if x1 > 1.0:
            x1 = -1.0
        if x2 > 1.0:
            x2 = -1.0
            velocity2 = 0.0

    pygame.quit()

if __name__ == "__main__":
    main()
