from typing import Literal, TypeAlias

Info: TypeAlias = Literal[
    "north",
    "east",
    "south",
    "west",
    "visited",
    "number",
    "breakable",
]
Direction: TypeAlias = Literal[
    "north",
    "east",
    "south",
    "west",
]


class Square:
    __north: bool = False
    __east: bool = False
    __south: bool = False
    __west: bool = False
    __visited: bool = False
    __number: int = 15
    __breakable: bool = True

    def set_square(
        self,
        north: bool | None = None,
        east: bool | None = None,
        south: bool | None = None,
        west: bool | None = None,
        visited: bool | None = None,
        number: int | None = None,
        breakable: bool | None = None,
    ) -> None:
        """Update only the parts of the square you choose.

        Every argument is optional, so you can change one value or several
        at once. Anything left as None keeps its current value. For example,
        set_square(north=False) opens the north wall and leaves everything
        else alone.

        Args:
            north: True to close the north wall, False to open it.
            east: True to close the east wall, False to open it.
            south: True to close the south wall, False to open it.
            west: True to close the west wall, False to open it.
            visited: Whether the generator has already been to this square.
            number: The number to store on this square.
            breakable: Whether this square's walls can be removed.
        """
        if north is not None:
            self.__north = north
        if east is not None:
            self.__east = east
        if south is not None:
            self.__south = south
        if west is not None:
            self.__west = west
        if visited is not None:
            self.__visited = visited
        if number is not None:
            self.__number = number
        if breakable is not None:
            self.__breakable = breakable

    def get_info(
        self,
        info: Info,
    ) -> bool | int:
        """Look up one piece of information about the square.

        Tell it what you want to know by name, and it hands back the current
        value. For example, get_info("north") tells you whether the north
        wall is closed.

        Args:
            info: The value to look up. This can be "north", "east", "south",
                "west", "visited", "number" or "breakable".

        Returns:
            The number stored on the square if you ask for "number".
            Otherwise, True or False for the value you asked for.
        """
        match info:
            case "north":
                return self.__north
            case "east":
                return self.__east
            case "south":
                return self.__south
            case "west":
                return self.__west
            case "visited":
                return self.__visited
            case "number":
                return self.__number
            case "breakable":
                return self.__breakable

    def __get_direction(self, direction: Direction) -> int:
        """Turn a direction name into its matching number.

        The directions are numbered clockwise, starting from north. For
        example, "east" gives you 1.

        Args:
            direction: The direction to convert. This can be "north", "east",
                "south" or "west".

        Returns:
            0 for north, 1 for east, 2 for south or 3 for west.
        """
        match direction:
            case "north":
                return 0
            case "east":
                return 1
            case "south":
                return 2
            case "west":
                return 3

    def change_number(
            self,
            direction: Direction
            ) -> None:
        """Mark one wall as open in the square's number.

        The square's number stores all four walls, with one bit for each
        direction: 1 means closed and 0 means open. This function sets the
        bit for the given direction to 0 and leaves the other three alone.
        For example, a fully closed square has the number 15 (1111 in
        binary), and opening its north wall changes that to 14 (1110).

        Args:
            direction: The wall to open. This can be "north", "east", "south"
                or "west".
        """
        number = self.get_info("number")
        bit = self.__get_direction(direction)
        number = number & ~(1 << bit)
        self.set_square(number=number)

    def is_wall_up(
            self,
            direction: Direction
            ) -> bool:
        """Check whether the wall in a given direction is closed.

        The answer comes from the square's number, where each direction has
        its own bit: 1 means closed and 0 means open. For example, if the
        number is 14 (1110 in binary), the north wall is open and the other
        three are closed.

        Args:
            direction: The wall to check. This can be "north", "east",
                "south" or "west".

        Returns:
            True if the wall is closed, or False if it's open.
        """
        number = self.get_info("number")
        # first bit = north
        # second bit = east
        # third bit = south
        # fourth bit = west
        bit = self.__get_direction(direction)
        # create a mask by shifting 1 to the left by `bit`
        mask = 1 << bit

        # check if the result of the bitwise AND is 0
        return (number & mask) != 0
