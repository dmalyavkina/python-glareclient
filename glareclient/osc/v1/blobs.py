# Copyright (c) 2016 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from osc_lib.command import command
from oslo_log import log as logging

from glareclient.common import utils as glare_utils

LOG = logging.getLogger(__name__)


class UploadBlob(command.Lister):
    """Upload blob"""

    def get_parser(self, prog_name):
        parser = super(UploadBlob, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<ID>",
            help="ID of the artifact to display",
        )
        parser.add_argument(
            '--type-name',
            default=None,
            metavar='<TYPE_NAME>',
            help='',
        )
        parser.add_argument(
            '--blob',
            default=None,
            metavar='<TYPE_NAME>',
            help='',
        )
        parser.add_argument(
            '--blob-property',
            metavar="<key=value>",
            action='append',
            default=[],
            help=''
        )

    def take_action(self, parsed_args):
        LOG.debug("take_action({0})".format(parsed_args))
        client = self.app.client_manager.artifact
        data = client.artifacts.upload_blob(parsed_args.id,
                                            parsed_args.blob_property,
                                            parsed_args.blob,
                                            type_name=parsed_args.type_name)
        return self.dict2columns(data)


class DownloadBlob(command.Lister):
    """Download blob"""

    def get_parser(self, prog_name):
        parser = super(DownloadBlob, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<ID>",
            help="ID of the artifact to display",
        )
        parser.add_argument(
            '--type-name',
            default=None,
            metavar='<TYPE_NAME>',
            help='',
        )
        parser.add_argument(
            '--blob',
            default=None,
            metavar='<TYPE_NAME>',
            help='',
        )
        parser.add_argument(
            '--blob-property',
            metavar="<key=value>",
            action='append',
            default=[],
            help=''
        )

    def take_action(self, parsed_args):
        LOG.debug("take_action({0})".format(parsed_args))
        client = self.app.client_manager.artifact
        data = client.artifacts.download_blob(parsed_args.id,
                                              parsed_args.blob_property,
                                              parsed_args.blob,
                                              type_name=parsed_args.type_name)
        return self.dict2columns(data)
