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
from osc_lib import utils
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class ListArtifacts(command.Lister):
    """Lists artifacts"""

    def get_parser(self, prog_name):
        parser = super(ListArtifacts, self).get_parser(prog_name)
        parser.add_argument(
            '--type-name',
            default=None,
            metavar='<TYPE_NAME>',
            help='',
        )
        parser.add_argument(
            '--limit',
            default=None,
            metavar='<LIMIT>',
            help='Maximum number of artifacts to get.',
        )
        parser.add_argument(
            '--page-size',
            default=None,
            metavar='<SIZE>',
            help='Number of artifacts to request in each paginated request.',
        )
        parser.add_argument(
            '--filters',
            default=None,
            metavar='<KEY=VALUE>',
            help='Filter artifacts by a user-defined artifact property.',
        )
        parser.add_argument(
            '--sort',
            default=None,
            metavar='<key>[:<direction>]',
            help="Comma-separated list of sort keys and directions in the "
                 "form of <key>[:<asc|desc>].",
        )
        return parser

    def take_action(self, parsed_args):
        LOG.debug("take_action({0})".format(parsed_args))
        client = self.app.client_manager.artifact
        data = client.artifacts.list(type_name=parsed_args.type_name,
                                     **parsed_args)

        columns = ('id', 'name')
        column_headers = [c.capitalize() for c in columns]
        return (
            column_headers,
            list(utils.get_item_properties(
                s,
                columns,
            ) for s in data)
        )


class ShowArtifact(command.ShowOne):
    """Display environment details"""

    def get_parser(self, prog_name):
        parser = super(ShowArtifact, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<ID>",
            help=("Name or ID of the environment to display"),
        )
        parser.add_argument(
            '--type-name',
            default=None,
            metavar='<TYPE_NAME>',
            help='',
        )
        return parser

    def take_action(self, parsed_args):
        LOG.debug("take_action({0})".format(parsed_args))
        client = self.app.client_manager.artifact
        data = client.artifacts.get(parsed_args.id,
                                    type_name=parsed_args.type_name,
                                    **parsed_args)
        return self.dict2columns(data)


class CreateArtifact(command.ShowOne):
    """Display environment details"""

    def get_parser(self, prog_name):
        parser = super(CreateArtifact, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<ID>",
            help=("Name or ID of the environment to display"),
        )
        parser.add_argument(
            '--type-name',
            default=None,
            metavar='<TYPE_NAME>',
            help='',
        )
        return parser

    def take_action(self, parsed_args):
        LOG.debug("take_action({0})".format(parsed_args))
        client = self.app.client_manager.artifact
        data = client.artifacts.get(parsed_args.id,
                                    type_name=parsed_args.type_name,
                                    **parsed_args)
        return self.dict2columns(data)
