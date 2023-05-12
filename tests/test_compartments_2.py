from piascomms.utils import observation_space_by_id
from pathlib import Path
from piascomms.client import Client, TranslateReply
from piascomms.internal_geometry.shape_manipulation.xml_request import RequestVolume
import pprint

bad = ['|A|A|A|A|A|A|A|A|A|A|A|A|A|A']

def all_obs():
    data = observation_space_by_id((10, 50), max_volume=7000)
    pp = pprint.pformat(data)
    print(pp)

VAL = []

def single(num):
    global VAL
    client = Client() # sending multiple messages with the same client requires async programming or multithreading, something intresting but something for another time.
    
    volume = RequestVolume()
    volume.name = num
    volume.request_type = 'Compute_volume_integrals'
    # volume.id = numcd pias    
    volume_string = volume.to_xml_string()
    client.send_from_stream(volume_string)
    reply = TranslateReply(client.cache_recieved_bytes)
    reply.to_line()

    val = reply.find_value('volume')
    VAL += [(val, num)]
    print(f"{num = }, {val = }")
    for line in reply.message.recieved_lines:
        print(line.data)


all_obs()