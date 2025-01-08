"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
from helpers import cd_to_datetime
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    with open(neo_csv_path) as ncp:
        csv_reader = csv.DictReader(ncp)
        for row in csv_reader:
            designation = row.get("pdes", "").strip()
            name = row.get("name", "").strip() or None
            diameter = row.get("diameter", "").strip()
            hazardous = row.get("pha", "").strip()

            diameter = float(diameter) if diameter else float("nan")
            hazardous = hazardous == "Y"
            neos.append(
                NearEarthObject(
                    designation=designation,
                    name=name,
                    diameter=diameter,
                    hazardous=hazardous,
                )
            )
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    with open(cad_json_path) as cad_johnson:
        data = json.load(cad_johnson)
        fields = data.get("fields", [])
        cad_data = data.get("data", [])

        # Get indices of required fields
        designation_index = fields.index("des")
        time_index = fields.index("cd")
        distance_index = fields.index("dist")
        velocity_index = fields.index("v_rel")

        for approach in cad_data:
            # Extract and handle missing or empty values
            des = approach[designation_index].strip()
            time = approach[time_index]
            distance = (
                float(approach[distance_index].strip())
                if approach[distance_index]
                else 0.0
            )
            velocity = (
                float(approach[velocity_index].strip())
                if approach[velocity_index]
                else 0.0
            )

            # Create CloseApproach object
            approaches.append(
                CloseApproach(
                    _designation=des,
                    time=time,
                    distance=distance,
                    velocity=velocity,
                )
            )
    return approaches
