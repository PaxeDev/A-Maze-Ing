"""
Run test with pytest -v
"""
import pytest
from config.parser import MazeConfig
from pathlib import Path
from unittest.mock import patch
from mazegen import MazeGenerator
from mazegen.square import Square


def test_generator_initialization() -> None:
    """Test that MazeGenerator initializes dimensions and grid correctly."""
    raw_data = {
        "WIDTH": "4",
        "HEIGHT": "3",
        "ENTRY": "0,0",
        "EXIT": "3,2",
        "OUTPUT_FILE": "out.txt"
    }
    config = MazeConfig.model_validate(raw_data)

    engine = MazeGenerator(
        width=config.WIDTH,
        height=config.HEIGHT,
        entry_coord=config.ENTRY,
        exit_coord=config.EXIT,
        output_file=config.OUTPUT_FILE
    )

    assert engine.width == 4
    assert engine.height == 3
    assert engine.entry == (0, 0)
    assert engine.exit == (3, 2)

    assert engine.grid == []


def test_export_to_hex_format(tmp_path: Path) -> None:
    """Test the exact output format of the hexadecimal export."""
    fake_output = tmp_path / "test_out.txt"

    raw_data = {
        "WIDTH": "3",
        "HEIGHT": "3",
        "ENTRY": "0,0",
        "EXIT": "1,1",
        "OUTPUT_FILE": str(fake_output)
    }
    config = MazeConfig.model_validate(raw_data)

    maze = MazeGenerator(
        width=config.WIDTH,
        height=config.HEIGHT,
        entry_coord=config.ENTRY,
        exit_coord=config.EXIT,
        output_file=config.OUTPUT_FILE
    )

    # Creating Square objects
    def create_square(val: int) -> Square:
        square = Square()
        square.set_square(number=val)
        return square

    maze.grid = [
        [create_square(15), create_square(10), create_square(15)],
        [create_square(5),  create_square(0),  create_square(10)],
        [create_square(1),  create_square(2),  create_square(4)]
    ]

    maze.export_to_hex()

    content = fake_output.read_text()

    # Expected output ending with 'N' from dummy solve()
    lines = content.split('\n')
    assert lines[0] == "faf"
    assert lines[1] == "50a"
    assert lines[2] == "124"
    assert lines[3] == ""
    assert lines[4] == "0,0"
    assert lines[5] == "1,1"


def test_export_to_hex_dimension_mismatch(tmp_path: Path) -> None:
    """
    Test that exporting a grid with incorrect dimensions raises ValueError.
    """
    fake_output = tmp_path / "test_out.txt"
    raw_data = {
        "WIDTH": "3",
        "HEIGHT": "3",
        "ENTRY": "0,0",
        "EXIT": "1,1",
        "OUTPUT_FILE": str(fake_output)
    }
    config = MazeConfig.model_validate(raw_data)

    maze = MazeGenerator(
        width=config.WIDTH,
        height=config.HEIGHT,
        entry_coord=config.ENTRY,
        exit_coord=config.EXIT,
        output_file=config.OUTPUT_FILE
    )

    def create_square(val: int) -> Square:
        square = Square()
        square.set_square(number=val)
        return square

    # Corrupt grid dimensions artificially
    maze.grid = [[create_square(15)]]

    with pytest.raises(ValueError, match="Grid dimensions do not match"):
        maze.export_to_hex()


def test_export_to_hex_permission_denied(tmp_path: Path) -> None:
    """
    Test that a PermissionError during file open
    is caught and re-raised cleanly.
    """
    fake_output = tmp_path / "test_out.txt"
    raw_data = {
        "WIDTH": "3",
        "HEIGHT": "3",
        "ENTRY": "0,0",
        "EXIT": "1,1",
        "OUTPUT_FILE": str(fake_output)
    }
    config = MazeConfig.model_validate(raw_data)

    maze = MazeGenerator(
        width=config.WIDTH,
        height=config.HEIGHT,
        entry_coord=config.ENTRY,
        exit_coord=config.EXIT,
        output_file=config.OUTPUT_FILE
    )

    def create_square(val: int) -> Square:
        square = Square()
        square.set_square(number=val)
        return square

    maze.grid = [
        [create_square(15), create_square(15), create_square(15)],
        [create_square(15), create_square(15), create_square(15)],
        [create_square(15), create_square(15), create_square(15)]
    ]

    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(OSError,
                           match="Failed to write output file"):
            maze.export_to_hex()
