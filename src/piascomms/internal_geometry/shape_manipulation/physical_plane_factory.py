"""
This modules adds physical planes in the ship layout file
"""
import os
from shape_manipulation.xml2dataclasses.physical_planes import PlaneEquation, PhysicalPlanes
from shape_manipulation.xml2dataclasses.xml_utils import ReferenceValues
from internal_geometry.shape_manipulation.boundary_contour_factory import BoundaryVerticeFactory
import datetime
from uuid import uuid4

print(os.getcwd())
class PhysicalPlaneFactory:
    def __init__(self, planes: list, orientation: str, distance: int, boundary_fr_1, boundary_fr_2) -> None:
        self.planes = planes
        self._boundary_fr_1 = boundary_fr_1
        self._boundary_fr_2 = boundary_fr_2
        self.date_format = "%d-%m-%YT%H:%M:%SZ"
        self.date_modified = datetime.datetime.now().strftime(self.date_format)
        self.name = f"{orientation} {distance}"
        self.guuid = uuid4()
        self.plane_id = self.guuid
        plane_type = {
            "longitudinal": [0.000, 1.000, 0.000],
            "transverse": [1.000, 0.000, 0.000],
            "deck": [0.000, 0.000, 1.000]
        }
        self.plane_vector = plane_type.get(orientation)
        self.boundary_factory = BoundaryVerticeFactory(planes=planes, boundary_1=self.bound_1, boundary_2=self.bound_2, orientation=orientation)
        self.distance = ReferenceValues.ReferenceValue(distance)

    @property
    def boundary_contour_vertices(self):
        return self.boundary_factory.set_boundary_vertices()

    @property
    def plane_equation(self):
        return PlaneEquation(
            component_a=self.plane_vector[0], 
            component_b=self.plane_vector[1], 
            component_c=self.plane_vector[2], 
            component_d=ReferenceValues([self.distance]))    

    @property
    def bound_1(self):
        for plane in self.planes:
            if plane.name == self._boundary_fr_1:
                return plane
            elif plane.physical_plane_id == self._boundary_fr_1:
                return plane
            elif plane.physical_plane_guid == self._boundary_fr_1:
                return plane
        raise ValueError(f"{self._boundary_fr_1} not an existing plane.")

    @property
    def bound_2(self):
        for plane in self.planes:
            if plane.name == self._boundary_fr_2:
                return plane
            elif plane.physical_plane_id == self._boundary_fr_2:
                return plane
            elif plane.physical_plane_guid == self._boundary_fr_2:
                return plane
        raise ValueError(f"{self._boundary_fr_2} not an existing plane.")

    def set_physical_plane(self):
        return PhysicalPlanes.PhysicalPlane(
            physical_plane_id=self.plane_id,
            name=self.name,
            last_modification_time=self.date_modified,
            physical_plane_guid=self.guuid,
            plane_equation=self.plane_equation,
            boundary_contour_vertices=self.boundary_contour_vertices
            )


if __name__ == "__main__":
    from xml2dataclasses.physical_planes import physical_planes_from_xml
    from pathlib import Path

    
    empty_layout = Path(r"internal_geometry/shape_manipulation/empty_layout.xml")
    planes = physical_planes_from_xml(xml_path=empty_layout)
    planes = planes.physical_planes.physical_plane

    p = PhysicalPlaneFactory(planes=planes, orientation='transverse', distance=5, boundary_fr_1=5, boundary_fr_2=6 )
    physical_plane = p.set_physical_plane()
    print(physical_plane)
    
    from xsdata.formats.dataclass.serializers import XmlSerializer
    from xsdata.formats.dataclass.serializers.config import SerializerConfig

    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    print(serializer.render(physical_plane))