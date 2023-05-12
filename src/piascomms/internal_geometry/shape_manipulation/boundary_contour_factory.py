"""
if the planes is bounded by the two deck frames it is a transverse frame.
the transverse frame is also bounded by the side frames. Subssequently, 
the frame is not bounded by any other transverse frame. This fact that
frames are not bounded by frames with a similair orientation applies to all frames.

The Boundary contour vertices list is made of five vertices but four them are unique (the 
first one is repeated at the end). The vertices hold the two connecting planes at each corner.
"""
from dataclasses import dataclass
from ..shape_manipulation.xml2dataclasses.physical_planes import PhysicalPlanes, BoundaryContourVertices
from pathlib import Path
from typing import List, Tuple

@dataclass
class OuterBoundaries:
    aft: PhysicalPlanes.PhysicalPlane
    fore: PhysicalPlanes.PhysicalPlane
    port: PhysicalPlanes.PhysicalPlane
    starboard: PhysicalPlanes.PhysicalPlane
    bottom: PhysicalPlanes.PhysicalPlane
    top: PhysicalPlanes.PhysicalPlane


class BoundaryVerticeFactory:
    def __init__(self, 
                 planes: list, 
                 boundary_1: PhysicalPlanes.PhysicalPlane, 
                 boundary_2: PhysicalPlanes.PhysicalPlane, 
                 orientation) -> None:
        self.bound_1 = boundary_1
        self.bound_2 = boundary_2
        outer_boundaries = OuterBoundaries(planes[0], planes[1], planes[2], planes[3], planes[4], planes[5])
        connections_with_planes = {"Longitudinal bulkhead": [outer_boundaries.bottom, outer_boundaries.top],
                                    "Frame"               : [outer_boundaries.port, outer_boundaries.starboard],
                                    "Deck"                : [outer_boundaries.port, outer_boundaries.starboard]}
        self.connections_with_planes = connections_with_planes.get(orientation)
        self.planes = planes
        self.old_class()

    def old_class(self):
        raise Warning("The function boundary_setter() has replaced this class.")

    def simple(self):
        boundry_class = BoundaryContourVertices.BoundaryContourVertice
        a = boundry_class(
            id_physical_plane_1=self.bound_1.physical_plane_id,
            id_physical_plane_2=self.connections_with_planes[1].physical_plane_id,
            guid_physical_plane_1=self.bound_1.physical_plane_guid,
            guid_physical_plane_2=self.connections_with_planes[1].physical_plane_guid,
            excluded=2
                        )
        c = boundry_class(
            id_physical_plane_1=self.bound_2.physical_plane_id,
            id_physical_plane_2=self.connections_with_planes[0].physical_plane_id,
            guid_physical_plane_1=self.bound_2.physical_plane_guid,
            guid_physical_plane_2=self.connections_with_planes[0].physical_plane_guid,
            excluded=2
                        )
        return BoundaryContourVertices([a, c]) 
    
    def custom(self):
        boundry_class = BoundaryContourVertices.BoundaryContourVertice

  
    def set_boundary_vertices(self):
        boundry_class = BoundaryContourVertices.BoundaryContourVertice
        a = boundry_class(
            id_physical_plane_1=self.bound_1.physical_plane_id,
            id_physical_plane_2=self.connections_with_planes[1].physical_plane_id,
            guid_physical_plane_1=self.bound_1.physical_plane_guid,
            guid_physical_plane_2=self.connections_with_planes[1].physical_plane_guid,
            excluded=2
                        )
        b = boundry_class(
            id_physical_plane_1=self.bound_1.physical_plane_id,
            id_physical_plane_2=self.connections_with_planes[0].physical_plane_id,
            guid_physical_plane_1=self.bound_1.physical_plane_guid,
            guid_physical_plane_2=self.connections_with_planes[0].physical_plane_guid,
            excluded=2
                        )
        c = boundry_class(
            id_physical_plane_1=self.bound_2.physical_plane_id,
            id_physical_plane_2=self.connections_with_planes[0].physical_plane_id,
            guid_physical_plane_1=self.bound_2.physical_plane_guid,
            guid_physical_plane_2=self.connections_with_planes[0].physical_plane_guid,
            excluded=2
                        )
        d = boundry_class(
            id_physical_plane_1=self.bound_2.physical_plane_id,
            id_physical_plane_2=self.connections_with_planes[1].physical_plane_id,
            guid_physical_plane_1=self.bound_2.physical_plane_guid,
            guid_physical_plane_2=self.connections_with_planes[1].physical_plane_guid,
            excluded=2
                        )
        e = boundry_class(
            id_physical_plane_1=self.bound_1.physical_plane_id,
            id_physical_plane_2=self.connections_with_planes[1].physical_plane_id,
            guid_physical_plane_1=self.bound_1.physical_plane_guid,
            guid_physical_plane_2=self.connections_with_planes[1].physical_plane_guid,
            excluded=2
                        )
        return BoundaryContourVertices([a, b, c, d, e]) 
    

def boundary_setter(vertices: List[Tuple[int, int]]) -> BoundaryContourVertices:
        """
        Arg: 
            vertives List[tuple]: [(plane id 1,plane id 2, excluded=2), ...]
        Return:
            BoundaryContourVertices

        * The vertices should be ordered
        * The orientation should be counter clockwise (right hand rule)
        """
        contour_vertices = []
        for vertex in vertices:
             contour_vertices.append(BoundaryContourVertices.BoundaryContourVertice(
                  id_physical_plane_1=vertex[0],
                  id_physical_plane_2=vertex[1],
                  excluded=2
             ))
        return BoundaryContourVertices(boundary_contour_vertice=contour_vertices)

def check_plane_id(planes: list, plane_id: int) -> bool:
    
    for plane in planes:
        if plane.physical_plane_id == plane_id:
            return True
    
    return False