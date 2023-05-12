from piascomms.internal_geometry.shape_manipulation.boundary_contour_factory import BoundaryVerticeFactory, boundary_setter
from piascomms.layout_properties import PlaneData
from pathlib import Path
from piascomms.utils import write_json
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

# empty_layout = Path(r"C:\Users\cursist\Dorus\OpenGym\recieved_data.xml")
# planes = PlaneData(empty_layout)
# planes = planes.list_of_planes
# write_json(Path('layout'), planes)


# bound = BoundaryVerticeFactory(planes, planes[4], planes[5], 'transverse')
# boundaries = bound.set_boundary_vertices()
# print(bound.bound_1)
# #### serialize the dataclase
# #### This has to be migrated to its own class

# config = SerializerConfig(pretty_print=True)
# serializer = XmlSerializer(config=config)
# print(serializer.render(boundaries))

vertices = [(5, 4), (5, 3), (6, 3), (5, 4)]

bounds = boundary_setter(vertices)

for bound in bounds.boundary_contour_vertice:
    print(bound)