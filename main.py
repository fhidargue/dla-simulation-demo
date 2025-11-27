#!/usr/bin/env -S uv run --script

import argparse
from pathlib import Path

from dla.DLA import DLA


def main(output_dir: str, file_name: str, height: int, width: int):
    sim = DLA(args.width, args.height)
    # for _ in range(20):
    #     sim.random_seed()

    for x in range(width):
        sim.set_seed(x, height // 2)

    frame_number = 0
    found_count = 0
    for _ in range(100):
        if sim.walk():
            print("Found a seed")
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
    args = parser.parse_args()

    Path(args.output).mkdir(parents=True, exist_ok=True)
    main(args.output, args.name, args.height, args.width)
