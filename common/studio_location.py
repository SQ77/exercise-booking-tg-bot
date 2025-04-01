"""
studio_location.py
Author: https://github.com/lendrixxx
Description: This file defines the StudioLocation enum which represents the location of a studio.
"""
from enum import Enum

class StudioLocation(str, Enum):
  """
  Enum representing the location of a studio.
  """
  All = "All"
  Orchard = "Orchard"
  TJPG = "TJPG"
  Bugis = "Bugis"
  Raffles = "Raffles"
  Centrepoint = "Centrepoint"
  i12 = "i12"
  MilleniaWalk = "Millenia Walk"
  StarVista = "Star Vista"
  GreatWorld = "Great World"
  CrossStreet = "Cross Street"
  Robinson = "Robinson"
  Null = "Null"
