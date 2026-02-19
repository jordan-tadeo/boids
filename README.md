# Boids

A real-time boids (flocking) simulation built with Python and Pygame.

The simulation models emergent flock behavior from three simple local rules:
- separation (avoid crowding nearby boids)
- alignment (match nearby boid velocity)
- cohesion (move toward nearby boid center)

Reference: [Stanford overview of Boids](https://cs.stanford.edu/people/eroberts/courses/soco/projects/2008-09/modeling-natural-systems/boids.html#:~:text=Boids%20is%20an%20artificial%20life,behavior%20of%20each%20individual%20bird.)

![Boids simulation](https://github.com/jordan-tadeo/boids/blob/main/img/boid_simulation.gif)

## Features

- 2D flock simulation at 60 FPS
- Wraparound world edges (infinite-space effect)
- Heading-based boid rendering with smooth rotation
- Adjustable flocking constants for behavior tuning

## Requirements

- Python 3.12+
- Pygame 2.6+

This project includes a `pyproject.toml` and `uv.lock`, so you can run with either `uv` or `pip`.

## Quick Start

### Option 1: `uv` (recommended)

```bash
uv sync
uv run python main.py
```

### Option 2: `venv` + `pip`

```bash
python -m venv .venv
source .venv/bin/activate
pip install pygame numpy
python main.py
```

## Controls

- Close the window or press your OS close button to exit.

## Project Layout

```text
boids/
  main.py            # game loop
  src/
    boid.py          # boid state + flocking rules
    world.py         # boid updates, wrapping, drawing
    window.py        # pygame window/display helpers
    utility.py       # lightweight Vector2 implementation
```

## How It Works

Each frame:
1. `main.py` clears the screen and draws all boids.
2. `world.update_all_boid_positions()` updates each boid position and applies flocking acceleration.
3. `world.infinite_edges()` wraps boids at screen boundaries.
4. The display is presented, then frame rate is capped with `clock.tick(60)`.

Core flocking behavior is implemented in `src/boid.py`:
- `separation()`
- `alignment()`
- `cohesion()`
- combined in `three_rules()`

## Tuning Behavior

Edit constants in `src/boid.py`:

- `max_speed`: caps boid speed
- `max_accel`: controls acceleration strength
- `neighbor_range`: radius for neighbor detection
- `separation_range`: minimum spacing threshold
- alignment/cohesion scaling factors inside `alignment()` and `cohesion()`

Small changes can produce very different flock dynamics, so tune incrementally.

## Notes

- Window size is defined in `src/window.py`.
- Boid spawn count is set in `main.py` (`create_boid_list(128)`).
