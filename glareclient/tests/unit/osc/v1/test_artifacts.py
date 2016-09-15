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


import collections
import json
import tempfile

import mock

from glareclient.osc.v1 import artifacts as osc_art
from glareclient.tests.unit.osc.v1 import fakes
from glareclient.v1 import artifacts as api_art

RESPONSE_DATA = [('fc15c365-d4f9-4b8b-a090-d9e230f1f6ba',
                  'art1',
                  '0.0.0',
                  'f649c77999e449e89627024f71b76603',
                  'private',
                  'active'),
                 ('48d35c1d-6739-459b-bbda-e4dcba8a684a',
                  'art2',
                  '0.0.0',
                  'f649c77999e449e89627024f71b76603',
                  'private',
                  'active')]

COLUMNS = ['Id', 'Name', 'Version', 'Owner', 'Visibility', 'Status']


class TestArtifacts(fakes.TestArtifacts):
    def setUp(self):
        super(TestArtifacts, self).setUp()
        self.artifact_mock = \
            self.app.client_manager.artifact.artifacts
        self.http = mock.MagicMock()


class TestListArtifacts(TestArtifacts):

    def setUp(self):
        super(TestListArtifacts, self).setUp()
        self.artifact_mock.call.return_value = \
            api_art.Controller(self.http, type_name='sample_artifact')

        # Command to test
        self.cmd = osc_art.ListArtifacts(self.app, None)

    def test_artifact_list(self):
        arglist = ['sample_artifact']
        verifylist = [('type_name', 'sample_artifact')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        self.assertEqual(COLUMNS, columns)
        self.assertEqual(RESPONSE_DATA, data)

    def test_artifact_list_with_params(self):
        arglist = ['sample_artifact', '--sort', 'name:asc']
        verifylist = [('type_name', 'sample_artifact'),
                      ('sort', 'name:asc')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        columns, data = self.cmd.take_action(parsed_args)

        # Check that columns are correct
        self.assertEqual(COLUMNS, columns)
        self.assertEqual(RESPONSE_DATA, data)

