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


class Controller(object):
    def __init__(self, http_client):
        self.http_client = http_client

    def list(self, af_type, **kwargs):
        url = '/artifacts/%s' % af_type
        resp, body = self.http_client.get(url)
        return body

    def get(self, af_type, af_id):
        url = '/artifacts/%(af_type)s/%(af_id)s' % {'af_type': af_type,
                                                    'af_id': af_id}
        resp, body = self.http_client.get(url)
        return body
