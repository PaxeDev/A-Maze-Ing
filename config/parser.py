from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ValidationError
from pathlib import Path


class MazeConfigError(Exception):
    """Exception raised for errors in the maze configuration process."""

    pass


class MazeConfig(BaseModel):
    """Container for maze configuration parameters parsed via Pydantic.

    Attributes:
        WIDTH (int): Maze width measured in cells.
        HEIGHT (int): Maze height measured in cells.
        ENTRY (tuple[int, int]): (x, y) coordinates of the entry cell.
        EXIT (tuple[int, int]): (x, y) coordinates of the exit cell.
        OUTPUT_FILE (str): Name of the file where the maze will be exported.
        PERFECT (bool): Whether the maze is perfect (single path, no loops).
        SEED (int | None): Optional random seed for reproducible generation.
    """

    model_config = {"extra": "forbid"}
    WIDTH: int = Field(ge=3, le=1000)
    HEIGHT: int = Field(ge=3, le=1000)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str = Field(min_length=3)
    PERFECT: bool = False
    SEED: int | None = None

    @model_validator(mode='after')
    def validate_boundaries(self) -> 'MazeConfig':
        """Validates entry and exit placement relative to maze boundaries.

        Ensures that entry and exit coordinates fit within the maze dimensions
        and do not point to the exact same cell.

        Returns:
            MazeConfig: The validated configuration instance.

        Raises:
            ValueError: If entry and exit coordinates are identical or fall
                outside grid boundaries.
        """

        if self.ENTRY == self.EXIT:
            raise ValueError("Entry and exit coordinates "
                             "cannot be the same cell.")
        for coord_label, coordinate in [('entry', self.ENTRY),
                                        ('exit', self.EXIT)]:
            x_coord, y_coord = coordinate
            if not (0 <= x_coord < self.WIDTH and 0 <= y_coord < self.HEIGHT):
                raise ValueError(
                        f"{coord_label} coordinates {coordinate} are out of "
                        f"bounds for maze size {self.WIDTH}x{self.HEIGHT}")
        return self

    @field_validator('ENTRY', 'EXIT', mode='before')
    @classmethod
    def convert_to_tuple(cls, raw_value: str) -> tuple[int, int]:
        """Converts a comma-separated string into a coordinate tuple.

        Args:
            raw_value (str): Raw string input representing coordinates,
                e.g., "0,0".

        Returns:
            tuple[int, int]: A tuple containing the parsed (x, y) integer
                coordinates.

        Raises:
            ValueError: If the string cannot be split into exactly two
                valid integers.
        """
        try:
            raw_x, raw_y = raw_value.split(",")
            return (int(raw_x.strip()), int(raw_y.strip()))
        except ValueError:
            raise ValueError("Coordinates must be exactly two integers "
                             f"separated by a comma (got: '{raw_value}')")

    @classmethod
    def from_file(cls, filepath: str) -> 'MazeConfig':
        """Reads a text configuration file and instantiates a MazeConfig.

        Parses key-value pairs from the file path, filtering out comments and
        empty lines, and validates the resulting dictionary using Pydantic.

        Args:
            filepath (str): Path to the configuration text file.

        Returns:
            MazeConfig: Validated maze configuration instance.

        Raises:
            MazeConfigError: If the file cannot be read, contains syntax
                errors, or fails configuration validation.
        """
        config_path = Path(filepath)
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                if config_path.suffix != '.txt':
                    raise MazeConfigError(f"Invalid file: '{config_path}'. "
                                          "Must be a valid <filename>.txt")
                lines = file.readlines()
        except FileNotFoundError:
            raise MazeConfigError("Configuration file "
                                  f"not found: '{config_path}'.")
        except PermissionError:
            raise MazeConfigError("Permissions denied "
                                  f"to read file: '{config_path}'.")
        except UnicodeDecodeError:
            raise MazeConfigError(f"File '{config_path}' is not "
                                  "a valid UTF-8 text file.")

        raw_config_data: dict[str, str] = {}
        for line in lines:
            clean_line = line.split('#')[0].strip()
            if not clean_line or clean_line.startswith('#'):
                continue
            if '=' not in clean_line:
                raise MazeConfigError("Bad syntax in config file "
                                      f"(missing '='): '{clean_line}'")
            config_key, config_value = clean_line.split('=', 1)
            raw_config_data[config_key.strip().upper()] = config_value.strip()
        try:
            return cls.model_validate(raw_config_data)
        except ValidationError as validation_error:
            clean_errors: list[str] = []
            for error_detail in validation_error.errors():
                location_parts = [
                    str(location)
                    for location in error_detail["loc"]
                    if location != "__root__"]

                field_name = " -> ".join(location_parts)

                error_message = str(error_detail["msg"])
                if error_message.startswith("Value error, "):
                    error_message = error_message[len("Value error, "):]

                if field_name:
                    clean_errors.append(f"  - {field_name}: {error_message}")
                else:
                    clean_errors.append(f"  - {error_message}")

            formatted_summary = "\n".join(clean_errors)
            raise MazeConfigError("Invalid configuration "
                                  f"data:\n{formatted_summary}")
