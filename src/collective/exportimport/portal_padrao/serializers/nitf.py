from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from zope.component import adapter, getMultiAdapter
from zope.interface import Interface, implementer

from collective.nitf.interfaces import INITF


@implementer(ISerializeToJson)
@adapter(INITF, Interface)
class NIFTJSONSerializer(SerializeFolderToJson):
    def get_image(self):
        image = self.context.image()
        if image:
            serialized = getMultiAdapter((image, self.request), ISerializeToJson)()
            return serialized["image"]

    def __call__(self, version=None, include_items=True):
        result = super(NIFTJSONSerializer, self).__call__(version, include_items)
        result.update(
            json_compatible(
                {
                    "image": self.get_image(),
                }
            )
        )
        return result
