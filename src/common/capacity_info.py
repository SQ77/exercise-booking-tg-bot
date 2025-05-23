"""
capacity_info.py
Author: https://github.com/lendrixxx
Description: This file defines the CapacityInfo class used to store information of the capacity of a class.
"""

from dataclasses import dataclass


@dataclass
class CapacityInfo:
    """
    Class to store capacity details of a class, including total capacity, remaining
    spots, and waitlist info.

    Attributes:
      - has_info (bool): Indicates if capacity info is available.
      - capacity (int): Total class capacity.
      - remaining (int): Remaining available spots in the class.
      - waitlist_capacity (int): Capacity for waitlisted students.
      - waitlist_reserved (int): Number of waitlisted students already reserved.

    """

    has_info: bool
    capacity: int
    remaining: int
    waitlist_capacity: int
    waitlist_reserved: int

    def __init__(
        self,
        has_info: bool = False,
        capacity: int = 0,
        remaining: int = 0,
        waitlist_capacity: int = 0,
        waitlist_reserved: int = 0,
    ) -> None:
        """
        Initializes the CapacityInfo instance.

        Args:
          - has_info (bool): True if capacity info is available, false otherwise.
          - capacity (int): The total class capacity.
          - remaining (int): The remaining available spots in the class.
          - waitlist_capacity (int): The capacity for waitlisted students.
          - waitlist_reserved (int): The number of waitlisted students already reserved.

        """
        self.has_info = has_info
        self.capacity = capacity
        self.remaining = remaining
        self.waitlist_capacity = waitlist_capacity
        self.waitlist_reserved = waitlist_reserved
