import random

from dla.simulation_type import SimulationType
from image.image import Image


class DLA:
    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the DLA simulation.

        Args:
            width (int): Width of the simulation grid.
            height (int): Height of the simulation grid.
        """
        self.width = width
        self.height = height
        self.sim_data = Image(self.width, self.height)
        self.sim_data.clear((255, 255, 255, 255))
        self.output_image = Image(self.width, self.height, (128, 128, 128, 255))

    def save_image(self, file_name: str) -> None:
        """
        Save the current simulation output image to a file.

        Args:
            file_name (str): Path of the file to write to.
        """
        self.output_image.save(file_name)

    def random_seed(self) -> None:
        """
        Place a random seed inside the boundary with a=0
        """
        x, y = self._start_placement()
        self.sim_data.set_pixel(x, y, (255, 255, 255, 0))

    def set_seed(self, x: int, y: int) -> None:
        """
        Place a seed pixel at a specific position.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
        """
        self.sim_data.set_pixel(x, y, (255, 255, 255, 0))

    def _start_placement(self) -> tuple[int, int]:
        """
        Choose a random starting position for a particle.

        Returns:
            tuple[int, int]: A valid (x, y) coordinate inside the inner boundary.
        """
        x = random.randint(1, self.width - 2)
        y = random.randint(1, self.height - 2)
        return x, y

    def walk(self) -> bool:
        """
        Perform one random walker simulation step.

        Returns:
            bool: True if the walker found and attached to a seed,
                  False if it hit the edge and was discarded.
        """
        walking = True
        found = False

        x, y = self._start_placement()

        # Loop until we either hit an edge or find a seed
        while walking:
            x += random.choice([-1, 0, 1])
            y += random.choice([-1, 0, 1])

            # Check bounds and quit if edge is hit
            if x < 1 or x >= self.width - 1 or y < 1 or y >= self.height - 1:
                print("Hit edge")
                walking = False
                found = False
                break
            else:
                for x_offset in [-1, 0, 1]:
                    for y_offset in [-1, 0, 1]:
                        pixel_color = self.sim_data.get_pixel(
                            x + x_offset, y + y_offset
                        )

                        if pixel_color[3] == 0:
                            print("Found seed")
                            self.sim_data.set_pixel(
                                x,
                                y,
                                random.choice(
                                    [(255, 0, 0, 0), (0, 255, 0, 0), (0, 0, 255, 0)]
                                ),
                            )
                            self.output_image.set_pixel(x, y, (0, 0, 255, 255))

                            found = True
                            walking = False
                            break
        return found
