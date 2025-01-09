"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import math
import csv
import json
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for result in results:
            writer.writerow(sanitize_row(result))


def sanitize_row(row):
    """Replace None or NaN values in a row with an empty string."""
    out = [
        ""
        if value is None or (isinstance(value, float) and math.isnan(value))
        else value
        for key, value in row.sanitize().items()
    ]
    new_out = []
    for item in out:
        if item == True:
            item = "True"
        elif item == False:
            item = "False"
        new_out.append(item)
    return new_out


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    data = []
    for close_approach in results:
        data.append(make_dict_from_approach(close_approach))
    with open(filename, "w") as file:
        json.dump(data, file)


def make_dict_from_approach(close_approach):
    """Return a dictionary of all the values inside a CloseApproach instance."""
    return {
        "datetime_utc": datetime_to_str(close_approach.time),
        "distance_au": float(close_approach.distance),
        "velocity_km_s": float(close_approach.velocity),
        "neo": {
            "designation": str(close_approach.neo.designation),
            "name": str(close_approach.neo.name) if close_approach.neo.name else "",
            "diameter_km": float(close_approach.neo.diameter)
            if close_approach.neo.diameter
            else float("NaN"),
            "potentially_hazardous": bool(close_approach.neo.hazardous),
        },
    }
