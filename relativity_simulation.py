import math
import sys
import random
import pygame

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Relativity Simulation")
clock = pygame.time.Clock()

# Load the spaceship image
spaceship = pygame.image.load('pictures/spaceship.png')

# Get the dimensions of the spaceship image
spaceship_width, spaceship_height = spaceship.get_size()

# Set the initial position of the spaceship_rect to the center of the screen
spaceship_rect = spaceship.get_rect(center=(width // 2, height // 2))


def generate_stars(n):
    """Generate a list of stars represented as (x, y, radius) tuples."""
    return [(random.randint(0, width), random.randint(0, height), random.randint(1, 3)) for _ in range(n)]


def generate_planets(n):
    """Generate a list of planets represented as (x, y, radius, color) tuples."""
    colors = [(255, 100, 100), (100, 100, 255), (100, 255, 100)]
    return [(random.randint(0, width), random.randint(0, height), random.randint(10, 30), random.choice(colors)) for _
            in range(n)]


def generate_galaxies(n):
    """Generate a list of galaxies represented as (x, y, radius) tuples."""
    return [(random.randint(0, width), random.randint(0, height), random.randint(30, 50)) for _ in range(n)]


def generate_nebulae(n):
    """Generate a list of nebulae represented as (x, y, radius, color) tuples."""
    return [(random.randint(0, width), random.randint(0, height), random.randint(20, 40),
             (random.randint(50, 200), random.randint(50, 200), random.randint(150, 255))) for _ in range(n)]


def generate_black_holes(n):
    """Generate a list of black holes represented as (x, y, radius) tuples."""
    return [(random.randint(0, width), random.randint(0, height), random.randint(5, 15)) for _ in range(n)]


def update_celestial_objects(objects, speed):
    """Update the positions of celestial objects to simulate movement."""
    updated_objects = []
    for obj in objects:
        x, y, *extra = obj  # Unpack the tuple
        x -= speed  # Move object to the left
        # Respawn at the right if it moves past the left edge of the screen
        if x < 0:
            x = width
            y = random.randint(0, height)
        updated_objects.append((x, y, *extra))  # Pack into a tuple and add to the updated list
    return updated_objects


def draw_celestial_objects(objects, type='star'):
    """Draw stars, planets, galaxies, or nebulae on the screen."""
    for obj in objects:
        if type == 'star':
            x, y, radius = obj
            pygame.draw.circle(screen, (255, 255, 255), (x, y), radius)
        elif type == 'planet':
            x, y, radius, color = obj
            pygame.draw.circle(screen, color, (x, y), radius)
        elif type == 'galaxy':
            x, y, radius = obj
            pygame.draw.circle(screen, (200, 200, 200), (x, y), radius)
        elif type == 'nebula':
            x, y, radius, color = obj
            pygame.draw.circle(screen, color, (x, y), radius)
        elif type == 'black_hole':
            x, y, radius = obj
            pygame.draw.circle(screen, (0, 0, 0), (x, y), radius)


# Function to calculate traveler's time
def traveler_time(relative_velocity, earth_time):
    c = 299792458  # Speed of light in m/s
    v = relative_velocity * c  # Relative velocity as a fraction of light speed
    time_dilation_factor = 1 / math.sqrt(1 - (v ** 2 / c ** 2))
    return earth_time / time_dilation_factor


# Function to calculate the Lorentz factor
def lorentz_factor(relative_velocity):
    c = 299792458
    v = relative_velocity * c
    gamma = 1 / math.sqrt(1 - (v ** 2 / c ** 2))
    return gamma


# Function to update the spaceship image based on the Lorentz factor
def update_spaceship_position(width, height, relative_velocity, original_spaceship, original_position):
    gamma = lorentz_factor(relative_velocity)
    contracted_width = int(original_spaceship.get_width() / gamma)
    contracted_height = original_spaceship.get_height()

    # Calculate the contracted position to keep the spaceship in the middle
    contracted_x = (width - contracted_width) / 2
    contracted_y = (height - contracted_height) / 2

    return contracted_x, contracted_y


# Function to calculate time dilation
def time_dilation(relative_velocity, duration_earth_years):
    c = 299792458  # Speed of light in m/s
    v = relative_velocity * c  # Relative velocity as a fraction of light speed
    time_dilation_factor = 1 / math.sqrt(1 - (v ** 2 / c ** 2))
    return duration_earth_years / time_dilation_factor


# Function to display the time
def display_time(screen, earth_time, traveler_time, position):
    font = pygame.font.Font(None, 36)
    earth_time_text = font.render(f"Earth Time: {earth_time:.2f} years", True, (255, 255, 255))
    traveler_time_text = font.render(f"Traveler's Time: {traveler_time:.2f} years", True, (255, 255, 255))
    screen.blit(earth_time_text, (position[0], position[1]))
    screen.blit(traveler_time_text, (position[0], position[1] + 40))


# Function to display the speedometer
def display_speedometer(screen, relative_velocity, position):
    font = pygame.font.Font(None, 36)
    speed_text = font.render(f"Speed: {relative_velocity * 100:.2f}% of c", True, (255, 255, 255))
    screen.blit(speed_text, position)


# Main function
def main():
    stars = generate_stars(100)  # Generate 100 stars
    planets = generate_planets(5)  # Generate 5 planets
    galaxies = []  # Initialize empty list for galaxies
    nebulae = []  # Initialize empty list for nebulae
    black_holes = generate_black_holes(3)  # Generate 3 black holes

    # Initial relative velocity
    relative_velocity = 0.5

    # Flags to keep track of arrow key presses
    increase_speed = False
    decrease_speed = False
    is_running = False

    earth_time = 0
    time_increment = 0.01
    duration_earth_years = 1000

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Ensure a clean exit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    increase_speed = True
                elif event.key == pygame.K_DOWN:
                    decrease_speed = True
                elif event.key == pygame.K_s:
                    is_running = not is_running
                elif event.key == pygame.K_r:
                    earth_time = 0
                    relative_velocity = 0.5
                    is_running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    increase_speed = False
                elif event.key == pygame.K_DOWN:
                    decrease_speed = False

        # Adjust speed based on arrow key presses
        if increase_speed:
            relative_velocity = min(0.9999, relative_velocity + 0.01)
        elif decrease_speed:
            relative_velocity = max(0, relative_velocity - 0.01)

        if is_running:
            earth_time += time_increment
            if earth_time > duration_earth_years:
                is_running = False

        # Add new galaxies and nebulae with a spawn chance per frame
        if random.random() < 0.0001:
            galaxies.extend(generate_galaxies(1))
        if random.random() < 0.0005:
            nebulae.extend(generate_nebulae(1))

        stars = update_celestial_objects(stars, 1)  # Stars move slowly
        planets = update_celestial_objects(planets, 3)  # Planets move faster
        galaxies = update_celestial_objects(galaxies, 2)  # Galaxies move moderately
        nebulae = update_celestial_objects(nebulae, 1)  # Nebulae move slowly
        black_holes = update_celestial_objects(black_holes, 4)  # Black holes move faster

        # Drawing
        screen.fill((0, 0, 0))  # Black background for space
        draw_celestial_objects(stars, 'star')
        draw_celestial_objects(planets, 'planet')
        draw_celestial_objects(galaxies, 'galaxy')
        draw_celestial_objects(nebulae, 'nebula')
        draw_celestial_objects(black_holes, 'black_hole')

        # Draw the spaceship with resized image
        screen.blit(spaceship, spaceship_rect)

        # Display time and speedometer
        display_time(screen, earth_time, time_dilation(relative_velocity, earth_time), (50, 50))
        display_speedometer(screen, relative_velocity, (50, height - 40))

        # Update spaceship position
        new_position = update_spaceship_position(width, height, relative_velocity, spaceship, (0, 0))
        if new_position is not None:
            spaceship_rect.center = new_position

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
