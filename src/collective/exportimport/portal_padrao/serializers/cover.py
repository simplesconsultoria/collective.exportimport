from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from zope.component import adapter, getMultiAdapter, queryMultiAdapter
from zope.interface import Interface, implementer

from collective.cover.interfaces import ICover
from collective.nitf.interfaces import INITF


@implementer(ISerializeToJson)
@adapter(ICover, Interface)
class CoverJSONSerializer(SerializeFolderToJson):
    def get_tiles(self):
        context_url = self.context.absolute_url()
        tiles = self.context.get_tiles()
        if not tiles:
            return

        # import pdb;pdb.set_trace()
        response = []
        for tile_info in tiles:
            tile_id = tile_info["id"]
            tile_type = str(self.context.get_tile_type(tile_id))
            tile_info["@id"] = "{0}/{1}/{2}".format(
                context_url,
                tile_type,
                tile_id,
            )
            tile = self.context.get_tile(tile_id)
            value = {}
            try:
                serializer = queryMultiAdapter((tile, self.request), ISerializeToJson)
                if serializer:
                    value = serializer()
            except Exception:
                pass
            tile_info.update(value)
            response.append(tile_info)
        return response

    def __call__(self, version=None, include_items=True):
        result = super(CoverJSONSerializer, self).__call__(version, include_items)
        result.update(
            json_compatible(
                {
                    "tiles": self.get_tiles(),
                }
            )
        )
        return result
