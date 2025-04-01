"""
capacity_availability.py
Author: https://github.com/lendrixxx
Description: This file defines the ClassAvailability enum which represents the availability status of a class.
"""
from enum import Enum

class ClassAvailability(str, Enum):
  """
  Enum representing the availability status of a class.
  These values define whether a class is available, waitlisted, full, or cancelled.
  """
  Available = "Available"
  Waitlist = "Waitlist"
  Full = "Full"
  Cancelled = "Cancelled"
  Null = "Null"
