"""
This module builds an XML request of type add_physical_plane

author: Dorus Boogaard
"""
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from .xml2dataclasses.physical_planes import ShipDesign, PlaneEquation, BoundaryContourVertices, PhysicalPlanes
from .boundary_contour_factory import boundary_setter, check_plane_id
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class Compartment:
    id: Optional[int] = field(
        default =None,
        metadata={
            "name": "Compartment_ID",
            "type": "Element",
            "namespace": ""
        }
    )
    guid: Optional[str] = field(
        default =None,
        metadata={
            "name": "Compartment_GUID",
            "type": "Element",
            "namespace": ""
        }
    )
    name: Optional[str] = field(
        default =None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": ""
        }
    )

@dataclass
class PhysicalPlane:
    physical_plane_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "physical_plane_ID",
            "type": "Element",
            "namespace": ""
        }            
    )      

@dataclass
class RequestParameters:

    request_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Request_type",
            "type": "Element",
            "namespace": ""
        }            
    )    

    physical_plane: Optional[PhysicalPlane] = field(
        default=None,
        metadata={
            "name": "physical_plane",
            "type": "Element",
            "namespace": ""
        }            
    )   

    plane_equation: Optional[PlaneEquation] = field(
        default=None,
        metadata={
            "name": "plane_equation",
            "type": "Element",
            "namespace": ""
        }            
    )

    boundary_contour_vertices: Optional[BoundaryContourVertices] = field(
        default=None,
        metadata={
            "name": "boundary_contour_vertices",
            "type": "Element",
            "namespace": ""
        }            
    )

    file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "file_name",
            "type": "Element",
            "namespace": ""
        }            
    ) 
    data: Optional[ShipDesign] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": ""
        }                
    ) 

    compartment: Optional[Compartment] = field(
        default=None,
        metadata={
            "name": "compartment",
            "type": "Element",
            "namespace": ""
        }                
    )  
    moulded_form_volume: Optional[int] = field(
        default=None,
        metadata={
            "name": "moulded_form_volume",
            "type": "Element",
            "namespace": ""
        }                
    )


@dataclass
class XmlRequest:
    request_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Request_type",
            "type": "Element",
            "namespace": ""
        }            
    )    
    request_parameters: Optional[RequestParameters] = field(
            default_factory=None,
            metadata={
                "name": "Request_parameters",
                "type": "Element",
                "namespace": ""
            }        
        )
@dataclass 
class Dummy:
    xml_request: List["Dummy.XmlRequest"] = field(
        default=None,
        metadata={
            "name": "XML_request",
            "type": "Element",
            "namespace": ""
        }            
    )   
    @dataclass
    class XmlRequest:
        request_type: Optional[str] = field(
            default=None,
            metadata={
                "name": "Request_type",
                "type": "Element",
                "namespace": ""
            }            
        )    
        request_parameters: Optional[RequestParameters] = field(
                default_factory=list,
                metadata={
                    "name": "Request_parameters",
                    "type": "Element",
                    "namespace": ""
                }        
            )     


@dataclass
class XmlRequests(Dummy):
    class Meta:
        name = 'XML_requests'

CONFIG = SerializerConfig(encoding="UTF-8", xml_version="1.0", pretty_print=True)
SERIALIZER = XmlSerializer(config=CONFIG)

def check_if_plane(planes: list, boundary_vertex: int) -> bool:
        for plane in planes:
            if plane.physical_plane_id == boundary_vertex:
                return plane
        raise ValueError(f"{boundary_vertex} not an existing plane.")

class AddPhysicalPlane:

    def __init__(self, 
                 planes: list,  
                 orientation: str, 
                 distance: float, 
                 boundary_vertices: List[Tuple[int, int]]):
        """
        Args:
            planes (list): list of plane objects. Used for checking the boundary input and for for setting the boundary vertices. Might be over complicated.
            orientation (str): orientation of the plane. Can be "longitudinal", "transverse" or "horizontal"
            distance (float): distance of the plane from the reference plane.
            Boundary_vertices (List[tuple])
        """
        self.planes = planes
        plane_type          = {
            "Longitudinal bulkhead": [0.000, 1.000, 0.000],
            "Frame"                : [1.000, 0.000, 0.000],
            "Deck"                 : [0.000, 0.000, 1.000]
        }
        self.plane_vector   = plane_type.get(orientation)
        self.distance       = distance
        
        for vertex in boundary_vertices:
            if not check_plane_id(self.planes, vertex[0]) or not check_plane_id(self.planes, vertex[1]):
                raise ValueError(f"plane {vertex[0]} or {vertex[1]} does not exist.")
            
        self._boundaries = boundary_setter(boundary_vertices)
        self.orientation = orientation
    
    @property
    def boundary_contour_vertices(self):
        return self._boundaries

    @boundary_contour_vertices.setter
    def boundary_contour_vertices(self, boundary_vertices: List[tuple]) -> BoundaryContourVertices:
        for vertex in boundary_vertices:
            if not check_plane_id(self.planes, vertex[0]) or not check_plane_id(self.planes, vertex[1]):
                raise ValueError(f"plane {vertex[0]} or {vertex[1]} does not exist.")
            
        self._boundaries = boundary_setter(boundary_vertices)

    def set_parameters(self):
        return RequestParameters(plane_equation=self.plane_equation,
                                 boundary_contour_vertices=self.boundary_contour_vertices)

    def add_request(self, request: str='add_physical_plane'):
        return Dummy.XmlRequest(request_type=request,
                          request_parameters=self.set_parameters())

    def set_request(self, request: str = 'add_physical_plane'):
        """
        Suitable for a single request.
        """
        return XmlRequests(xml_request=[self.add_request(request), Dummy.XmlRequest(request_type="save_ship_layout")])
    
    def to_xml_string(self):
        return SERIALIZER.render(self.set_request())
    
    @property
    def plane_equation(self):
        return PlaneEquation(
            component_a=self.plane_vector[0], 
            component_b=self.plane_vector[1], 
            component_c=self.plane_vector[2], 
            component_d=self.distance)   


    def __str__(self):
        d = {'orientation': self.orientation, 'plane equation: ': [self.plane_vector, self.distance], "Boundaries: ": self._boundaries}
        import pprint
        pp = pprint.pformat(d)
        return f"{pp}"



class RequestFactory:
    def __init__(self) -> None:
        self._request_type = ""

    @property
    def request_type(self):
        return self._request_type
    
    @request_type.setter
    def request_type(self, request: str):
        types = ["Import_ship_layout_from_XMLfile", 'Export_ship_layout', 'Compute_volume_integrals', "save_ship_layout", "Remove_physical_plane"]
        if request in types:
            self._request_type = request
        else:
            raise ValueError("request is not an existing request type.")

  
    def set_parameters(self):
        return RequestParameters(request_type=self.request_type)

    def set_request(self) -> None:
        request = XmlRequests.XmlRequest(self.request_type)
        return XmlRequests(xml_request=[request])
    
    def to_xml_string(self):
        return SERIALIZER.render(self.set_request()) 

class RemovePhysicalPlane(RequestFactory):
    def __init__(self, physical_plane_id: int) -> None:
        super().__init__()
        self.request_type = "Remove_physical_plane"
        self.physical_plane_id = physical_plane_id

    def set_parameters(self):
        return RequestParameters(physical_plane=PhysicalPlane(physical_plane_id=self.physical_plane_id))

    def set_request(self):
        request = XmlRequests.XmlRequest(self.request_type, self.set_parameters())
        return XmlRequests(xml_request=[request])


class RequestVolume(RequestFactory):
    def __init__(self) -> None:
        super().__init__()
        self._name = None
        self.id = None
        self.request_type = 'Compute_volume_integrals'
        self.max_volume = 6000
        

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name    

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id

    def compartment(self):
        if self.name:
            return Compartment(name=self.name)
        elif self.id:
              return Compartment(id=self.id)

    def set_parameters(self):
        return RequestParameters(request_type=self.request_type, compartment=self.compartment(), moulded_form_volume=self.max_volume)
    
    def set_request(self) -> None:
        return XmlRequests(xml_request=[XmlRequests.XmlRequest(request_parameters=self.set_parameters())])