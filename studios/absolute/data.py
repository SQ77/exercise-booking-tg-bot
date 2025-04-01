"""
data.py
Author: https://github.com/lendrixxx
Description: This file contains data used for retrieving Absolute schedules.
"""
from common.studio_location import StudioLocation
from common.studio_type import StudioType

# Dictionary of studio locations and params used in get request
LOCATION_MAP = {
  StudioLocation.Centrepoint: 1,
  StudioLocation.StarVista: 2,
  StudioLocation.MilleniaWalk: 3,
  StudioLocation.i12: 5,
  StudioLocation.GreatWorld: 6,
  StudioLocation.Raffles: 8,
}

# Dictionary of location strings from response and studio locations
RESPONSE_LOCATION_TO_STUDIO_LOCATION_MAP = {
  "The Centrepoint (CTP)": StudioLocation.Centrepoint,
  "The Star Vista (STV)": StudioLocation.StarVista,
  "Millenia Walk (MW)": StudioLocation.MilleniaWalk,
  "i12 Katong (KTG)": StudioLocation.i12,
  "Great World (GW)": StudioLocation.GreatWorld,
  "Raffles Place (RP)": StudioLocation.Raffles,
}

# Dictionary of room IDs and studio types
ROOM_ID_TO_STUDIO_TYPE_MAP = {
  "2318746084081403485": StudioType.AbsolutePilates, # Centrepoint Wunda Chair
  "831322535101466334": StudioType.AbsolutePilates,  # Centrepoint Reformer Room 1
  "1180495114737288579": StudioType.AbsolutePilates, # Centrepoint Reformer Room 2
  "816664672039076934": StudioType.AbsoluteSpin,     # Centrepoint Ride

  "831322688713656132": StudioType.AbsolutePilates,  # i12 Reformer Room 1
  "2049314421699774164": StudioType.AbsolutePilates, # i12 Reformer Room 2
  "1120160541927540298": StudioType.AbsoluteSpin,    # i12 Ride

  "1666936824318133997": StudioType.AbsolutePilates, # Star Vista Reformer
  "831321640959739033": StudioType.AbsoluteSpin,     # Star Vista Ride

  "2062965464820090493": StudioType.AbsolutePilates, # Raffles Place Reformer Room 1
  "2062965605622876053": StudioType.AbsolutePilates, # Raffles Place Reformer Room 2
  "2062965745611965609": StudioType.AbsoluteSpin,    # Raffles Place Ride

  "1973969112329618498": StudioType.AbsolutePilates, # Great World Reformer

  "979675880630519234": StudioType.AbsoluteSpin, # Millenia Walk Ride
}
