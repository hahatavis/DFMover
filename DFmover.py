import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set the initial dimensions of the screen (width, height)
screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)  # Increased height to 600
pygame.display.set_caption('Moving Circle with Adjustable Speed and Size')

# Define colors
DULL_GREEN = (85, 107, 47)  # Dull green background
GREY = (169, 169, 169)  # Grey color for both circle and squares
BLACK = (0, 0, 0)  # Text color

# Font for displaying text
font = pygame.font.SysFont(None, 36)

# Circle properties
circle_radius = 30  # Initial radius of the circle
circle_x = circle_radius  # Start position of the circle (left edge)
circle_y = 200  # Y position is fixed
circle_speed = 2  # Initial speed of movement
direction = 1  # 1 means moving right, -1 means moving left

# Pause duration in seconds when the circle reaches the edges
pause_duration = 0.5  # Half a second

# Square group properties (adjusted y-coordinates for better visibility and grey color for all squares)
groups = {
    'A': {'size': 40, 'x_start': 50, 'y': 350, 'color': GREY},    # Group A (grey squares)
    'B': {'size': 30, 'x_start': 300, 'y': 450, 'color': GREY},   # Group B (grey squares)
    'C': {'size': 20, 'x_start': 550, 'y': 550, 'color': GREY}    # Group C (grey squares)
}

# Function to draw the squares in each group with consistent gaps
def draw_group(label, x_start, y, base_size, color):
    spacing = 15  # Fixed gap between squares
    for i in range(5):
        square_size = base_size - i * 5  # Squares get smaller from left to right
        square_x = x_start + i * (base_size + spacing)  # X position calculated using the initial base size + fixed spacing
        pygame.draw.rect(screen, color, (square_x, y, square_size, square_size))

    # Draw the label above the group
    label_text = font.render(label, True, BLACK)
    screen.blit(label_text, (x_start, y - 40))  # Label above squares

def draw_menu():
    """Display instructions for the user to adjust the speed and size."""
    speed_text = font.render(f'Speed: {circle_speed}', True, BLACK)
    size_text = font.render(f'Size: {circle_radius}', True, BLACK)
    instructions_speed = font.render('Press UP/DOWN to adjust speed', True, BLACK)
    instructions_size = font.render('Press LEFT/RIGHT to adjust size', True, BLACK)
    
    # Draw the text onto the screen
    screen.blit(speed_text, (10, 10))
    screen.blit(size_text, (10, 50))
    screen.blit(instructions_speed, (10, 90))
    screen.blit(instructions_size, (10, 130))

# Main game loop
while True:
    # Handle events (e.g., quitting and adjusting speed/size)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Adjust speed based on UP and DOWN arrow presses
            if event.key == pygame.K_UP:
                circle_speed += 1  # Increase speed
            elif event.key == pygame.K_DOWN and circle_speed > 1:
                circle_speed -= 1  # Decrease speed

            # Adjust size based on LEFT and RIGHT arrow presses
            if event.key == pygame.K_RIGHT:
                circle_radius += 5  # Increase the radius
            elif event.key == pygame.K_LEFT and circle_radius > 5:
                circle_radius -= 5  # Decrease the radius (min size = 5)

        # Handle window resize event
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            circle_y = event.h // 2  # Keep the circle vertically centered when resizing

    # Move the circle by updating the x-coordinate
    circle_x += direction * circle_speed

    # Check if the circle hits the screen's right boundary
    if circle_x >= screen.get_width() - circle_radius:  # Right boundary
        circle_x = screen.get_width() - circle_radius  # Ensure the circle stays at the boundary
        pygame.display.flip()  # Update display to show the circle at the edge
        time.sleep(pause_duration)  # Pause momentarily
        direction = -1  # Switch to moving left

    # Check if the circle hits the screen's left boundary
    elif circle_x <= circle_radius:  # Left boundary
        circle_x = circle_radius  # Ensure the circle stays at the boundary
        pygame.display.flip()  # Update display to show the circle at the edge
        time.sleep(pause_duration)  # Pause momentarily
        direction = 1  # Switch to moving right

    # Fill the screen with dull green to erase the previous frame
    screen.fill(DULL_GREEN)

    # Draw the circle
    pygame.draw.circle(screen, GREY, (circle_x, circle_y), circle_radius)

    # Draw the groups of squares (A, B, and C) below the circle
    for label, group in groups.items():
        draw_group(label, group['x_start'], group['y'], group['size'], group['color'])

    # Display the menu for adjusting speed and size
    draw_menu()

    # Update the display
    pygame.display.flip()

    # Set the frame rate (60 frames per second)
    pygame.time.Clock().tick(60)
