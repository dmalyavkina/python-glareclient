# Copyright 2016 OpenStack Foundation
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

import mock
from osc_lib.tests import utils


def test_list(*args, **kwargs):
    return [{'id': 'fc15c365-d4f9-4b8b-a090-d9e230f1f6ba',
             'name': 'art1',
             'version': '0.0.0',
             'owner': 'f649c77999e449e89627024f71b76603',
             'visibility': 'private',
             'status': 'active'},
            {'id': '48d35c1d-6739-459b-bbda-e4dcba8a684a',
             'name': 'art2',
             'version': '0.0.0',
             'owner': 'f649c77999e449e89627024f71b76603',
             'visibility': 'private',
             'status': 'active'}]


class TestArtifacts(utils.TestCommand):

    def setUp(self):
        super(TestArtifacts, self).setUp()
        self.app.client_manager.artifact = mock.MagicMock()
        self.app.client_manager.artifact.artifacts.list = test_list
