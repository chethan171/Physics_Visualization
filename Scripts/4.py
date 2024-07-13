import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# Initialize Pygame and OpenGL
pygame.init()
display = (1200, 800)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
glTranslatef(0.0, 0.0, -20)

# Parameters for projectile motion
height = 1.0
force = 10.0
angle = 45.0
velocity = np.array([force * math.cos(math.radians(angle)),
                     force * math.sin(math.radians(angle)),
                     0.0])
position = np.array([0.0, height, 0.0])
gravity = np.array([0.0, -9.81, 0.0])
trajectory = []
projecting = False
range_displayed = False

# Camera control variables
camera_angle_x = 0
camera_angle_y = 0
zoom = 1.0
mouse_down = False
mouse_last_x, mouse_last_y = 0, 0

# Function to reset the projectile
def reset_projectile():
    global position, velocity, trajectory, projecting, range_displayed
    position = np.array([0.0, height, 0.0])
    velocity = np.array([force * math.cos(math.radians(angle)),
                         force * math.sin(math.radians(angle)),
                         0.0])
    trajectory = []
    projecting = False
    range_displayed = False

# Function to display controls and other text
def display_text():
    controls = [
        "Controls:",
        "Mouse: Rotate camera",
        "Mouse Scroll: Zoom in/out",
        "Up/Down: Adjust height",
        "Left/Right: Adjust force",
        "W/S: Adjust angle",
        "Space: Start motion",
        "K: Reset",
        "Q: Quit"
    ]
    height_text = f"Height: {height:.2f}"
    angle_text = f"Angle: {angle:.2f} degrees"
    velocity_text = f"Velocity: ({velocity[0]:.2f}, {velocity[1]:.2f}, {velocity[2]:.2f})"
    range_text = f"Range: {trajectory[-1][0]:.2f}" if range_displayed else ""
    y = 10
    for line in controls:
        render_text(line, 10, display[1] - y - 20)
        y += 30
    render_text(height_text, 10, display[1] - y - 20)
    y += 30
    render_text(angle_text, 10, display[1] - y - 20)
    y += 30
    render_text(velocity_text, 10, display[1] - y - 20)
    if range_displayed:
        y += 30
        render_text(range_text, 10, display[1] - y - 20)

# Function to draw a sphere
def draw_sphere(radius, lat_bands, long_bands):
    for i in range(lat_bands):
        lat0 = math.pi * (-0.5 + float(i) / lat_bands)
        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)
        
        lat1 = math.pi * (-0.5 + float(i + 1) / lat_bands)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(long_bands + 1):
            lng = 2 * math.pi * float(j) / long_bands
            x = math.cos(lng)
            y = math.sin(lng)
            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
        glEnd()

# Function to render text using OpenGL
def render_text(text, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glWindowPos2i(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_q):
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
                mouse_last_x, mouse_last_y = event.pos
            elif event.button == 4:
                zoom *= 1.1
            elif event.button == 5:
                zoom /= 1.1
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        elif event.type == MOUSEMOTION:
            if mouse_down:
                dx, dy = event.pos[0] - mouse_last_x, event.pos[1] - mouse_last_y
                camera_angle_x += dy * 0.1
                camera_angle_y += dx * 0.1
                mouse_last_x, mouse_last_y = event.pos
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                height += 0.1
                reset_projectile()
            elif event.key == K_DOWN:
                height -= 0.1
                reset_projectile()
            elif event.key == K_LEFT:
                force -= 1.0
                reset_projectile()
            elif event.key == K_RIGHT:
                force += 1.0
                reset_projectile()
            elif event.key == K_w:
                angle += 1.0
                reset_projectile()
            elif event.key == K_s:
                angle -= 1.0
                reset_projectile()
            elif event.key == K_SPACE and not projecting:
                projecting = True
            elif event.key == K_k:
                reset_projectile()

    if projecting:
        velocity += gravity * clock.get_time() / 1000.0
        position += velocity * clock.get_time() / 1000.0
        trajectory.append(position.copy())
        if position[1] <= 0:
            position[1] = 0
            projecting = False
            range_displayed = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glScalef(zoom, zoom, zoom)
    glRotatef(camera_angle_x, 1, 0, 0)
    glRotatef(camera_angle_y, 0, 1, 0)

    # Draw surface
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)
    glVertex3f(-10, 0, -10)
    glVertex3f(10, 0, -10)
    glVertex3f(10, 0, 10)
    glVertex3f(-10, 0, 10)
    glEnd()

    # Draw projectile
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(*position)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    # Draw trajectory
    glColor3f(0, 1, 0)
    glBegin(GL_LINE_STRIP)
    for point in trajectory:
        glVertex3fv(point)
    glEnd()

    glPopMatrix()

    # Display controls and other text
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, display[0], 0, display[1], -1, 1)
    display_text()
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
