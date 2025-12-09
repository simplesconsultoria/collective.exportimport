import base64

from plone import api
from plone.namedfile.file import NamedBlobImage
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import Interface, implementer

from collective.cover.tiles.base import IPersistentCoverTile


@implementer(ISerializeToJson)
@adapter(IPersistentCoverTile, Interface)
class TileJSONSerializer:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        obj = self.context
        data = obj.data
        tile_name = obj.__name__
        uuid = obj.data.get("uuid", "")
        result = {
            "UID": uuid,
            "type": tile_name,
        }
        for name, value in data.items():
            if isinstance(value, NamedBlobImage):
                value = {
                    "filename": value.filename,
                    "content-type": value.contentType,
                    "data": base64.b64encode(value.data),
                    "encoding": "base64",
                }
            else:
                value = json_compatible(value)
            result[json_compatible(name)] = value
        return result
