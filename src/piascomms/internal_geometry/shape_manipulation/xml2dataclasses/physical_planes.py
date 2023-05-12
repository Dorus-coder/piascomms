from dataclasses import dataclass, field
from typing import Optional, List
from .xml_utils import ReferenceValues, ReferenceVectors
# from xml2dataclasses import ReferenceValues
from xsdata.formats.dataclass.parsers import XmlParser

@dataclass
class PlaneEquation:

    component_a: Optional[float] = field(
        default=None,
        metadata={
            "name": "Acomponent",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )
    component_b: Optional[float] = field(
        default=None,
        metadata={
            "name": "Bcomponent",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )
    component_c: Optional[float] = field(
        default=None,
        metadata={
            "name": "Ccomponent",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )
    component_d: Optional[ReferenceValues] = field(
        default=None,
        metadata={
            "name": "Dcomponent",
            "type": "Element",
            'namespace': "",
            "required": True
        }
    )

@dataclass
class BoundaryContourVertices:
    boundary_contour_vertice: List["BoundaryContourVertices.BoundaryContourVertice"] = field(
        default_factory=list,
        metadata={
            "name": "Boundary_contour_vertex",
            "type": "Element",
            "namespace": "",
            "required": True
        }       
    )

    @dataclass
    class BoundaryContourVertice:
        id_physical_plane_1: Optional[int] = field(
        default=None,
        metadata={
            "name": "ID_physical_plane_1",
            "type": "Element",
            "namespace": ""
        }            
        )
        id_physical_plane_2: Optional[int] = field(
        default=None,
        metadata={
            "name": "ID_physical_plane_2",
            "type": "Element",
            "namespace": ""
        }            
        )
        guid_physical_plane_1: Optional[str] = field(
        default=None,
        metadata={
            "name": "GUID_physical_plane_1",
            "type": "Element",
            "namespace": ""
        }            
        )
        guid_physical_plane_2: Optional[str] = field(
        default=None,
        metadata={
            "name": "GUID_physical_plane_2",
            "type": "Element",
            "namespace": ""
        }            
        )
        excluded: Optional[int] = field(
        default=None,
        metadata={
            "name": "Xcluded",
            "type": "Element",
            "namespace": ""
        }            
        )

@dataclass
class PhysicalPlanes:
    physical_plane: List["PhysicalPlanes.PhysicalPlane"] = field(
        default_factory=list,
        metadata={
            "name": "Physical_plane",
            "type": "Element",
            "namespace": ""
        }
    )   
    @dataclass
    class PhysicalPlane:
        physical_plane_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "Physical_plane_ID",
            "type": "Element",
            "namespace": "",
            "required": "",            
        }
    )
        name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
            "required": True,            
        }
    )
        last_modification_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "Last_modification_time",
            "type": "Element",
            "namespace": "",
            "required": True,            
        }
    )           
        physical_plane_guid: Optional[str] = field(
        default=None,
        metadata={
            "name": "Physical_plane_GUID",
            "type": "Element",
            "namespace": "",
            "required": True,            
        }
    )
        plane_equation: Optional[PlaneEquation] = field(
        default=None,
        metadata={
            "name": "Plane_equation",
            "type": "Element",
            "namespace": "",
            "required": True,            
        }
    )      
    
        boundary_contour_vertices: Optional[BoundaryContourVertices] = field(
            default_factory=list,
            metadata={
            "name": "Boundary_contour_vertices",
            "type": "Element",
            "namespace": "",
            "required": True            
            }            
        )     

@dataclass
class ContentCats:
    content_cat: List["ContentCats.ContentCat"] = field(
        default_factory=list,
        metadata={
            "name": "Content_category",
            "type": "Element",
            "namespace": ""
        }
    )   
    @dataclass 
    class ContentCat:
        content_id: Optional[int] = field(
            default = None,
            metadata={
                "name": "Design_content_IDnumber",
                "type": "Element",
                "namespace": ""
            }
        )
        name: Optional[str] = field(
            default = None,
            metadata={
                "name": "Name",
                "type": "Element",
                "namespace": ""
            }
        )

@dataclass
class SubcompartmentShapes:
    subcompartment_shape: List["SubcompartmentShapes.SubcompartmentShape"] = field(
        default_factory=list,
        metadata={
            "name": "Subcompartment_shape",
            "type": "element",
            "namespace": ""
        }
    )

    @dataclass
    class SubcompartmentShape:
        subcompartment_shape_id: Optional[int] = field(
            default=None,
            metadata={
                "name": "Subcompartment_shape_ID",
                "type": "Element",
                "namespace": "",
                "required": False,            
            }
    )
        subcompartment_shape_guuid: Optional[str] = field(
            default=None,
            metadata={
                "name": "Subcompartment_shape_GUID",
                "type": "Element",
                "namespace": "",
                "required": False,            
            }
    )
        Name: Optional[str] = field(
            default=None,
            metadata={
                "name": "Name",
                "type": "Element",
                "namespace": "",
                "required": True,            
            }
    )
        side: Optional[str] = field(
            default=None,
            metadata={
                "name": "Side",
                "type": "Element",
                "namespace": "",
                "required": True,            
            }
    )
        subcompartment_shape_type: Optional[str] = field(
            default="shapetype_derived_from_physical_planes",
            metadata={
                "name": "Subcompartment_shape_type",
                "type": "Element",
                "namespace": "",
                "required": True,            
            }
    )
        geometrical_bsp_id_point: Optional[ReferenceVectors] = field(
            default=None,
            metadata={
                "name": "Geometrical_bsp_identification_point",
                "type": "Element",
                "namespace": "",
                "required": True,            
            }
    )

@dataclass
class Subcompartments:
    subcompartment: List["Subcompartments.Subcompartment"] = field(
            default_factory=list,
            metadata={
                "name": "Subcompartment",
                "type": "Element",
                "namespace": ""
            }        
    )

    @dataclass
    class Subcompartment:
        shape_guid: Optional[str] = field(
            default=None,
            metadata={
                "name": "Shape_GUID",
                "type": "Element",
                "namespace": ""
            }            
        )
        subcomp_guid: Optional[str] = field(
            default=None,
            metadata={
                "name": "Subcompartment_GUID",
                "type": "Element",
                "namespace": ""
            }            
        )
        sign: Optional[str] = field(
            default=None,
            metadata={
                "name": "Sign",
                "type": "Element",
                "namespace": ""
            }            
        )
        permeability_for_tank_volume: Optional[str] = field(
            default=None,
            metadata={
                "name": "Permeability_for_tank_volume",
                "type": "Element",
                "namespace": ""
            }            
        )
        permeability_for_damage_stability: Optional[str] = field(
            default=None,
            metadata={
                "name": "Permeability_for_damage_stability",
                "type": "Element",
                "namespace": ""
            }            
        )

@dataclass
class Compartments:
    compartments: List["Compartments.Compartment"] = field(
        default_factory=list,
        metadata={
            "name": "Compartment",
            "type": "Element",
            "namespace": ""
        }
    )   
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
        output_and_calculations: Optional[bool] = field(
            default =None,
            metadata={
                "name": "Selected_for_output_and_calculations",
                "type": "Element",
                "namespace": ""
            }
        )
        design_density: Optional[float] = field(
            default =None,
            metadata={
                "name": "Design_density",
                "type": "Element",
                "namespace": ""
            }
        )
        subcompartments: Optional[Subcompartments] = field(
            default_factory=list,
            metadata={
                "name": "Subcompartments",
                "type": "Element",
                "namespace": ""
            }
        )

@dataclass
class DeletedPlanes:
    deleted_plane: List["DeletedPlanes.DeletedPlane"] = field(
        default_factory=list,
        metadata={
            "name": "Deleted_physical_plane",
            "type": "Element",
            "namespace": ""
        }
    )
    @dataclass
    class DeletedPlane:
        guid: Optional[str] = field(
            default =None,
            metadata={
                "name": "Deleted_physical_plane",
                "type": "Element",
                "namespace": ""
            }
        )

@dataclass
class ShipDesignType:
    SARC_XML_dictionary_version: Optional[int] = field(
        default=None,
        metadata={
        "Name": "SARC_XML_dictionary_version",
        "type": "Element", 
        }
    )
    
    physical_planes: Optional[PhysicalPlanes] = field(
        default=None,
        metadata={
        "name": "Physical_planes",
        "type": "Element",
        "namespace": "",
        "required": True            
        }            
    )
    deleted_planes: Optional[DeletedPlanes] = field(
        default=None,
        metadata={
        "name": "Deleted_physical_planes",
        "type": "Element",
        "namespace": "",
        "required": False            
        }            
    )

    compartments: Optional[Compartments] = field(
        default=None,
        metadata={
        "name": "Compartments",
        "type": "Element",
        "namespace": "",
        "required": True            
        }            
    ) 
    sub_compartment_shapes: Optional[SubcompartmentShapes] = field(
        default=None,
        metadata={
        "name": "Subcompartment_shapes",
        "type": "Element",
        "namespace": "",
        "required": True            
        }            
    ) 
    content_cats: Optional[ContentCats] = field(
        default=None,
        metadata={
        "name": "Content_categories",
        "type": "Element",
        "namespace": "",
        "required": True            
        }            
    )


@dataclass
class ShipDesign(ShipDesignType):
    class Meta:
        name = "Ship_design"

from typing import Protocol

class Path(Protocol):
    ...

def physical_planes_from_xml(xml_path: Path):
    parser = XmlParser()
    return parser.from_path(xml_path, ShipDesign)
