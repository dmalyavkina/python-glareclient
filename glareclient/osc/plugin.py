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

from osc_lib import utils
from oslo_log import log as logging

from glareclient._i18n import _

LOG = logging.getLogger(__name__)

DEFAULT_APPLICATION_CATALOG_API_VERSION = "1"
API_VERSION_OPTION = "os_artifact_api_version"
API_NAME = "artifact"
API_VERSIONS = {
    '1': 'glareclient.v1.client.Client',
}


def make_client(instance):
    """Returns an application-catalog service client"""
    glare_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug("Instantiating glare client: {0}".format(
              glare_client))

    client = glare_client(
        instance.get_configuration().get('glare_url'),
        region_name=instance._region_name,
        session=instance.session,
        service_type='artifact',
    )
    return client


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-artifact-api-version',
        metavar='<--os-artifact-api-version>',
        default=utils.env(
            'OS_ARTIFACT_API_VERSION',
            default=DEFAULT_APPLICATION_CATALOG_API_VERSION),
        help=_("Artifact API version, default={0}"
               "(Env:OS_ARTIFACT_API_VERSION)").format(
                   DEFAULT_APPLICATION_CATALOG_API_VERSION))
    parser.add_argument('--glare-url',
                        default=utils.env('GLARE_URL'),
                        help=_('Defaults to env[GLARE_URL].'))
    return parser
