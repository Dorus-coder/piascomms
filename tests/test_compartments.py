from piascomms.layout_properties import CompartmentData, PlaneData
from piascomms.client import Client, TranslateReply
from piascomms.internal_geometry.shape_manipulation.xml_request import RequestVolume


comp = CompartmentData(r"C:\Users\cursist\Dorus\ThesisResearch\recieved_data.xml")
plane = PlaneData(r"C:\Users\cursist\Dorus\OpenGym\recieved_data.xml")
requested_comp = comp.compartment_names[7]

client = Client() # sending multiple messages with the same client requires async programming or multithreading, something intresting but something for another time.
volume = RequestVolume()
volume.request_type = 'Compute_volume_integrals'
volume.name = requested_comp
volume_string = volume.to_xml_string()
client.send_from_stream(volume_string)
reply = TranslateReply(client.cache_recieved_bytes)
reply.to_line()
volume = reply.message.recieved_lines



# print(f"{plane.list_of_planes = }")
print("#"*50)
print(f"{comp.compartment_names = }")	
print("#"*50)
print(f"{volume = }")
for line in reply.message.recieved_lines:
    print(line.data)
