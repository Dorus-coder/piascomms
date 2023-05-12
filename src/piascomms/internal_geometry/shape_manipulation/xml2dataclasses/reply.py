from dataclasses import dataclass, field
from physical_planes import ShipDesignType, Compartments
from typing import Optional, List


# @dataclass
# class Reply:
#     request_type: Optional[str] = field(
#         default=None,
#         metadata={
#         "name": "Request_type",
#         "type": "element",
#         })
#     ship_design: Optional[ShipDesignType] = field(
#         default=None,
#         metadata={
#         "name": "Ship_design",
#         "type": "element"
#         }
#     )
  
@dataclass
class Reply:
    request_type: Optional[str] = field(
        default=None,
        metadata={
        "name": "Request_type",
        "type": "element",
        "required": True
        })
    ship_design: Optional[ShipDesignType] = field(
        default=None,
        metadata={
        "name": "Ship_design",
        "type": "element",
        })
    
@dataclass
class Replies:
    SARC_XML_dictionary_version: Optional[int] = field(
        default=None,
        metadata={
        "Name": "SARC_XML_dictionary_version",
        "type": "Element", 
        }
    )
    xml_replies: Optional[Reply] = field(
        default=None,
        metadata={
        "name": "XML_reply",
        "type": "Element",
        "required": True
        }
    )




@dataclass
class XmlReplies(Replies):
    class Meta:
        name = "XML_reply"

if __name__ == "__main__":
    from pathlib import Path
    from xsdata.formats.dataclass.parsers import XmlParser
    from xsdata.formats.dataclass.context import XmlContext


    # t = Reply(request_type="Export_ship_layout", ship_design=ShipDesignType())
    # r = XmlReplies(SARC_XML_dictionary_version=1, xml_replies=[t])

    # print(r)
    # parser = XmlParser(context=XmlContext())
    xml_path =Path(r"C:\Users\cursist\Dorus\ThesisResearch\recieved_data.xml")
    # layout = parser.from_string(xml_path, XmlReplies)
    # print(layout)

  
    import lxml
    from xsdata.formats.dataclass.parsers.handlers import LxmlEventHandler
    parser = XmlParser(handler=LxmlEventHandler)
    tree = lxml.etree.parse(str(xml_path))
    bill_to = parser.parse(tree.find('.//Compartments'), Compartments)
    print(bill_to)
