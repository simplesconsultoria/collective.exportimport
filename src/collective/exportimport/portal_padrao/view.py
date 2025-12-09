# -*- coding: UTF-8 -*-
import logging

from plone import api
from Products.Five import BrowserView

logger = logging.getLogger(__name__)

TYPES_TO_EXPORT = []


class ExportAll(BrowserView):
    def __call__(self):
        request = self.request
        if not request.form.get("form.submitted", False):
            return self.index()

        portal = api.portal.get()

        export_name = "export_content"
        logger.info("Start {}".format(export_name))
        view = api.content.get_view(export_name, portal, request)
        view.portal_type = []
        view.path = "/".join(portal.getPhysicalPath())
        view.depth = -1
        exported_types = [i["value"] for i in view.portal_types()]
        request.form["form.submitted"] = True
        view(
            portal_type=exported_types,
            include_blobs=1,
            download_to_server=2,
            migration=True,
            write_errors=True,
        )
        logger.info("Finished {}".format(export_name))

        other_exports = [
            "export_relations",
            "export_localroles",
            "export_ordering",
            "export_defaultpages",
            "export_redirects",
        ]
        for export_name in other_exports:
            export_view = api.content.get_view(export_name, portal, request)
            request.form["form.submitted"] = True
            # store each result in var/instance/export_xxx.json
            export_view(download_to_server=True)

        logger.info("Finished export_all")
        # Important! Redirect to prevent infinite export loop :)
        return self.request.response.redirect(self.context.absolute_url())
