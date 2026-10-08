"""
Run test with pytest -v
"""
from config import MazeConfig, MazeConfigError
from pydantic import ValidationError
import pytest
from pathlib import Path


def test_valid_configuration() -> None:
    """Test with valid data"""

    raw_data = {
        "WIDTH": "15",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "14,9",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }

    config = MazeConfig.model_validate(raw_data)

    assert config.WIDTH == 15
    assert type(config.WIDTH) is int

    assert config.ENTRY == (0, 0)
    assert type(config.ENTRY) is tuple

    assert config.PERFECT is True
    assert type(config.PERFECT) is bool

    assert config.HEIGHT == 10
    assert type(config.HEIGHT) is int

    assert config.EXIT == (14, 9)
    assert type(config.EXIT) is tuple

    assert config.OUTPUT_FILE == "maze_output.txt"
    assert type(config.OUTPUT_FILE) is str

    assert config.SEED is None


def test_coordinates_out_of_bounds() -> None:
    """Test that fails if the coordinates exceed the maze size."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "15,15",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "out of bounds" in str(error_info.value)


def test_same_ENTRY_and_exit() -> None:
    """Test that fails if the coordinates are the same"""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "0,0",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }
    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "cannot be the same cell" in str(error_info.value)


def test_invalid_coordinate_format() -> None:
    """Test that fails if coordinates are missing the comma separator."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "exactly two values separated by a comma" in str(error_info.value)


def test_missing_mandatory_data() -> None:
    """Test that fails if a required field is missing from the config."""
    raw_data = {
        # "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "Field required" in str(error_info.value)
    assert "WIDTH" in str(error_info.value)


def test_coordinates_too_many_commas() -> None:
    """Test that fails if coordinates have extra commas."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "1,,2",
        "EXIT": "9,9,9",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "exactly two values separated by a comma" in str(error_info.value)


def test_forbidden_extra_keys() -> None:
    """Test that fails if unknown or misspelled keys are provided."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true",
        "withd": "15"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "Extra inputs are not permitted" in str(error_info.value)


def test_negative_coordinates() -> None:
    """Test that fails if ENTRY or exit coordinates are negative."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "-1,5",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "out of bounds" in str(error_info.value)


def test_maze_too_small() -> None:
    """
    Test that fails if the maze dimensions are below
    the logical minimum (e.g., 3x3).
    """
    raw_data = {
        "WIDTH": "2",
        "HEIGHT": "2",
        "ENTRY": "0,0",
        "EXIT": "1,1",
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": "true"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "greater than or equal to 3" in str(error_info.value)


def test_from_file_success(tmp_path: Path) -> None:
    """Test that from_file reads a file, ignoring comments and blank lines."""
    config_file = tmp_path / "valid_config.txt"
    config_file.write_text(
        "# Maze Configuration\n"
        "\n"
        "WIDTH = 15\n"
        "HEIGHT = 10\n"
        "ENTRY = 0,0\n"
        "EXIT = 14,9\n"
        "OUTPUT_FILE = maze_output.txt\n"
        "PERFECT = true\n"
        "SEED = 42\n",
        encoding="utf-8"
    )

    config = MazeConfig.from_file(str(config_file))

    assert config.WIDTH == 15
    assert config.SEED == 42
    assert config.OUTPUT_FILE == "maze_output.txt"
    assert config.ENTRY == (0, 0)


def test_from_file_not_found() -> None:
    """Test that from_file raises MazeConfigError when file is missing."""
    with pytest.raises(MazeConfigError) as error_info:
        MazeConfig.from_file("un_archivo_que_no_existe.txt")

    assert "not found" in str(error_info.value)


def test_from_file_invalid_data_raises_custom_error(tmp_path: Path) -> None:
    """
    Test that from_file wraps Pydantic
    ValidationErrors into MazeConfigError.
    """
    config_file = tmp_path / "invalid_config.txt"
    config_file.write_text(
        "WIDTH=2\n"
        "HEIGHT=10\n"
        "ENTRY=0,0\n"
        "EXIT=9,9\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=true\n",
        encoding="utf-8"
    )

    with pytest.raises(MazeConfigError) as error_info:
        MazeConfig.from_file(str(config_file))

    assert "Invalid configuration data" in str(error_info.value)
    assert "WIDTH" in str(error_info.value)


def test_OUTPUT_FILE_too_short() -> None:
    """Test that fails if OUTPUT_FILE is shorter than 3 characters."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "OUTPUT_FILE": "a",
        "PERFECT": "true"
    }

    with pytest.raises(ValidationError) as error_info:
        MazeConfig.model_validate(raw_data)

    assert "String should have at least 3 characters" in str(error_info.value)


def test_coordinates_with_crazy_spaces() -> None:
    """Test that validates stripping spaces from coordinates."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "  0  ,  0  ",
        "EXIT": " 9, 9 ",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "true"
    }

    config = MazeConfig.model_validate(raw_data)

    assert config.ENTRY == (0, 0)
    assert config.EXIT == (9, 9)


def test_from_file_bad_syntax_missing_equals(tmp_path: Path) -> None:
    """Test that fails if a line in the config file is missing an '='."""
    config_file = tmp_path / "bad_syntax_config.txt"
    config_file.write_text(
        "WIDTH=15\n"
        "HEIGHT=10\n"
        "ESTO ES BASURA SIN SIGNO IGUAL\n"
        "ENTRY=0,0\n"
        "EXIT=14,9\n"
        "OUTPUT_FILE=maze_output.txt\n"
        "PERFECT=true\n",
        encoding="utf-8"
    )

    with pytest.raises(MazeConfigError) as error_info:
        MazeConfig.from_file(str(config_file))

    assert "Bad syntax" in str(error_info.value)
    assert "missing '='" in str(error_info.value)


def test_perfect_default_is_false() -> None:
    """Test that PERFECT defaults to False if omitted from config."""
    raw_data = {
        "WIDTH": "10",
        "HEIGHT": "10",
        "ENTRY": "0,0",
        "EXIT": "9,9",
        "OUTPUT_FILE": "maze_output.txt"
        # PERFECT key is intentionally missing
    }

    config = MazeConfig.model_validate(raw_data)

    assert config.PERFECT is False
    assert type(config.PERFECT) is bool
