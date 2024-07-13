import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
START_POS_X = 0.0  # Starting x position of the object
START_POS_Y = 0.9  # Starting y position of the object
SIZE = 0.1         # Size of the object

# Initial values
gravity = -9.8
gravity_step = 0.1  # Initial gravity change step
y_velocity = 0.0
is_dragging = False

def draw_text(position, text_string, size=64):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_square(x, y, size):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + size, y)
    glVertex2f(x + size, y - size)
    glVertex2f(x, y - size)
    glEnd()

def screen_to_world(mouse_x, mouse_y):
    world_x = (mouse_x / WINDOW_WIDTH) * 2 - 1
    world_y = (mouse_y / WINDOW_HEIGHT) * 2 - 1
    world_y = -world_y  # Flip y-axis
    return world_x, world_y

def init():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)

def main():
    global y_velocity, is_dragging, gravity, gravity_step

    init()

    clock = pygame.time.Clock()

    pos_x = START_POS_X
    pos_y = START_POS_Y

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_UP:
                    gravity -= gravity_step
                    gravity_step += 0.01  # Increase the step size
                elif event.key == K_DOWN:
                    gravity += gravity_step
                    gravity_step += 0.01  # Increase the step size
            elif event.type == MOUSEBUTTONDOWN:
                is_dragging = True
            elif event.type == MOUSEBUTTONUP:
                is_dragging = False
            elif event.type == MOUSEWHEEL:
                gravity += event.y * gravity_step
                gravity_step += 0.01  # Increase the step size

        if is_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pos_x, pos_y = screen_to_world(mouse_x, mouse_y)
            y_velocity = 0.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw heading and gravity value
        draw_text((-0.35, 0.8), "Gravity Demonstration", size=48)
        draw_text((-0.2, 0.7), f"Gravity: {abs(gravity):.4f}", size=32)
        
        # Display velocity
        draw_text((-0.2, 0.6), f"Velocity: {y_velocity:.4f}", size=32)
        
        # Display controls
        draw_text((-0.9, -0.9), "Controls:", size=24)
        draw_text((-0.9, -0.95), "Press UP arrow key to decrease gravity", size=20)
        draw_text((-0.9, -1.0), "Press DOWN arrow key to increase gravity", size=20)
        draw_text((-0.9, -1.05), "Click and drag to move the object", size=20)
        draw_text((-0.9, -1.1), "Scroll mouse wheel to adjust gravity", size=20)
        draw_text((-0.9, -1.15), "Press ESC key to quit", size=20)

        if not is_dragging:
            # Apply gravity
            y_velocity += gravity * 0.0001  # Scale gravity to match previous value

        # Update position
        pos_y += y_velocity

        # Collision with ground
        if pos_y - SIZE < -1:
            pos_y = -1 + SIZE
            y_velocity = -y_velocity * 0.8  # Bounce effect

        glColor3f(1, 0, 0)  # Red
        draw_square(pos_x, pos_y, SIZE)

        pygame.display.flip()
        clock.tick(60)  # Adjust frame rate (60 FPS here)

    pygame.quit()

if __name__ == "__main__":
    main()
