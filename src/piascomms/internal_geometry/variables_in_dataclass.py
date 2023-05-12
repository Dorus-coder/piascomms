"""
This module containts the Pias variables in dataclasses for the 
purpose of communicating with Pias through XML

@author: Dorus Boogaard
date created: 08-02-2023
date modified:

@co_author:

"""
from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime


@dataclass
class Compartment:
    Compartment_ID: int
    guid: uuid4
    last_modification: datetime
    last_synchronization: datetime
    name: str
    name_2: str
    number_of_subcompartments: int
    abbreviation: str
    array: list
    selected_for_output_and_calculations: bool = True
    design_content_id_number: int = 0
    design_density: float = 1.0
    in_private_color: bool = False
    private_color: str = ""

    def __post_init__(self):
        if len(self.name) > 50:
            raise ValueError(f"The length of the compartment name has a max of 50 characters. name = {self.name}")
        if len(self.name_2) > 50:
            raise ValueError(f"The length of the compartment name has a max of 50 characters. name = {self.name_2}")
        if len(self.abbreviation) > 8:
            raise ValueError(f"The abbreviation has a maximum of 8 characters. abbreviation: {self.abbreviation}")

    

@dataclass
class Subcompartment:
    guid: uuid4
    shape_guid: uuid4
    sign: int = 1
    permeability_for_tank_volume: float = 0.95
    permeability_for_damage_stability: float = 0.98

@dataclass
class Type:
    type: str 

@dataclass
class SubcompartmentShape:
    guid: uuid4
    last_modification: datetime
    last_synchronization: datetime
    name: str
    subcompartment_shape_type: Type
    side: Type
    convertible_between_frustum_and_bsp: bool
    
    def __post_init__(self):
        if self.subcompartment_shape_type == 'shapetype_derived_from_physical_planes':
            ...
        elif self.subcompartment_shape_type == 'shapetype_fustrum':
            ...
        elif self.subcompartment_shape_type == 'shapetype_external_file':
            ...
        else:
            raise ValueError(f"subcompartment shape type {self.subcompartment_shape_type} not known.")
