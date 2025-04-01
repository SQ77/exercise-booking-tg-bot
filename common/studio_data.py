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
  def __init__(self, locations: list[StudioLocation]=None, instructors: list[str]=None) -> None:
    self.locations = locations
    self.instructors = ["All"] if instructors is None else instructors
