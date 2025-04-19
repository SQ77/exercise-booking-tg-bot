"""
studio_data.py
Author: https://github.com/lendrixxx
Description: This file defines the StudioData class used to store details of a single studio.
"""

from common.studio_location import StudioLocation


class StudioData:
    """
    Class to represent a single studio's details including locations and instructors.

    Attributes:
      - locations (list[StudioLocation]): Locations of the studio.
      - instructors (list[str]): Name of instructors.

    """

    locations: list[StudioLocation]
    instructors: list[str]

    def __init__(self, locations: list[StudioLocation] = [], instructors: list[str] = ["All"]) -> None:
        """
        Initializes the StudioData instance.

        Args:
          - locations (list[StudioLocation]): The list of locations of the studio.
          - instructors (list[str]): The list of instructors of the studio.

        """
        self.locations = locations
        self.instructors = instructors

    def __eq__(self, other: object) -> bool:
        """
        Equality check between the StudioData and another object.

        Args:
          - other (object): The other object to compare.

        Returns:
          bool: True if both objects are equal, false otherwise.

        """
        if not isinstance(other, StudioData):
            return False

        return self.locations == other.locations and self.instructors == other.instructors
