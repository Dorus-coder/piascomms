from piascomms.internal_geometry.shape_manipulation.xml_request import AddPhysicalPlane, RequestFactory
from piascomms.client import Client, TranslateReply
from pathlib import Path
import time 


def save_layout():
    save = RequestFactory()
    save.request_type = "save_ship_layout"
    data_for_client = save.to_xml_string()


    client = Client()
    client.send_from_stream(data_for_client)
    reply = TranslateReply(client.cache_recieved_bytes)
    reply.to_line()

def request_layout():
    
    ship_layout = RequestFactory()
    ship_layout.request_type = "Export_ship_layout"
    ship_layout_request_string = ship_layout.to_xml_string()

    client = Client()
    start = time.time()
    client.send_from_stream(ship_layout_request_string)
    end = time.time()
    delta = end - start
    minutes = int(delta // 60)
    seconds = delta % 60
    print(f"process took {minutes}:{seconds:.2f}")
    reply = TranslateReply(client.cache_recieved_bytes)
    reply.to_line()

    xml_path = Path("recieved_data.xml")
    with xml_path.open('w') as outfile:
        for line in reply.message.recieved_lines:
            outfile.write(line.data)


request_layout()