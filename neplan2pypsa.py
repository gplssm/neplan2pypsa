import pandas as pd
import os
from math import sqrt


names_translations = {
    "lines": {
        "id": 1,
        "csvfile": "lines.csv"},
    "generators": {
        "id": 51,
        "csvfile": "generators.csv"}
}

control_trans = {
    "SL": "Slack",
    "PI": "PQ",
    "IC": "PQ",
    "PC": "PQ",
    "SC": "PQ"
}


def read_edt(file):
    """
    Params:
    file (str): Relative or absolute .edt-file path
    Returns:
        dict of pandas.DataFrame: EDT file data separated by component type
    """

    lines_trans = {
            "name": "c4",
            "bus0": "c1",
            "bus1": "c2",
            "length": "r20",
            "num_parallel": "r15",
            "type_info": "c6"}

    edt = pd.read_csv(file,
                      sep="\t",
                      encoding='iso-8859-1',
                      index_col=False,
                      dtype={"r7": float},
                      decimal=",")

    # Select all lines
    lines_slice = edt[edt["id"] == 1]

    # Only "entire lines" not its segments
    lines_slice = lines_slice[~lines_slice[["c1", "c2"]].isna().any(axis=1)]

    # Rename easily translatable fields
    lines = lines_slice[list(lines_trans.values())].rename(columns={v: k for k, v in lines_trans.items()})

    # Add more fields that require calculations
    lines["r"] = lines_slice["r11"] * lines_slice["r20"]
    lines["x"] = lines_slice["r8"] * lines_slice["r20"]
    lines["s_nom"] = sqrt(3) * lines_slice["r7"] * lines_slice["r1"]
    lines["kind"] = ""

    return lines


def read_ndt(file):
    """
        Params:
        file (str): Relative or absolute .edt-file path
        Returns:
            pandas.DataFrame: NDT file converted to eDisGo compatible bus format
        """

    buses_trans = {
        "name": "c1",
        "control": "c2",
    }

    load_trans = {
        "name": "c3",
        "bus": "c1",
        "power_data_info": "c2",
        "S/P": "r1",
        "Q/cosphi": "r2"
    }

    generator_trans = {
        "name": "c3",
        "bus": "c1",
        "power_data_info": "c2",
        "S/P": "r1",
        "Q/cosphi": "r2"
    }

    ndt_raw = pd.read_csv(file,
                      sep="\t",
                      encoding='iso-8859-1',
                      index_col=False,
                      decimal=",")

    # Split NDT data into load, generator and bus nodes
    load = ndt_raw[(ndt_raw[["r1", "r2"]] > 0).any(axis=1)]
    generator = ndt_raw[(ndt_raw[["r1", "r2"]] < 0).any(axis=1)]
    bus_nodes = ndt_raw.loc[
        [_ for _ in list(ndt_raw.index) if _ not in list(load.index) + list(generator.index)]]

    # Select relevant load data, convert P,Q values, and rename fields
    loads = load[list(load_trans.values())].rename(
        columns={v: k for k, v in load_trans.items()}).set_index("name")
    loads["peak_load"] = loads.apply(_convert_p_nom, axis=1, element="load")
    loads["annual_consumption"] = ""
    loads["sector"] = ""
    loads.drop(["power_data_info", "S/P", "Q/cosphi"], axis=1, inplace=True)

    # Select relevant generator data, convert P,Q values, and rename fields
    generators = generator[list(generator_trans.values())].rename(
        columns={v: k for k, v in generator_trans.items()}).set_index("name")
    generators["p_nom"] = generators.apply(_convert_p_nom, element="generator", axis=1)
    generators["control"] = "PQ"
    generators['type'] = ""
    generators['subtype'] = ""
    generators['weather_cell_id'] = ""
    generators.drop(["power_data_info", "S/P", "Q/cosphi"], axis=1, inplace=True)

    # Select relevant bus data and rename it
    buses = bus_nodes[list(buses_trans.values())].rename(
        columns={v: k for k, v in buses_trans.items()}).set_index("name")
    buses["x"] = ""
    buses["y"] = ""
    buses["mv_grid_id"] = ""
    buses["lv_grid_id"] = ""
    buses["in_building"] = ""
    buses["v_nom"] = 10
    buses.replace({'control': control_trans}, inplace=True)
    buses.replace({'voltage level': {"T": "high voltage", "F": "low voltage"}}, inplace=True)

    # Test if all load and generator data find buses to join
    joinable_load = load.join(buses, on="c1", how="left", rsuffix="bus")
    try:
        assert len(joinable_load) == len(load)
    except AssertionError as e:
        e.args += ("Some loads are missing a bus to join on!", )
        raise

    joinable_generator = generator.join(buses, on="c1", how="left", rsuffix="bus")
    try:
        assert len(joinable_generator) == len(generator)
    except AssertionError as e:
        e.args += ("Some generators are missing a bus to join on!",)
        raise

    return buses, loads, generators


def _convert_p_nom(row, element=None):
    if element is "generator":
        sign = -1
        unit_convert = 1
    elif element is "load":
        sign = 1
        unit_convert = 1e-3


    if row["power_data_info"] == "PQ":
        return sign * unit_convert * row["S/P"]
    elif row["power_data_info"] == "PC":
        return sign * unit_convert* row["S/P"]
    elif row["power_data_info"] == "SC":
        return sign * unit_convert * row["S/P"] * row["Q/cosphi"]
    else:
        raise ValueError("Type {} is unknown!".format(row["power_data_info"]))


def print_data_info(lines, buses):
    """
    Print information about edt and ndt data

    Params:
    lines: dict of pandas.DataFrame
        Processed line data from EDT file
    buses: pandas.DataFrame
        Bus data extracted from NDT data
    """

    lines_two_buses = lines[lines["bus0"].isin(buses.index) & lines["bus1"].isin(buses.index)]

    print("Number of lines with two buses: ",
          len(lines_two_buses),
          " of in total: ",
          len(lines))
    print("Lines with S_nom/v_nom: ", (lines["s_nom"] == 0).value_counts().loc[False])
    print("Total buses: ", len(buses))
    print("Unique buses: ", len(buses.index.unique()))
    print("N/A buses: ", buses.index.isna().sum())


if __name__== "__main__":

    # Define file names
    edt_filename = "10kV_ELE_vorlage_1Sa.edt.txt"
    ndt_filename = "10kV_ELE_vorlage_1Sa.ndt.txt"

    # read data files
    lines = read_edt(edt_filename)
    buses, loads, generators = read_ndt(ndt_filename)

    # Save element and node data to file
    lines.to_csv("lines.csv", index=False)
    buses.to_csv("buses.csv")
    loads.to_csv("loads.csv", index=False)
    generators.to_csv("generators.csv", index=False)

    # Print information about read data
    print_data_info(lines, buses)


