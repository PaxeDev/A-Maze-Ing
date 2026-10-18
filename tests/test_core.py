"""
Run test with pytest -v
"""
import pytest
from mazegen.core import BaseMazeGenerator
from config.parser import MazeConfig
from pathlib import Path
from unittest.mock import patch


def test_base_generator_is_abstract() -> None:
    """Test that BaseMazeGenerator cannot be instantiated directly."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze_output.txt"
    }
    config = MazeConfig.model_validate(raw_data)

    with pytest.raises(TypeError) as error_info:
        BaseMazeGenerator(config)  # type: ignore

    assert "Can't instantiate abstract class" in str(error_info.value)
    assert "generate" in str(error_info.value)
    assert "solve" in str(error_info.value)


def test_child_generator_grid_initialization() -> None:
    """Test that a concrete implementation initializes the grid correctly."""

    # Create a dummy child class that fulfills the contract
    class DummyMazeEngine(BaseMazeGenerator):
        def generate(self) -> None:
            pass

        def solve(self) -> str:
            return "E"

    # Setup a 4x3 maze config
    raw_data = {
        "WIDTH": "4",
        "HEIGHT": "3",
        "ENTRY": "0,0",
        "EXIT": "3,2",
        "OUTPUT_FILE": "out.txt"
    }
    config = MazeConfig.model_validate(raw_data)

    # Instantiate the dummy engine
    engine = DummyMazeEngine(config.WIDTH,
                             config.HEIGHT,
                             config.ENTRY,
                             config.EXIT,
                             config.OUTPUT_FILE)

    # Verify grid dimensions (3 rows, 4 columns)
    assert len(engine.grid) == 3
    assert len(engine.grid[0]) == 4

    # Verify all initial cells are walls (0)
    for row in engine.grid:
        for cell in row:
            assert cell == 15


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

    # 2. Creating Maze
    class DummyMaze(BaseMazeGenerator):
        def generate(self) -> None:
            # Simulate Mazegen
            # 15 = F, 10 = A
            #  5 = 5,  0 = 0
            self.grid = [
                [15, 10, 15],
                [5, 0, 10],
                [1,   2,  4]
            ]

        def solve(self) -> str:
            return "ES"  # East, South

    maze = DummyMaze(config.WIDTH,
                     config.HEIGHT,
                     config.ENTRY,
                     config.EXIT,
                     config.OUTPUT_FILE)
    maze.generate()  # Simulate matrix

    # Our export meethod
    maze.export_to_hex()

    # 4. check file exist and content
    assert fake_output.exists()

    with open(fake_output, 'r', encoding='utf-8') as f:
        content = f.read()

    # Expected output
    expected_content = (
        "faf\n"
        "50a\n"
        "124\n"
        "\n"
        "0,0\t# entry (x,y)\n"
        "1,1\t# exit (x,y)\n"
        "ES\n"
    )

    assert content == expected_content


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

    class CorruptMaze(BaseMazeGenerator):
        def generate(self) -> None:
            self.grid = [[15]]

        def solve(self) -> str:
            return "N"

    maze = CorruptMaze(config.WIDTH,
                       config.HEIGHT,
                       config.ENTRY,
                       config.EXIT,
                       config.OUTPUT_FILE)
    maze.generate()

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

    class ValidMaze(BaseMazeGenerator):
        def generate(self) -> None:
            self.grid = [[15, 15, 15], [15, 15, 15], [15, 15, 15]]

        def solve(self) -> str:
            return "N"

    maze = ValidMaze(config.WIDTH,
                     config.HEIGHT,
                     config.ENTRY,
                     config.EXIT,
                     config.OUTPUT_FILE)
    maze.generate()

    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(OSError,
                           match="Failed to write output file"):
            maze.export_to_hex()
