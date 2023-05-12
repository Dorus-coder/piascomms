from dataclasses import dataclass, field
from typing import Optional, List


@dataclass  
class ReferenceValues:
    reference_value: List['ReferenceValues.ReferenceValue'] = field(
        default=None,
        metadata={
            "name": "Reference_value",
            "type": "Element",
            "required": False 
        }       

    )

    @dataclass
    class ReferenceValue:
        distance: Optional[float] = field(
        default=None,
        metadata={
            "name": "Distance",
            "type": "Element",
            "required": True 
        }             
        )


@dataclass
class Length:
    reference_value: Optional[ReferenceValues] = field(
        default=None,
        metadata={
            "name": "Reference_value",
            "type": "Element",
            "namespace": "",
            "required": True
        }                     
    )

@dataclass
class ReferenceVectors:
    reference_vector: List['ReferenceVectors.ReferenceVector'] = field(
        default=None,
        metadata={
            "name": "Reference_vector",
            "type": "Element",
            "required": "False" 
        }       

    )
    @dataclass
    class ReferenceVector:
        x: Optional[ReferenceValues] = field(
            default=None,
            metadata={
                "name": "L",
                "type": "Element",
                "namespace": "",
                "required": True
            }                       
        )
        y: Optional[ReferenceValues] = field(
            default=None,
            metadata={
                "name": "B",
                "type": "Element",
                "namespace": "",
                "required": True
            }                       
        )
        z: Optional[ReferenceValues] = field(
            default=None,
            metadata={
                "name": "H",
                "type": "Element",
                "namespace": "",
                "required": True
            }                       
        )

@dataclass
class Fustrums:
    fustrum: List["Fustrums.Fustrum"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "" 
        }   
    )

    @dataclass
    class Fustrum:
        class Meta:
            name = "Frustum_point"

        side_num: Optional[str] = field(
            default=None,
            metadata={
                "name": "AftFwd_and_number",
                "type": "Element",
                "namespace": "",
                "required": True
            }             
        )

        reference_vector: Optional[ReferenceVectors] = field(
            default=None,
            metadata={
                "name": "Reference_vector",
                "type": "Element",
                "namespace": "",
                "required": True
            }             
        )