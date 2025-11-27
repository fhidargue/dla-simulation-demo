import random
import sys

from Image.src.image import Image, rgba


class DLA:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.sim_data = Image(self.width, self.height)
        self.sim_data.clear((255, 255, 255, 255))
        self.output_image = Image(self.width, self.height, (128, 128, 128, 255))

    def save_image(self, fname: str) -> None:
        self.output_image.save(fname)

    def random_seed(self) -> None:
        """
        Place a random seed inside the boundary with a=0
        """

        x, y = self._random_start()
        self.sim_data.set_pixel(x, y, (255, 255, 255, 0))
        self.output_image.set_pixel(x, y, (0, 255, 0, 255))  # Seeds are now green

    def set_seed(self, x: int, y: int) -> None:
        self.sim_data.set_pixel(x, y, (255, 255, 255, 0))
        self.output_image.set_pixel(x, y, (0, 255, 0, 255))  # Seeds are now green

    def _random_start(self) -> tuple[int, int]:
        x = random.randint(1, self.width - 1)
        y = random.randint(1, self.height - 1)

        return x, y

    def walk(self) -> bool:
        walking = True
        found = False

        x, y = self._random_start()

        # 1 Loop until we either hit an edge or find a seed
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
                        pixel_color = self.sim_data.get_pixel(x + x_offset, y + y_offset)

                        if pixel_color[3] == 0:
                            print("Found seed")
                            self.sim_data.set_pixel(
                                x, y, random.choice([(255, 0, 0, 0), (0, 255, 0, 0), (0, 0, 255, 0)])
                            )
                            self.output_image.set_pixel(x, y, (0, 0, 255, 255))

                            found = True
                            walking = False
                            break
        return found
