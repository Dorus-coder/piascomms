from piascomms.layout_properties import PlaneData
from pathlib import Path

source = Path(r"C:\Users\cursist\Dorus\OpenGym\recieved_data.xml")

layout = PlaneData(source).list_of_planes
idx = 5


print(layout[idx])
print(type(layout[idx].boundary_contour_vertices))