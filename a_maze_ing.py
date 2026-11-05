"""
CLI application entry point for the A-Maze-ing.

Handles argument parsing, validates the configuration using Pydantic,
and triggers the maze generation algorithms.
"""
import sys
try:
    from config import MazeConfig, MazeConfigError
    from mazegen import MazeGenerator
    from viewer import CursesViewer
except ImportError as e:
    print(f"Environment Error: Missing dependency '{e.name}'.")
    print("Please ensure you are running the script inside the virtual"
          "environment.")
    print("Use 'uv run python a_maze_ing.py <config_file.txt>'")
    sys.exit(1)


def main() -> None:
    """Executes the main CLI workflow.

    Reads the configuration file provided as a CLI argument, validates the
    data, instantiates the maze generator, and saves the output to disk.

    Raises:
        SystemExit: If arguments are missing, or if the configuration parsing
        or execution fails.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file.txt>")
        sys.exit(1)

    config_filepath = sys.argv[1]

    try:
        config = MazeConfig.from_file(config_filepath)

        # Instantiate the generator
        generator = MazeGenerator(
            width=config.WIDTH,
            height=config.HEIGHT,
            entry_coord=config.ENTRY,
            exit_coord=config.EXIT,
            output_file=config.OUTPUT_FILE,
            perfect=config.PERFECT,
            seed=config.SEED
        )

        # Generate the maze
        generator.generate()

        if config.WIDTH > 50 or config.HEIGHT > 50:
            print("Maze is too large to show in the terminal, "
                  f"check {config.OUTPUT_FILE}")
        else:
            # Launch the interactive terminal visualization
            viewer = CursesViewer(generator)
            viewer.show()

    except MazeConfigError as error:
        # Catch and display our custom parsing errors cleanly
        print(f"Error: {error}", file=sys.stderr)
        return
    except (ValueError, OSError) as operational_error:
        print(f"Execution Error: {operational_error}", file=sys.stderr)
        return
    except Exception as unexpected_error:
        print(f"Unexpected error occurred: {unexpected_error}")
        return


if __name__ == "__main__":
    main()
