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

from glareclient.common import utils
from glareclient import exc
from oslo_utils import encodeutils
import six
from six.moves.urllib import parse


class Controller(object):
    def __init__(self, http_client, type_name=None):
        self.http_client = http_client
        self.type_name = type_name
        self.default_page_size = 20
        self.sort_dir_values = ('asc', 'desc')

    def _check_type_name(self, type_name):
        """Check that type name and type versions were specified"""
        type_name = type_name or self.type_name
        if type_name is None:
            msg = "Type name must be specified"
            raise exc.HTTPBadRequest(msg)
        return type_name

    def _validate_sort_param(self, sort):
        """Validates sorting argument for invalid keys and directions values.

        :param sort: comma-separated list of sort keys with optional <:dir>
        after each key
        """
        for sort_param in sort.strip().split(','):
            key, _sep, dir = sort_param.partition(':')
            if dir and dir not in self.sort_dir_values:
                msg = ('Invalid sort direction: %(sort_dir)s.'
                       ' It must be one of the following: %(available)s.'
                       ) % {'sort_dir': dir,
                            'available': ', '.join(self.sort_dir_values)}
                raise exc.HTTPBadRequest(msg)
        return sort

    def create(self, name, version='0.0.0', type_name=None, **kwargs):
        """Create an artifact of given type and version.

        :param name: name of creating artifact.
        :param version: semver string describing an artifact version
        """
        type_name = self._check_type_name(type_name)
        kwargs.update({'name': name, 'version': version})
        url = '/artifacts/%s' % type_name
        resp, body = self.http_client.post(url, data=kwargs)
        return body

    def update(self, artifact_id, type_name=None, remove_props=None,
               **kwargs):
        """Update attributes of an artifact.

        :param artifact_id: ID of the artifact to modify.
        :param remove_props: List of property names to remove
        :param \*\*kwargs: Artifact attribute names and their new values.
        """
        type_name = self._check_type_name(type_name)
        url = '/artifacts/%s/%s' % (type_name, artifact_id)
        hdrs = {'Content-Type': 'application/json-patch+json'}
        changes = []
        if remove_props:
            for prop_name in remove_props:
                if prop_name not in kwargs:
                    changes.append({'op': 'remove',
                                    'path': '/%s' % prop_name})
        for prop_name in kwargs:
            changes.append({'op': 'add', 'path': '/%s' % prop_name,
                            'value': kwargs[prop_name]})
        resp, body = self.http_client.patch(url, headers=hdrs, data=changes)
        return body

    def get(self, artifact_id, type_name=None):
        """Get information about an artifact.

        :param artifact_id: ID of the artifact to get.

        """
        type_name = self._check_type_name(type_name)
        url = '/artifacts/%s/%s' % (type_name, artifact_id)
        resp, body = self.http_client.get(url)
        return body

    def list(self, type_name=None, **kwargs):
        """Retrieve a listing of artifacts objects.

        :param page_size: Number of artifacts to request in each
                          paginated request.
        :returns: generator over list of artifacts.
        """
        type_name = self._check_type_name(type_name)

        limit = kwargs.get('limit')
        page_size = kwargs.get('page_size') or self.default_page_size

        def paginate(url, page_size, limit=None):
            next_url = url

            while True:
                if limit and page_size > limit:
                    next_url = next_url.replace("limit=%s" % page_size,
                                                "limit=%s" % limit)

                resp, body = self.http_client.get(next_url)
                for artifact in body[type_name]:
                    yield artifact

                    if limit:
                        limit -= 1
                        if limit <= 0:
                            raise StopIteration

                try:
                    next_url = body['next']
                except KeyError:
                    return

        filters = kwargs.get('filters', [])
        filters.append(('limit', page_size))

        url_params = []
        for param, items in filters:
            values = [items] if not isinstance(items, list) else items
            for value in values:
                if isinstance(value, six.string_types):
                    value = encodeutils.safe_encode(value)
                url_params.append({param: value})

        url = '/artifacts/%s?' % type_name

        for param in url_params:
            url = '%s&%s' % (url, parse.urlencode(param))

        if 'sort' in kwargs:
            url = '%s&sort=%s' % (url, self._validate_sort_param(
                kwargs['sort']))

        for artifact in paginate(url, page_size, limit):
            yield artifact

    def active(self, artifact_id, type_name=None):
        """Set artifact status to 'active'.

        :param artifact_id: ID of the artifact to get.
        """
        return self.update(artifact_id, type_name,
                           status='active')

    def deactivate(self, artifact_id, type_name=None):
        """Set artifact status to 'deactivated'.

        :param artifact_id: ID of the artifact to get.
        """
        return self.update(artifact_id, type_name,
                           status='deactivated')

    def reactivate(self, artifact_id, type_name=None):
        """Set artifact status to 'active'.

        :param artifact_id: ID of the artifact to get.
        """
        return self.update(artifact_id, type_name,
                           status='active')

    def publish(self, artifact_id, type_name=None):
        """Set artifact visibility to 'public'.

        :param artifact_id: ID of the artifact to get.
        """
        return self.update(artifact_id, type_name,
                           visibility='public')

    def delete(self, artifact_id, type_name=None):
        """Delete an artifact and all its data.

        :param artifact_id: ID of the artifact to delete.
        """
        type_name = self._check_type_name(type_name)
        url = '/artifacts/%s/%s' % (type_name, artifact_id)
        self.http_client.delete(url)

    def upload_blob(self, artifact_id, blob_property, data, type_name=None):
        """Upload blob data.

        :param artifact_id: ID of the artifact to download a blob
        :param blob_property: blob property name
        """
        type_name = self._check_type_name(type_name)
        hdrs = {'Content-Type': 'application/octet-stream'}
        url = '/artifacts/%s/%s/%s' % (type_name, artifact_id, blob_property)
        self.http_client.put(url, headers=hdrs, data=data)

    def download_blob(self, artifact_id, blob_property, type_name=None,
                      do_checksum=True):
        """Get blob data.

        :param artifact_id: ID of the artifact to download a blob
        :param blob_property: blob property name
        :param do_checksum: Enable/disable checksum validation.
        """
        type_name = self._check_type_name(type_name)
        url = '/artifacts/%s/%s/%s' % (type_name, artifact_id, blob_property)
        resp, body = self.http_client.get(url)
        checksum = resp.headers.get('content-md5', None)
        content_length = int(resp.headers.get('content-length', 0))
        if checksum is not None and do_checksum:
            body = utils.integrity_iter(body, checksum)
        return utils.IterableWithLength(body, content_length)
