import random
import pytest

from dla.dla import DLA
from image.image import Image


@pytest.fixture(autouse=True)
def seeded_rng():
    random.seed(12345)


@pytest.fixture
def sim():
    """
    Create a small simulation.
    """
    return DLA(50, 50)


def test_dla_initialization(sim):
    assert sim.width == 50
    assert sim.height == 50
    assert isinstance(sim.sim_data, Image)
    assert isinstance(sim.output_image, Image)

    px = sim.sim_data.get_pixel(10, 10)
    assert px == (255, 255, 255, 255)


def test_set_seed_sets_transparent_pixel(sim):
    sim.set_seed(5, 5)
    pixel = sim.sim_data.get_pixel(5, 5)
    assert pixel[3] == 0


def test_random_seed_places_transparent_pixel(sim):
    sim.random_seed()

    seed_count = 0
    for x in range(sim.width):
        for y in range(sim.height):
            if sim.sim_data.get_pixel(x, y)[3] == 0:
                seed_count += 1

    assert seed_count == 1


def test_start_placement_within_bounds(sim):
    for _ in range(100):
        x, y = sim._start_placement()
        assert 1 <= x < sim.width - 1
        assert 1 <= y < sim.height - 1


def test_walk_returns_bool(sim):
    result = sim.walk()
    assert isinstance(result, bool)


def test_walk_eventually_sticks(sim):
    """
    Walker must stick to a seed eventually.
    """
    sim.set_seed(25, 25)
    attached = False

    for _ in range(200):
        if sim.walk():
            attached = True
            break

    assert attached is True


def test_walk_eventually_hits_edge_or_attaches(sim):
    """
    Ensure walk() never loops forever.
    """
    result = sim.walk()
    assert isinstance(result, bool)


def test_output_image_updates_on_stick(sim):
    sim.set_seed(10, 10)

    before_blue = 0
    for x in range(sim.width):
        for y in range(sim.height):
            if sim.output_image.get_pixel(x, y) == (0, 0, 255, 255):
                before_blue += 1

    for _ in range(300):
        if sim.walk():
            break

    after_blue = 0
    for x in range(sim.width):
        for y in range(sim.height):
            if sim.output_image.get_pixel(x, y) == (0, 0, 255, 255):
                after_blue += 1

    assert after_blue > before_blue

