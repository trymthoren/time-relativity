Relativity Simulation with Pygame
Overview
This project is an interactive simulation built with Python and Pygame that visualizes the effects of relativity, including time dilation and Lorentz contraction, as experienced by a spaceship traveling at relativistic speeds. It's an upgraded version of a previous non-graphical Python script, enhancing the educational experience with visual representations of complex physics phenomena.

Features
Celestial Object Generation: Generates stars, planets, galaxies, nebulae, and black holes to populate the simulation universe.

Relativity Effects Visualization: Visualizes time dilation and Lorentz contraction based on the spaceship's velocity.

Interactive Control: Allows users to control the spaceship's speed using keyboard inputs, exploring the universe at different relativistic speeds.

Dynamic Universe: Celestial objects move and respawn, creating a lively cosmos for exploration.


Installation
To run this simulation, you'll need Python and Pygame installed on your system. Follow these steps to set up your environment:

Ensure you have Python installed. If not, download and install it from python.org.
Install Pygame via pip:

```bash
pip install pygame
```

```bash
python relativity_simulation.py
```

How It Works
The Physics Behind the Simulation
The simulation is grounded in two fundamental concepts of special relativity:

Time Dilation: Demonstrates how time stretches for an observer moving at a significant fraction of the speed of light.

```python
def traveler_time(relative_velocity, earth_time):
    c = 299792458  # Speed of light in m/s
    v = relative_velocity * c
    time_dilation_factor = 1 / math.sqrt(1 - (v ** 2 / c ** 2))
    return earth_time / time_dilation_factor

```

Lorentz Contraction: Visualizes the contraction of space in the direction of motion for objects traveling at relativistic speeds.

```python
def update_spaceship_position(width, height, relative_velocity, original_spaceship, original_position):
    gamma = lorentz_factor(relative_velocity)
    contracted_width = int(original_spaceship.get_width() / gamma)
    return (width - contracted_width) / 2, (height - spaceship.get_height()) / 2

```

Generating the Cosmos
The universe in the simulation is dynamically generated, with functions responsible for creating various celestial objects:

```python
def generate_stars(n):
    return [(random.randint(0, width), random.randint(0, height), random.randint(1, 3)) for _ in range(n)]
```

Navigation and Interaction
Control the spaceship with the UP and DOWN arrow keys to adjust speed and explore the relativistic effects on time and space:

```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            velocity += 0.01
        elif event.key == pygame.K_DOWN:
            velocity -= 0.01

```

Contributing
Contributions to the project are welcome! Whether it's adding new features, improving the physics calculations, or enhancing the visualization, feel free to fork the repository and submit pull requests.

License
This project is open source and available under the MIT License.
