"""
This module contains utility functions for Pias communication module.


Author: Dorus Boogaard
created: 10-02-2023
modified: 21-03-2023
"""
from pathlib import Path
from .client import RecievedMessage
from .client import  Client, TranslateReply
from .layout_properties import CompartmentData
from .internal_geometry.shape_manipulation.xml_request import RequestVolume
import re
import json
from dataclasses import is_dataclass, asdict
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def observation_space_by_name(xml_path: Path, names=False) -> dict:
    """
    Arg:
        xml_path (Path): path to layout xml data (from Pias 'Export_ship_layout)
    Return:
        (dict): dict with compartment name, volume, center of gravity
    """


    space = {}
    names = CompartmentData(xml_path).compartment_names
    for name in names:
        client = Client() # sending multiple messages with the same client requires async programming or multithreading, something intresting but something for another time.
        volume = RequestVolume()
        volume.request_type = 'Compute_volume_integrals'
        volume.name = name
        volume_string = volume.to_xml_string()
        client.send_from_stream(volume_string)
        reply = TranslateReply(client.cache_recieved_bytes)
        reply.to_line()
        space[name] = observe_compartment(reply.message)
        sleep(0.3)
    return space

def observation_space_by_id(_range: tuple, max_volume: int):
    space = {}
    for _id in range(*_range):
        client = Client()
        volume = RequestVolume()
        volume.max_volume = max_volume
        volume.id = _id
        client.send_from_stream(volume.to_xml_string())
        reply = TranslateReply(client.cache_recieved_bytes)
        reply.to_line()
        obs_entry = observe_compartment(reply.message)
        if obs_entry.get('volume'):
            space[_id] = obs_entry
        
    if len(space) >= _range[1] - _range[0]:
        logger.warning('The observation space is saturated!!!! Some compartments might be lost.')    

    return space

def observe_compartment(compartment_data: RecievedMessage):
    """
    Arg:
        compartment_data: RecievedMessage object containing query results of Pias Query 
        'Compute_volume_integrals'
    Returns:
        comp_dict: dictionary containing volume, centroid_x and centroid_y of compartment
    """
    
    comp_dict = {}
    find_in = lambda x: float(re.search('>(.*)</', x).group(1))
    for line in compartment_data.recieved_lines:
        if '<volume>' in line.data:
            comp_dict['volume'] = find_in(line.data)
        elif '<B>' in line.data:
            comp_dict['centroid_x'] = find_in(line.data) 
        elif '<H>' in line.data:
            comp_dict['centroid_y'] = find_in(line.data)
        elif '<L>' in line.data:
            comp_dict['centroid_z'] = find_in(line.data)
    return comp_dict

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if is_dataclass(o):
                return asdict(o)
            return super().default(o)

def write_json(file_name: Path, _data, indent=4) -> None:
    if not isinstance(file_name, Path):
        raise TypeError("filename should be of type pathlib.Path")
    file_name = f"{file_name}.json"
    
    with open(file_name, 'w') as outfile:
        for data in _data:
            json_obj = json.dumps(data, cls=EnhancedJSONEncoder, indent=indent)
            outfile.write(json_obj)