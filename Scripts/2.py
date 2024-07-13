import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Constants for the first pendulum
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRAVITY = 0.0005
LENGTH1 = 0.5
DAMPING1 = 0.99  # Air resistance damping for pendulum 1

# Constants for the second pendulum
LENGTH2 = 0.4
DAMPING2 = 1.0  # No air resistance for pendulum 2
hanging_point1 = (-0.3, 0.3)  # Hanging point for the first pendulum
hanging_point2 = (0.3, -0.3)  # Hanging point for the second pendulum

# Initial angles (from vertical) and angular velocities for the pendulums
theta1 = np.pi / 4  # 45 degrees for the first pendulum
theta_velocity1 = 0.0
theta2 = np.pi / 3  # Initial angle for the second pendulum
theta_velocity2 = 0.0

# Mouse interaction
is_dragging = False
is_fullscreen = False

# Variables for counting oscillations
oscillations1 = 0
oscillations2 = 0
prev_theta_velocity1 = 0.0
prev_theta_velocity2 = 0.0

def draw_text(position, text_string, font_size=64):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_pendulum(origin, x, y):
    glBegin(GL_LINES)
    glVertex2f(origin[0], origin[1])
    glVertex2f(x, y)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(x - 0.05, y - 0.05)
    glVertex2f(x + 0.05, y - 0.05)
    glVertex2f(x + 0.05, y + 0.05)
    glVertex2f(x - 0.05, y + 0.05)
    glEnd()

def screen_to_world(mouse_x, mouse_y):
    world_x = (mouse_x / WINDOW_WIDTH) * 2 - 1
    world_y = (mouse_y / WINDOW_HEIGHT) * 2 - 1
    world_y = -world_y  # Flip y-axis
    return world_x, world_y

def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL | FULLSCREEN)
    else:
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)

def main():
    global theta1, theta_velocity1, theta2, theta_velocity2, is_dragging, is_fullscreen, oscillations1, oscillations2, prev_theta_velocity1, prev_theta_velocity2

    try:
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        glOrtho(-1, 1, -1, 1, -1, 1)

        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_f:
                        toggle_fullscreen()
                if event.type == MOUSEBUTTONDOWN:
                    is_dragging = True
                if event.type == MOUSEBUTTONUP:
                    is_dragging = False

            if is_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x, world_y = screen_to_world(mouse_x, mouse_y)
                # Check distance to decide which pendulum is dragged
                dist1 = np.sqrt((world_x - hanging_point1[0])**2 + (world_y - hanging_point1[1])**2)
                dist2 = np.sqrt((world_x - hanging_point2[0])**2 + (world_y - hanging_point2[1])**2)
                
                if dist1 < dist2:
                    dx = world_x - hanging_point1[0]
                    dy = world_y - hanging_point1[1]
                    theta1 = np.arctan2(dx, -dy)
                    theta_velocity1 = 0.0
                else:
                    dx = world_x - hanging_point2[0]
                    dy = world_y - hanging_point2[1]
                    theta2 = np.arctan2(dx, -dy)
                    theta_velocity2 = 0.0

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Draw heading
            draw_text((-0.6, 0.8), "Pendulums Under Gravity")

            # Draw instructions
            draw_text((-0.95, 0.7), "Press 'F' to toggle fullscreen. Press 'ESC' to exit.", font_size=32)

            # Pendulum 1 dynamics (with air resistance)
            gravity_force1 = GRAVITY * np.sin(theta1)
            theta_acceleration1 = (-gravity_force1 / LENGTH1)
            theta_velocity1 += theta_acceleration1
            theta_velocity1 *= DAMPING1
            theta1 += theta_velocity1

            # Pendulum 2 dynamics (without air resistance)
            gravity_force2 = GRAVITY * np.sin(theta2)
            theta_acceleration2 = (-gravity_force2 / LENGTH2)
            theta_velocity2 += theta_acceleration2
            theta_velocity2 *= DAMPING2
            theta2 += theta_velocity2

            # Calculate positions
            x1 = hanging_point1[0] + LENGTH1 * np.sin(theta1)
            y1 = hanging_point1[1] - LENGTH1 * np.cos(theta1)
            x2 = hanging_point2[0] + LENGTH2 * np.sin(theta2)
            y2 = hanging_point2[1] - LENGTH2 * np.cos(theta2)

            # Count oscillations for pendulum 1
            if prev_theta_velocity1 * theta_velocity1 < 0:
                oscillations1 += 1
            prev_theta_velocity1 = theta_velocity1

            # Count oscillations for pendulum 2
            if prev_theta_velocity2 * theta_velocity2 < 0:
                oscillations2 += 1
            prev_theta_velocity2 = theta_velocity2

            # Draw pendulums
            glColor3f(1, 0, 0)  # Red for pendulum 1 (with air resistance)
            draw_pendulum(hanging_point1, x1, y1)
            glColor3f(0, 0, 1)  # Blue for pendulum 2 (without air resistance)
            draw_pendulum(hanging_point2, x2, y2)

            # Display oscillations count
            draw_text((-0.95, -0.9), f"Oscillations: Pendulum 1 - {oscillations1}, Pendulum 2 - {oscillations2}", font_size=24)

            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
