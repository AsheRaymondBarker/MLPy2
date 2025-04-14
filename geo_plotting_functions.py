from calendar import day_abbr

import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib.patches import Patch, Circle
from pandas.core.interchange.dataframe_protocol import DataFrame


def translate_geom(df, x, y, scale, rotate):
    """
    Transforms a specified dataset of geometries as specified by params.

    :param df: Geopandas dataframe to be translated. (geopandas.DataFrame)
    :param x: Translation in x. (int/float)
    :param y: Translation in y. (int/float)
    :param scale: By how much the size of the geometry is changed. (int/float)
    :param rotate: By how much the rotation of the geometry is changed. (int/float)
    :return: Translated geopandas dataframe. (geopandas.DataFrame)
    """

    # Translate the geometry.
    df.loc[:, "geometry"] = df.geometry.translate(yoff=y, xoff=x)
    # Find center
    center = df.dissolve().centroid.iloc[0]
    # Scale and rotate around that center.
    df.loc[:, "geometry"] = df.geometry.scale(xfact=scale, yfact=scale, origin=center)
    df.loc[:, "geometry"] = df.geometry.rotate(rotate, origin=center)

    return df


def adjust_maps(df):
    """
    Adjusts the position and scaling of Alaska and Hawaii for a better visualisation.

    :param df: Geopandas dataframe to be adjusted. (geopandas.DataFrame)
    :return: Geopandas dataframe adjusted. (geopandas.DataFrame)
    """

    # Split dataframe.
    df_main_land = df[~df.STATEFP.isin(["02","15","72", "69", "60", "66", "78"])]
    df_marina_islands = df[df.STATEFP == "69"]
    df_amer_samoa = df[df.STATEFP == "60"]
    df_guam = df[df.STATEFP == "66"]
    df_virgin_islands = df[df.STATEFP == "78"]
    df_alaska = df[df.STATEFP == "02"]
    df_hawaii = df[df.STATEFP == "15"]
    df_puerto = df[df.STATEFP == "72"]
    # Transform Alaska and Hawaii.
    df_virgin_islands = translate_geom(df_virgin_islands, -2500000, 300000, 3, 0)
    df_guam = translate_geom(df_guam, 7700000, -5000000, 2, 0)
    df_amer_samoa = translate_geom(df_amer_samoa, 6500000, 1000000, 2, 0)
    df_marina_islands = translate_geom(df_marina_islands, 7400000, -4000000, 2, 70)
    df_puerto = translate_geom(df_puerto, -2500000, 300000, 3, 0)
    df_alaska = translate_geom(df_alaska, 1000000, -4900000, 0.7, 32)
    df_hawaii = translate_geom(df_hawaii, 5400000, -1500000, 1.5, 24)

    return pd.concat([df_main_land, df_alaska, df_hawaii,
                      df_puerto, df_marina_islands, df_amer_samoa, df_guam, df_virgin_islands])


def setup_map():
    """
    Sets up the USA map, loading in county and state data and transforming for best visuals.

    :return: Counties and states Geopandas dataframes. (geopandas.DataFrame, geopandas.DataFrame)
    """

    # Read in counties data.
    counties = gpd.read_file("C:\\Users\\emmot\\DataspellProjects\\ML_Proj2\\cb_2018_us_county_500k")
    # Removing USA overseas territories (e.g. Puerto Rico).
    #counties = counties[~counties.STATEFP.isin(["72", "69", "60", "66", "78"])]
    counties = counties.set_index("GEOID")

    # Read in states data.
    states = gpd.read_file("C:\\Users\\emmot\\DataspellProjects\\ML_Proj2\\cb_2018_us_state_500k")
    # Removing USA overseas territories.
    #states = states[~states.STATEFP.isin(["72", "69", "60", "66", "78"])]

    # Changing map projection.
    counties = counties.to_crs("ESRI:102003")
    states = states.to_crs("ESRI:102003")

    # Adjusting geometries (see adjust_maps).
    counties = adjust_maps(counties)
    states = adjust_maps(states)

    return counties, states


def label_plot(ax):
    label_color = "#4d524d"
    ax.annotate("ALASKA", (-2900000, -900000), size=12, color=label_color, family="monospace")

    ax.annotate("HAWAII", (-500000, -1700000), size=12, color=label_color, family="monospace")

    ax.annotate("PUERTO RICO", (370000, -1600000), size=12, color=label_color, family="monospace")

    ax.annotate("AMERICAN", (-3500000, -400000), size=12, color=label_color, family="monospace")
    ax.annotate("SAMOA", (-3500000, -470000), size=12, color=label_color, family="monospace")

    ax.annotate("GUAM", (-2800000, 0), size=12, color=label_color, family="monospace")

    ax.annotate("NORTHERN", (-3200000, 1200000), size=12, color=label_color, family="monospace")
    ax.annotate("MARIANA", (-3200000, 1130000), size=12, color=label_color, family="monospace")
    ax.annotate("ISLANDS", (-3200000, 1060000), size=12, color=label_color, family="monospace")