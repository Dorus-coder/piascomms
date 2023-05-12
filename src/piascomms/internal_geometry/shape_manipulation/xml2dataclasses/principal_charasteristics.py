from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PrincipalCharacteristics:
    class Meta:
        name = "Principal_characteristics"
    
    length_perpendicular: Optional[str] = field(
        default=None,
        metadata={
            "name": "length_between_perpendiculars",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )
    length_design_waterline: Optional[str] = field(
        default=None,
        metadata={
            "name": "length_design_waterline",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )
    hull_length: Optional[str] = field(
        default=None,
        metadata={
            "name": "hull_length",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )
    moulded_breadth: Optional[str] = field(
        default=None,
        metadata={
            "name": "moulded_breadth",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )
    moulded_depth: Optional[str] = field(
        default=None,
        metadata={
            "name": "moulded_depth",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    ) 
    design_draught: Optional[str] = field(
        default=None,
        metadata={
            "name": "design_draught",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )    
    mean_shell_thickness: Optional[str] = field(
        default=None,
        metadata={
            "name": "mean_shell_thickness",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    ) 
    volume_allowance_for_shell_and_appendages: Optional[str] = field(
        default=None,
        metadata={
            "name": "volume_allowance_for_shell_and_appendages",
            "type": "Element",
            "namespace": "",
            "required": True
        }
    )