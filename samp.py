import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Projectile parameters
initial_position = np.array([-5.0, 0.0, 0.0], dtype=float)  # Start position at origin
initial_velocity = np.array([10.0, 10.0, 0.0], dtype=float)  # Initial velocity in (x, y, z) direction
gravity = np.array([0.0, -9.8, 0.0], dtype=float)           # Gravity affecting only y direction

# Simulation parameters
time_step = 0.05  # Time step for simulation

# Interactive parameters
is_paused = False
selected_component = None

# Camera parameters
camera_rot_x = 0
camera_rot_y = 0
camera_distance = 25
mouse_last_pos = None

# Ground parameters
ground_level = 0.0

def init():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, -2.0, -camera_distance)  # Adjust the camera to see the motion horizontally

def draw_axes():
    glBegin(GL_LINES)
    # X axis in red
    glColor3f(1, 0, 0)
    glVertex3f(-10, 0, 0)
    glVertex3f(10, 0, 0)
    # Y axis in green
    glColor3f(0, 1, 0)
    glVertex3f(0, -5, 0)
    glVertex3f(0, 5, 0)
    glEnd()

def draw_projectile(position):
    glPushMatrix()
    glColor3f(1, 0, 0)  # Red color for the projectile
    glTranslatef(position[0], position[1], position[2])
    # Draw a sphere using quadric object
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.1, 20, 20)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def draw_trajectory(path):
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 1)  # Blue color for the trajectory
    for pos in path:
        glVertex3f(pos[0], pos[1], pos[2])
    glEnd()

def draw_ground():
    glColor3f(0.5, 0.5, 0.5)  # Gray color for the ground
    glBegin(GL_QUADS)
    glVertex3f(-10, ground_level, -10)
    glVertex3f(-10, ground_level, 10)
    glVertex3f(10, ground_level, 10)
    glVertex3f(10, ground_level, -10)
    glEnd()

def draw_text(position, text_string):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2d(position[0], position[1])
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def handle_mouse_events(event):
    global mouse_last_pos, camera_rot_x, camera_rot_y, camera_distance

    if event.type == MOUSEBUTTONDOWN:
        if event.button == 4:  # Scroll up
            camera_distance -= 1
        elif event.button == 5:  # Scroll down
            camera_distance += 1
        else:
            mouse_last_pos = event.pos
    elif event.type == MOUSEBUTTONUP:
        mouse_last_pos = None
    elif event.type == MOUSEMOTION:
        if mouse_last_pos:
            dx, dy = event.pos[0] - mouse_last_pos[0], event.pos[1] - mouse_last_pos[1]
            camera_rot_x += dy
            camera_rot_y += dx
            mouse_last_pos = event.pos

def main():
    global is_paused, initial_velocity, selected_component, camera_distance

    init()
    clock = pygame.time.Clock()

    position = initial_position.copy()
    velocity = initial_velocity.copy()
    path = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    is_paused = not is_paused
                elif event.key == K_r:
                    # Reset the simulation
                    position = initial_position.copy()
                    velocity = initial_velocity.copy()
                    path.clear()
                    is_paused = False
                elif event.key == K_UP:
                    velocity[1] += 1  # Increase y velocity
                elif event.key == K_DOWN:
                    velocity[1] -= 1  # Decrease y velocity
                elif event.key == K_LEFT:
                    velocity[0] -= 1  # Decrease x velocity
                elif event.key == K_RIGHT:
                    velocity[0] += 1  # Increase x velocity
                elif event.key == K_w:
                    velocity[2] += 1  # Increase z velocity
                elif event.key == K_s:
                    velocity[2] -= 1  # Decrease z velocity
            handle_mouse_events(event)

        if not is_paused:
            # Update position and velocity
            velocity += gravity * time_step
            position += velocity * time_step
            path.append(position.copy())

            # Collision with ground
            if position[1] <= ground_level:
                position[1] = ground_level
                velocity[0] = 0
                velocity[1] = 0
                velocity[2] = 0
                is_paused = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply camera transformations
        glLoadIdentity()
        gluLookAt(0, 0, camera_distance, 0, 0, 0, 0, 1, 0)
        glRotatef(camera_rot_x, 1, 0, 0)
        glRotatef(camera_rot_y, 0, 1, 0)

        # Draw axes
        draw_axes()

        # Draw ground
        draw_ground()

        # Draw projectile
        draw_projectile(position)

        # Draw trajectory
        draw_trajectory(path)

        # Draw velocity components
        draw_text((10, 770), f"Velocity X: {velocity[0]:.2f}")
        draw_text((10, 740), f"Velocity Y: {velocity[1]:.2f}")
        draw_text((10, 710), f"Velocity Z: {velocity[2]:.2f}")
        draw_text((10, 680), "Use Arrow keys to change X and Y velocity, W/S to change Z velocity")
        draw_text((10, 650), "Use Mouse to adjust velocity components: Left (X), Middle (Y), Right (Z)")
        draw_text((10, 620), "Scroll Mouse to Zoom In/Out")
        draw_text((10, 590), "Press R to Reset")

        pygame.display.flip()
        clock.tick(60)  # Cap frame rate at 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
