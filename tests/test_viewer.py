# pyright: reportPrivateUsage=false

import pytest
from unittest.mock import MagicMock, patch
from mazegen.viewer import CursesViewer
from typing import Any


# Environment Setup (Fixture)
@pytest.fixture
def dummy_maze() -> Any:
    """
    Generate a basic simulated maze
    so that the viewer has data to read.
    """
    class DummyConfig:
        HEIGHT = 2
        WIDTH = 2

    class DummyMaze:
        config = DummyConfig()
        # 10 = East/West (1010), 15 = All (1111), 0 = None (0000)
        grid = [[10, 15], [0, 5]]

    return DummyMaze()


# Interface and Keyboard Tests
def test_interactive_loop_state_changes(dummy_maze: Any) -> None:
    """
    Simulates keystrokes and
    verifies that the internal state changes correctly.
    """
    viewer = CursesViewer(dummy_maze)

    # create a fake race screen
    mock_stdscr = MagicMock()

    # program getch() to return 'h',
    # then 'c', and finally 'q' to exit.
    mock_stdscr.getch.side_effect = [ord('h'), ord('c'), ord('q')]

    # check the initial state
    assert viewer.show_path is True
    assert viewer.color_idx == 3

    # run the interactive loop with our fake screen
    with (patch('curses.curs_set'),
          patch('curses.start_color'),
          patch('curses.use_default_colors'),
          patch('curses.init_pair')):  # silence the actual call to curs_set.
        viewer._interactive_loop(mock_stdscr)

    # Comprobamos que el estado ha cambiado tras las pulsaciones fantasma
    assert viewer.show_path is False  # 'h' it had to be changed to False
    assert viewer.color_idx == 4      # 'c' it must from 3 to 4


def test_draw_ui_execution(dummy_maze: Any) -> None:
    """
    Verify that the drawing method executes without coordinate errors.
    """
    viewer = CursesViewer(dummy_maze)
    mock_stdscr = MagicMock()

    viewer.draw_ui(mock_stdscr)

    # verify that the screen was cleared at the start.
    mock_stdscr.clear.assert_called_once()
    # verified that it refreshed upon completion.
    mock_stdscr.refresh.assert_called_once()
    # verify that addstr was called multiple times to draw
    assert mock_stdscr.addstr.call_count > 0
