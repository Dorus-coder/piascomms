from piascomms.internal_geometry.shape_manipulation.xml_request import RemovePhysicalPlane, AddPhysicalPlane
from piascomms.layout_properties import PlaneData
from piascomms.client import Client
from time import sleep


flag = False
if flag:
    for i in range(7, 30):
        client = Client()
        rplane = RemovePhysicalPlane(physical_plane_id=i)
        data = rplane.to_xml_string()
        client.send_from_stream(data)
        sleep(2)

planes = PlaneData("recieved_data.xml").list_of_planes

request = AddPhysicalPlane(planes, "Frame", -50, 5, 6)

make = True
if make: 
    client = Client()
    data = request.to_xml_string()
    client.send_from_stream(data)
