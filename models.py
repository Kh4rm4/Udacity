"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = str(info["designation"])
        self.name = str(info["name"]) if info["name"] else None
        self.diameter = float(info["diameter"]) if info["diameter"] else float("nan")
        self.hazardous = (
            True if info["hazardous"] == "Y" or info["hazardous"] else False
        )

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def sanitize(self):
        """Return a dictionary of all the values inside a NearEarthObject instance."""
        return {
            "designation": str(self.designation),
            "name": str(self.name) if self.name else "",
            "diameter": float(self.diameter),
            "hazardous": bool(self.hazardous),
        }

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return (
            self.designation + " (" + self.name + ")" if self.name else self.designation
        )

    def __str__(self):
        """Return `str(self)`."""
        condition = " not " if not self.hazardous else " "
        output = f"A NearEarthObject {self.fullname} has a diameter of {self.diameter} and is{condition}hazardous."
        return output

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = str(info["_designation"])
        self.time = cd_to_datetime(info["time"]) if info["time"] else None
        self.distance = float(info["distance"]) if info["distance"] else 0.0
        self.velocity = float(info["velocity"]) if info["velocity"] else 0.0

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    def sanitize(self):
        """Return a dictionary of all the values inside a CloseApproach instance."""
        return {
            "_designation": str(self._designation),
            "time": datetime_to_str(self.time),
            "distance": float(self.distance),
            "velocity": float(self.velocity),
            "neo": self.neo.sanitize(),
        }

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return (
            f"At time: {self.time_str}, {self.neo.fullname} approches Earth at "
            + f"a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."
        )

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )
