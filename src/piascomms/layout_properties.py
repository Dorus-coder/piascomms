import lxml
from .internal_geometry.shape_manipulation.xml2dataclasses.physical_planes import Compartments, PhysicalPlanes
from xsdata.formats.dataclass.parsers.handlers import LxmlEventHandler
from xsdata.formats.dataclass.parsers import XmlParser
from pathlib import Path

class CompartmentData:
    def __init__(self, xml_path: Path):
        self.xml_path = xml_path

    @property
    def list_of_compartments(self):
        parser = XmlParser(handler=LxmlEventHandler)
        tree = lxml.etree.parse(str(self.xml_path))
        return parser.parse(tree.find('.//Compartments'), Compartments).compartments

    @property
    def compartment_names(self):
        return [comp.name for comp in self.list_of_compartments]
    
    @property
    def name_id(self) -> dict:
        return {comp.name: comp.id for comp in self.list_of_compartments}

class PlaneData:
    def __init__(self, xml_path: Path):
        self.xml_path = xml_path

    @property
    def list_of_planes(self):
        parser = XmlParser(handler=LxmlEventHandler)
        tree = lxml.etree.parse(str(self.xml_path))
        return parser.parse(tree.find('.//Physical_planes'), PhysicalPlanes).physical_plane
    
    @property
    def plane_names(self):
        return [plane.name for plane in self.list_of_planes]

