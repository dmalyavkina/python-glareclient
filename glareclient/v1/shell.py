# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from glareclient._i18n import _
from glareclient.common import utils


def do_artifact_list(gc, args):
    """List artifacts you can access."""

    kwargs = {}
    columns = ['ID', 'Name']

    artifacts = gc.artifacts.list(**kwargs)
    utils.print_list(artifacts, columns)


@utils.arg('id', metavar='<A_ID>', help=_('ID of image to describe.'))
def do_artifact_show(gc, args):
    """Describe a specific image."""
    af = gc.artifacts.get(args.id)
    utils.print_image(af, args.human_readable, int(args.max_column_width))

