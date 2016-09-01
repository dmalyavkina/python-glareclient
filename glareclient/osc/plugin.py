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

DEFAULT_API_VERSION = "1"
API_VERSION_OPTION = "os_artifact_api_version"
API_NAME = "artifact"
API_VERSIONS = {
    '1': 'glareclient.v1.client.Client',
}


def make_client(instance):
    """Returns an artifact service client"""
    artifact_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('Instantiating artifact client: %s', artifact_client)

    endpoint = instance.get_endpoint_for_service_type(
        API_NAME,
        region_name=instance.region_name,
        interface=instance.interface,
    )

    client = artifact_client(
        endpoint,
        token=instance.auth.get_token(instance.session),
        cacert=instance.cacert,
        insecure=not instance.verify,
    )

    return client


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-artifact-api-version',
        metavar='<artifact-api-version>',
        default=utils.env('OS_ARTIFACT_API_VERSION'),
        help=_('Artifact API version, default=%s '
               '(Env: OS_ARTIFACT_API_VERSION)') % DEFAULT_API_VERSION,
    )
    return parser
