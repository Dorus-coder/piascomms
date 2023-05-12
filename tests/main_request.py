from piascomms.internal_geometry.shape_manipulation.xml_request import AddPhysicalPlane, RequestFactory
from piascomms.internal_geometry.shape_manipulation.xml2dataclasses.physical_planes import BoundaryContourVertices 
from piascomms.layout_properties import PlaneData
from pathlib import Path
from piascomms.client import Client, TranslateReply
from collections import namedtuple

example_2 = Path(r"C:\Users\cursist\Dorus\OpenGym\recieved_data.xml")
planes = PlaneData(example_2).list_of_planes

PlaneInfo = namedtuple("PlaneInfo", ["orientation", "upper_limit", "boundary_vertices"])

plane_info = {0: PlaneInfo("Longitudinal bulkhead", 11.5 / 2, [(2, 5), (1, 5), (1, 6), (2, 6), (2, 5)]),
        1: PlaneInfo("Frame", 96, [(5, 4), (5, 3), (6, 3), (6, 4), (5, 4)]),
        2: PlaneInfo("Deck", 10, [(1, 4), (2, 4), (2, 3), (1, 3), (1, 4)])}


plane_type = 0
request = AddPhysicalPlane(planes=planes,
                           orientation=plane_info[plane_type].orientation,
                           distance=-2,
                           boundary_vertices=plane_info[plane_type].boundary_vertices
                           )
data = request.to_xml_string()

ship_layout = RequestFactory()
ship_layout.request_type = "Export_ship_layout"
ship_layout_request_string = ship_layout.to_xml_string()

client = Client()
client.send_from_stream(data)
reply = TranslateReply(client.cache_recieved_bytes)
reply.to_line()

for line in reply.message.recieved_lines:
    print(line.data)

# xml_path = Path("recieved_data.xml")
# with xml_path.open('w') as outfile:
#     for line in reply.message.recieved_lines:
#         outfile.write(line.data)
        
# # print(observation_space(xml_path))
