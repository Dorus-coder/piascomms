from dataclasses import dataclass, field
from internal_geometry.shape_manipulation.physical_plane_factory import PhysicalPlaneFactory
from internal_geometry.shape_manipulation.xml2dataclasses.physical_planes import physical_planes_from_xml, ShipDesign, PhysicalPlanes
from pathlib import Path


@dataclass
class SarcXMLDictVersion:
    version: int = field(default=3)


class ShipYard:
    def __init__(self, origin_file: str, orientation: str, distance: int, boundary_fr_1, boundary_fr_2) -> None:
        self.planes = physical_planes_from_xml(xml_path=Path(origin_file))
        self.list_of_planes = self.planes.physical_planes.physical_plane
        self.__xml_dict_version = SarcXMLDictVersion.version
        self.plane_factory = PhysicalPlaneFactory(
            planes=self.list_of_planes,
            orientation=orientation,
            distance=distance,
            boundary_fr_1=boundary_fr_1,
            boundary_fr_2=boundary_fr_2)

    @property
    def sarc_xml_dict_version(self):
        return self.__xml_dict_version

    @sarc_xml_dict_version.setter
    def sarc_xml_dict_version(self, version: int):
        self.__xml_dict_version = SarcXMLDictVersion(version=version)

    @property
    def updated_list_of_planes(self):
        return PhysicalPlanes(self.list_of_planes + [self.plane_factory.set_physical_plane()])


    def set_ship_design(self):
        return ShipDesign(
            SARC_XML_dictionary_version=self.sarc_xml_dict_version,
            physical_planes=self.updated_list_of_planes,
            compartments=self.planes.compartments,
            sub_compartment_shapes=self.planes.sub_compartment_shapes,
            content_cats=self.planes.content_cats)


if __name__ == "__main__":
    
    ship_design = ShipYard(
        origin_file=r"PiasExampleFiles\example_2\goa1.fromLayout.xml",
        orientation='transverse',
        distance=-45,
        boundary_fr_1=1,
        boundary_fr_2=2
        )

    ship_design_xml_output = ship_design.set_ship_design()

    from xsdata.formats.dataclass.serializers import XmlSerializer
    from xsdata.formats.dataclass.serializers.config import SerializerConfig

    output = Path('PiasExampleFiles\example_2\goa1.toLayout.xml')

    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)

    with output.open('w') as outfile:
        serializer.write(outfile, ship_design_xml_output)

    print(serializer.render(ship_design_xml_output))