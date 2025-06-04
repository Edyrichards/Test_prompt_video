"""Simple unit tests for the pipeline."""
from pathlib import Path

from core.script_generator import generate_script


def test_script_generation():
    segs = generate_script("a cat jumps over a wall", "exciting", model="hf-internal-testing/tiny-random-gpt2")
    assert len(segs) == 6


if __name__ == "__main__":
    test_script_generation()
    print("All tests passed")
