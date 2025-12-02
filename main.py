#!/usr/bin/env -S uv run --script

import argparse
from pathlib import Path

from dla.dla import DLA
from dla.simulation_type import SimulationType


def main(output_dir: str, file_name: str, height: int, width: int, type: str):
    """
    Run a full Diffusion Limited Aggregation (DLA) simulation.

    Args:
        output_dir (str):
            Directory where all output frames will be saved.
        file_name (str):
            Base name used for output image files.
        height (int):
            Height of the simulation grid.
        width (int):
            Width of the simulation grid.
        type (str):
            Simulation mode as a string. Accepted modes:
                - "center": seeds placed along the horizontal mid-line
                - "top": seeds placed along the top row
                - "bottom": seeds placed along the bottom row
                - "default" or anything else
    """
    sim = DLA(width, height)

    try:
        sim_type = SimulationType(type.lower())
    except ValueError:
        sim_type = SimulationType.DEFAULT

    match sim_type:
        case SimulationType.CENTER:
            for x in range(width):
                sim.set_seed(x, height // 2)
        case SimulationType.TOP:
            for x in range(width):
                sim.set_seed(x, 1)
        case SimulationType.BOTTOM:
            for x in range(width):
                sim.set_seed(x, height - 2)
        case _:
            for _ in range(20):
                sim.random_seed()

    frame_number = 0
    found_count = 0
    for _ in range(10000):
        if sim.walk():
            found_count += 1

            if found_count % 10 == 0:
                file = Path(output_dir) / f"{file_name}.{frame_number:04}.png"
                sim.save_image(str(file))
                frame_number += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple DLA Simulation")
    parser.add_argument("-o", "--output", type=str, default="./", help="output dir defaults to current")
    parser.add_argument("-n", "--name", type=str, default="./", help="output name for the file")
    parser.add_argument("-ht", "--height", type=int, default=400, help="height of the sim")
    parser.add_argument("-w", "--width", type=int, default=400, help="width of the sim")
    parser.add_argument("-t", "--type", type=str, default="random", help="type of simulation (default, center, top, bottom)")
    args = parser.parse_args()

    Path(args.output).mkdir(parents=True, exist_ok=True)
    main(args.output, args.name, args.height, args.width, args.type)
