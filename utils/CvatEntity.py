from typing import List
import json

class Elements(object):
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
    def __init__(self,  elements: List[Elements]=None, label_id: int=None, type: str=None, frame: str=None, group: int=None, source: str=None, occluded: bool=None, outside: bool=None,
                 z_order: int=None, rotation: float=None, points: List=None, attributes: List=None):
        Elements.__init__(self, label_id, type, frame, group, source, occluded, outside,
                 z_order, rotation, points, attributes)
        self.elements = elements

class Annotations(object):
    def __init__(self, shapes: List[Shapes], version: int=0, tags: List=[],tracks: List=[]):
        self.version = version
        self.tags = tags
        self.shapes = shapes
        self.tracks = tracks


if __name__ == "__main__":

    e = Elements()
    e.label_id = 2
    e.type="skeleton"
    e.frame=0
    e.group=0
    e.source="manual"
    e.occluded=False
    e.outside=False
    e.z_order=0
    e.rotation=float(0)
    e.points=[]
    e.attributes=[]

    s = Shapes()
    s.elements = [e]
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


#
#
# {
#     "version": 0,
#     "tags": [],
#     "shapes": [
#         {
#             "id": 4208,
#             "label_id": 1,
#             "type": "skeleton",
#             "frame": 0,
#             "group": 0,
#             "source": "manual",
#             "occluded": false,
#             "outside": false,
#             "z_order": 0,
#             "rotation": 0.0,
#             "points": [],
#             "attributes": [],
#             "elements": [
#                 {
#                     "label_id": 2,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         198.4337465456685,
#                         484.01356055619163
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 3,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         372.91933786202435,
#                         681.2420801239728
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 4,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         151.60489202545068,
#                         522.1213937785524
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 5,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         413.33328631679746,
#                         533.2073076045936
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 6,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         237.56470647053965,
#                         529.0500928833908
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 7,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         334.42988683573014,
#                         531.1287041954092
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 8,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         206.77313540596612,
#                         513.806956433313
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 9,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         367.78741300966857,
#                         517.2713059857322
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 10,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         278.62014919026376,
#                         531.1287041954092
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 11,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         194.58480290640168,
#                         614.2730776478031
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 12,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         376.1267945531532,
#                         614.9659349137526
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 13,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         237.56470647053965,
#                         681.4814336756677
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 14,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         363.29699705588985,
#                         680.7885606040503
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 15,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         265.1488281607974,
#                         478.470603643171
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 16,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         311.33619573287723,
#                         477.77773057155355
#                     ],
#                     "attributes": []
#                 },
#                 {
#                     "label_id": 17,
#                     "type": "points",
#                     "frame": 0,
#                     "group": 0,
#                     "source": "manual",
#                     "occluded": false,
#                     "outside": false,
#                     "z_order": 0,
#                     "rotation": 0.0,
#                     "points": [
#                         287.60102499869936,
#                         495.79234350243325
#                     ],
#                     "attributes": []
#                 }
#             ]
#         }
#     ],
#     "tracks": []
# }