import json
import unittest
from unittest import mock

import get_actions


class TestJsonToActions(unittest.TestCase):
    """
    Tests retrieval of actions from JSON dictionary
    """

    def test_one_service_one_action(self):
        """
        Test single service with one action
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1"])

    def test_one_service_two_action(self):
        """
        Test single service with two actions
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1", "action2"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1", "sn1:action2"])

    def test_two_service_single_action(self):
        """
        Test two service with single actions
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}, ' + \
                        '"Service Name 2": {"StringPrefix": "sn2","Actions": ["action1"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1", "sn2:action1"])

    def test_two_service_multi_action(self):
        """
        Test two service with single actions
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1", "action2"]}, ' + \
                        '"Service Name 2": {"StringPrefix": "sn2","Actions": ["action1", "action2", "action3"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1", "sn1:action2", "sn2:action1", "sn2:action2", "sn2:action3"])


class TestGenerateActionList(unittest.TestCase):
    """
    Tests generating the action list
    """

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"serviceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action(self, mock_get):
        """
        Test generate actions
        """

        action_list = get_actions.generate_action_list()
        self.assertListEqual(action_list, ["sn1:action1"])

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"serviceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn2","Actions": ["action1"]}, ' +
                             '"Service Name 2": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_sort(self, mock_get):
        """
        Test sort actions
        """

        action_list = get_actions.generate_action_list(True)
        self.assertListEqual(action_list, ["sn1:action1", "sn2:action1"])

    @mock.patch('builtins.open', mock.mock_open())
    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"serviceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_write(self, mock_get):
        """
        Test save actions to file
        """

        get_actions.generate_action_list(True, True)
        open.assert_called_with('aws_action_list.txt', 'w')

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"noServiceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_bad_response_no_servicemap_key(self, mock_get):
        """
        Test lack of 'serviceMap' key
        """

        with self.assertRaises(SystemExit):
            get_actions.generate_action_list()

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig123={"noServiceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_bad_response_no_split(self, mock_get):
        """
        Test lack of 'app.PolicyEditorConfig=' when doing split
        """

        with self.assertRaises(SystemExit):
            get_actions.generate_action_list()

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig=["noServiceMap": ' +
                             '{"Service Name 1"')
    def test_gen_action_bad_response_bad_json(self, mock_get):
        """
        Test bas json response
        """

        with self.assertRaises(SystemExit):
            get_actions.generate_action_list()


if __name__ == '__main__':
    unittest.main()
