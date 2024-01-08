from typing import List
import json

class Element(object):
    def __init__(self, label_id: int=None, type: str=None, frame: str=None, group: int=None, source: str=None, occluded: bool=None, outside: bool=None,
                 z_order: int=None, rotation: float=None, points: List=None, attributes: List=None):
        self.label_id = label_id
        self.type = type
        self.frame = frame,
        self.group = group,
        self.source = source,
        self.occluded = occluded,
        self.outside = outside,
        self.z_order = z_order,
        self.rotation = rotation,
        self.points = points,
        self.attributes = attributes

class Shapes(object):
    def __init__(self,  elements: List[Element], label_id: int=None, type: str=None, frame: str=None, group: int=None, source: str=None, occluded: bool=None, outside: bool=None,
                 z_order: int=None, rotation: float=None, points: List=None, attributes: List=None):
        Element.__init__(self, label_id, type, frame, group, source, occluded, outside,
                 z_order, rotation, points, attributes)
        self.elements = elements

class Annotations(object):
    def __init__(self, shapes: List[Shapes], version: int=0, tags: List=[],tracks: List=[]):
        self.version = version
        self.tags = tags
        self.shapes = shapes
        self.tracks = tracks


if __name__ == "__main__":

    l = []

    e = Element()
    e.label_id = 2
    e.type="skeleton"
    e.frame=0
    e.group=0
    e.source="manual"
    e.occluded=False
    e.outside=False
    e.z_order=0
    e.rotation=float(0)
    e.points=[252.0815176461926,
              61.27675985730022]
    e.attributes=[]

    l.append(e)

    b = Element()
    b.label_id = 2
    b.type="skeleton"
    b.frame=0
    b.group=0
    b.source="manual"
    b.occluded=False
    b.outside=False
    b.z_order=0
    b.rotation=float(0)
    bpoints=[252.0815176461926,
              61.27675985730022]
    b.attributes=[]

    l.append(b)

    s = Shapes()
    s.elements = l
    s.label_id = 1
    s.type="skeleton"
    s.frame=0
    s.group=0
    s.source="manual"
    s.occluded=False
    s.outside=False
    s.z_order=0
    s.rotation=float(0)
    s.points=[]
    s.attributes=[]

    a = Annotations(shapes=[s])

    json_data = json.dumps(a, default=lambda o: o.__dict__, indent=4)

    print(json_data)
