import sys
try:
    from config import MazeConfig, MazeConfigError
except ImportError as e:
    print(f"Environment Error: Missing dependency '{e.name}'.")
    print("Please ensure you are running the script inside the virtual"
          "environment.")
    print("Use 'uv run python a_maze_ing.py <config_file.txt>'")
    sys.exit(1)


def main() -> None:
    """
    Main entry point for the A-Maze-ing application.
    Handles CLI arguments, triggers configuration parsing,
    and starts the maze generation process.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file.txt>")
        sys.exit(1)

    config_filepath = sys.argv[1]

    try:
        config = MazeConfig.from_file(config_filepath)
        print("Configuration loaded successfully. "
              f"Maze size: {config.WIDTH}x{config.HEIGHT}")
        # 2. Instantiate the generator (Example for the future)
        # generator = DFSMazeGenerator(config)

        # 3. Generate the maze
        # generator.generate()

        # 4. Save the output directly to disk
        # generator.export_to_hex()
        print(f"Maze successfully saved to '{config.OUTPUT_FILE}'.")

    except MazeConfigError as error:
        # Catch and display our custom parsing errors cleanly
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, OSError) as operational_error:
        print(f"Execution Error: {operational_error}", file=sys.stderr)
        sys.exit(1)
    except Exception as unexpected_error:
        print(f"Unexpected error occurred: {unexpected_error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
