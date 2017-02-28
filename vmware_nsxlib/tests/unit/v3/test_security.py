# Copyright (c) 2015 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from vmware_nsxlib.tests.unit.v3 import nsxlib_testcase


class TestNsxLibFirewallSection(nsxlib_testcase.NsxLibTestCase):
    """Tests for vmware_nsxlib.v3.security.NsxLibFirewallSection"""

    def test_get_logicalport_reference(self):
        mock_port = '3ed55c9f-f879-4048-bdd3-eded92465252'
        result = self.nsxlib.firewall_section.get_logicalport_reference(
            mock_port)
        expected = {
            'target_id': '3ed55c9f-f879-4048-bdd3-eded92465252',
            'target_type': 'LogicalPort'
        }
        self.assertEqual(expected, result)

    def test_get_rule_address(self):
        result = self.nsxlib.firewall_section.get_rule_address(
            'target-id', 'display-name')
        expected = {
            'target_display_name': 'display-name',
            'target_id': 'target-id',
            'is_valid': True,
            'target_type': 'IPv4Address'
        }
        self.assertEqual(expected, result)

    def test_get_l4portset_nsservice(self):
        result = self.nsxlib.firewall_section.get_l4portset_nsservice()
        expected = {
            'service': {
                'resource_type': 'L4PortSetNSService',
                'source_ports': [],
                'destination_ports': [],
                'l4_protocol': 'TCP'
            }
        }
        self.assertEqual(expected, result)

    def test_create_with_rules(self):
        expected_body = {
            'display_name': 'display-name',
            'description': 'section-description',
            'stateful': True,
            'section_type': "LAYER3",
            'applied_tos': [],
            'rules': [{
                'display_name': 'rule-name',
                'direction': 'IN_OUT',
                'ip_protocol': "IPV4_IPV6",
                'action': "ALLOW",
                'logged': False,
                'disabled': False,
                'sources': [],
                'destinations': [],
                'services': []
            }],
            'tags': []
        }
        with mock.patch.object(self.nsxlib.client, 'create') as create:
            rule = self.nsxlib.firewall_section.get_rule_dict('rule-name')
            self.nsxlib.firewall_section.create_with_rules(
                'display-name', 'section-description', rules=[rule])
            resource = 'firewall/sections?operation=insert_bottom' \
                '&action=create_with_rules'
            create.assert_called_with(resource, expected_body)
