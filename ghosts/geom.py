"""Geom module

This module provides tools to manipulate telescope geometries, i.e. shifts and rotations

Todo:
    *

"""
import copy
import pandas as pd
from ghosts.tools import get_vector
from ghosts.geom_config import GEOM_CONFIG_0


def to_panda(geom_config):
    """ Convert a geometry configuration dictionary to a panda data frame

    Parameters
    ----------
    geom_config : `dict`
        a dictionary with shifts and rotations for each optical element

    Returns
    -------
    data_frame : `pandas.DataFrame`
        a `pandas` data frame with shifts and rotations information
    """
    data_frame = pd.DataFrame(data=geom_config)
    return data_frame


def to_dict(geom_frame):
    """ Convert a geometry panda data frame to a dictionary of use with `tweak_optics`

    Parameters
    ----------
    geom_frame : `pandas.DataFrame`
        a `pandas` data frame with shifts and rotations information

    Returns
    -------
    geom_config : `dict`
        a dictionary with shifts and rotations for each optical element
    """
    geom_config = geom_frame.to_dict()
    if 'shifts' in geom_config['geom_id'].keys():
        geom_config['geom_id'] = geom_config['geom_id']['shifts']
    else:
        geom_config['geom_id'] = geom_config['geom_id']['rotations']
    return geom_config


def concat_frames(geom_frame_list):
    """ Concatenates geometry configuration data frames within one table

     Parameters
     ----------
     geom_frame_list : `list` of `pandas.DataFrame`
         a list of geometry configuration data frames

     Returns
     -------
     geom_concat : `pandas.DataFrame`
        a `pandas` data frame with several configurations of shifts and rotations information
     """
    tmp_concat = pd.concat(geom_frame_list)
    geom_concat = tmp_concat.fillna(0)
    geom_concat.sort_values('geom_id')
    return geom_concat


def concat_dicts(geom_dict_list):
    """ Concatenates geometry configuration dictionaries into a data frame

     Parameters
     ----------
     geom_dict_list : `list` of `dict`
         a list of geometry configuration dictionaries

     Returns
     -------
     geom_concat : `pandas.DataFrame`
        a `pandas` data frame with several configurations of shifts and rotations information
     """
    frames = list()
    for one in geom_dict_list:
        frames.append(to_panda(one))
    geom_concat = concat_frames(frames)
    return geom_concat


# Helpers to create a set of geometries translations
def translate_optic(optic_name, axis, distance, geom_id=1000000):
    """ Create a dictionary to translate a piece of optic along an axis

     Parameters
     ----------
    optic_name : `string`
        the name of an optical element
    axis : `string`
        the name of the translation axis, usually y
    distance : `float`
        the value of the shift in meters
    geom_id : `int`
        the id of the new geometry configuration

     Returns
     -------
     geom : `dict`
        a `geom_config` dictionary for the application of the translation
     """
    geom = copy.deepcopy(GEOM_CONFIG_0)
    geom['geom_id'] = geom_id
    geom[optic_name]['shifts'] = get_vector(axis, distance)
    return geom


def rotate_optic(optic_name, axis, angle, geom_id=1000000):
    """ Rotate one optical element of a telescope given a list of Euler angles

    Parameters
    ----------
    optic_name : `string`
        the name of an optical element
    axis : `string`
        the name of the rotation axis, usually y
    angle : `float`
        the values of angle in degrees
    geom_id : `int`
        the id of the new geometry configuration

    Returns
    -------
     geom : `dict`
        a `geom_config` dictionary for the application of the rotation
    """
    geom = copy.deepcopy(GEOM_CONFIG_0)
    geom['geom_id'] = geom_id
    geom[optic_name]['rotations'] = get_vector(axis, angle)
    return geom


def build_translation_set(optic_name, axis, shifts_list, base_id=0):
    """ Build a set of geometries for the given list of translations

    Parameters
    ----------
    optic_name : `string`
        the name of an optical element
    axis : `string`
        the name of the rotation axis, usually y
    shifts_list : `list` of `float`
        the list of distances to scan in meters
    base_id : `int`
        the id of the first geometry configuration created, following ids will be `id+1`

    Returns
    -------
     geoms : `list` of `geom_config`
        a list of geometry configuration dictionaries
    """
    geoms = list()
    for i, shift in enumerate(shifts_list):
        geoms.append(translate_optic(optic_name, axis, shift, geom_id=base_id+i))
    return geoms


def build_rotation_set(optic_name, axis, angles_list, base_id=0):
    """ Build a set of geometries for the given list of rotations

    Parameters
    ----------
    optic_name : `string`
        the name of an optical element
    axis : `string`
        the name of the rotation axis, usually y
    angles_list : `list` of `float`
        the list of angles to scan in degrees
    base_id : `int`
        the id of the first geometry configuration created, following ids will be `id+1`

    Returns
    -------
     geoms : `list` of `geom_config`
        a list of geometry configuration dictionaries
    """
    geoms = list()
    for i, angle in enumerate(angles_list):
        geoms.append(rotate_optic(optic_name, axis, angle, geom_id=base_id+i))
    return geoms
