# piascomms
This package enable python communication with the software suite Pias. The communication module uses Python Socket programming to send XML data with the tcp/ip protocol.

# Installation
The package is not yet registerd on pypi.org. However, the piascomms package will be available through pypi.org in the foreseeable future.

In the mean time, users can install the package in the following way, assuming they have Python and pip installed.

1. In the terminal
``` bash
cd <repo of the project>
```
2. install and create a virtual environment with virtualenv or any other environment/package manager
``` bash
pip install virtualenv
```
``` bash
virtualenv --python="path_to_python_executable version <= python3.10" venv
```
3. Activate virtualenv in the terminal
``` bash
venv\Script\activate
```
4. clone piascomms in the Lib
``` bash
cd venv\lib
```
``` bash
git clone https://github.com/Dorus-coder/piascomms.git
```
5. choose between editable install (development) or build (production)
    
    5.1 editable install
   ``` bash
    pip install -e .
    ```
    5.2 build package
    ``` bash
    pip install build
    ```
    ``` bash
    py -m build
    ```
# Examples

## Adding a physical plane

```python
from piascomms.internal_geometry.shape_manipulation.xml_request import AddPhysicalPlane, RequestFactory
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

# planes types
# 0 == longitudinal bulkhead
# 1 == Frame
# 2 == Deck

plane_type = 0
request = AddPhysicalPlane(planes=planes,
                           orientation=plane_info[plane_type].orientation,
                           distance=-2,
                           boundary_vertices=plane_info[plane_type].boundary_vertices
                           )
data = request.to_xml_string()

client = Client()
client.send_from_stream(data)
reply = TranslateReply(client.cache_recieved_bytes)
reply.to_line()

for line in reply.message.recieved_lines:
    print(line.data)

```
## Removing physical planes

```python
from piascomms.client import Client
from piascomms.internal_geometry.shape_manipulation.xml_request import RemovePhysicalPlane


client = Client()
rplane = RemovePhysicalPlane(physical_plane_id=1)
data = rplane.to_xml_string()
client.send_from_stream(data)
```

## Export ship layout and write xml file

```python
from piascomms.internal_geometry.shape_manipulation.xml_request import RequestFactory
from piascomms.client import Client, TranslateReply
from pathlib import Path


ship_layout = RequestFactory()
ship_layout.request_type = "Export_ship_layout"
ship_layout_request_string = ship_layout.to_xml_string()

client = Client()
client.send_from_stream(ship_layout_request_string)

xml_path = Path("recieved_data.xml")
    with xml_path.open('w') as outfile:
        for line in reply.message.recieved_lines:
            outfile.write(line.data)

```

## Save the ship layout in Pias


```python
from piascomms.internal_geometry.shape_manipulation.xml_request import RequestFactory
from piascomms.client import Client

save = RequestFactory()
save.request_type = "save_ship_layout"
data_for_client = save.to_xml_string()

client = Client()
client.send_from_stream(data_for_client)
```

## Request compartment volume and print to the console

```python
from piascomms.internal_geometry.shape_manipulation.xml_request import RequestVolume
from piascomms.client import Client, TranslateReply

volume = RequestVolume()
volume.name = "compartment name"

client = Client()
client.send_from_stream(volume.to_xml_string())

reply = TranslateReply(client.cache_recieved_bytes)
reply.to_line()

for line in reply.message.recieved_lines:
        print(line.data)
```