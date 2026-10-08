from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic import ValidationError
from pathlib import Path


class MazeConfigError(Exception):
    """Exception raised for errors in the maze configuration process."""
    pass


class MazeConfig(BaseModel):
    """Container for the maze configuration parameters using Pydantic.

    Attributes:
        WIDTH (int): Maze width measured in cells.
        HEIGHT (int): Maze height measured in cells.
        ENTRY (tuple[int, int]): (x, y) coordinates of the entry cell.
        EXIT (tuple[int, int]): (x,y) coordinates of the exit cell.
        OUTPUT_FILE (str): Name of the file where the maze will be exported.
        PERFECT (bool): If the maze should be perfect (single path, no loops).
        SEED (int | None): Random seed for maze generation.
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
        """
        Validates that entry and exit coordinates fit within maze dimensions
        and are not the same cell.
        """

        if self.ENTRY == self.EXIT:
            raise ValueError("Entry and exit coordinates "
                             "cannot be the same cell.")
        for name, coord in [('entry', self.ENTRY), ('exit', self.EXIT)]:
            x, y = coord
            if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
                raise ValueError(
                        f"{name} coordinates {coord} are out of bounds "
                        f"for maze size {self.WIDTH}x{self.HEIGHT}"
                        )
        return self

    @field_validator('ENTRY', 'EXIT', mode='before')
    @classmethod
    def convert_to_tuple(cls, value: str) -> tuple[int, int]:
        """Converts a comma-separated string into a tuple of integers."""
        try:
            x, y = value.split(",")
        except ValueError:
            raise ValueError("Coordinates must have exactly two "
                             "values separated by a comma (e.g., '0,1')")
        return (int(x.strip()), int(y.strip()))

    @classmethod
    def from_file(cls, filepath: str) -> 'MazeConfig':
        """Reads the configuration file and creates a MazeConfig instance.

        Args:
            filepath (str): Path to the configuration file.

        Returns:
            MazeConfig: Instance with the extracted parameters.

        Raises:
            MazeConfigError: If the file cannot be read or validation fails.
        """
        path_obj = Path(filepath)
        try:
            with open(path_obj, 'r', encoding='utf-8') as file:
                if path_obj.suffix != '.txt':
                    raise MazeConfigError(f"Invalid file: '{path_obj}'. "
                                          "Must be a valid <filename>.txt")
                lines = file.readlines()
        except FileNotFoundError:
            raise MazeConfigError("Configuration file "
                                  f"not found: '{path_obj}'.")
        except PermissionError:
            raise MazeConfigError("Permissions denied "
                                  f"to read file: '{path_obj}'.")
        except UnicodeDecodeError:
            raise MazeConfigError(f"File '{path_obj}' is not "
                                  "a valid UTF-8 text file.")

        raw_data = {}
        for line in lines:
            clean_line = line.split('#')[0].strip()
            if not clean_line or clean_line.startswith('#'):
                continue
            if '=' not in clean_line:
                raise MazeConfigError("Bad syntax in config file "
                                      f"(missing '='): '{clean_line}'")
            key, value = clean_line.split('=', 1)
            raw_data[key.strip().upper()] = value.strip()
        try:
            return cls.model_validate(raw_data)
        except ValidationError as e:
            raise MazeConfigError(f"Invalid configuration data:\n{e}")
