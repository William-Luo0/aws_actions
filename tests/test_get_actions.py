import json
import unittest
from unittest import mock

import get_actions


class TestJsonToActions(unittest.TestCase):
    """
    GIVEN a JSON object with services and actions
    """

    def test_one_service_one_action(self):
        """
        WHEN there is only one service with one action
        THEN a single action item should be returned prefixed with the service
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1"])

    def test_one_service_two_action(self):
        """
        WHEN there is one service with multiple (two?) actions
        THEN multiple (two?) action items should be returned with the service prefixed
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1", "action2"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1", "sn1:action2"])

    def test_two_service_single_action(self):
        """
        WHEN there are multiple (two?) services with one action each
        THEN multiple (two?) action items should be returned with the service prefixed
         and they should have the correct prefix for their respective actions
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}, ' + \
                        '"Service Name 2": {"StringPrefix": "sn2","Actions": ["action1"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1", "sn2:action1"])

    def test_two_service_multi_action(self):
        """
        WHEN there are multiple (two?) services with multiple actions each
        THEN multiple action items should be returned with the service prefixed
         and the number of items returned should equal the total number of actions of all services
        """
        test_json_str = '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1", "action2"]}, ' + \
                        '"Service Name 2": {"StringPrefix": "sn2","Actions": ["action1", "action2", "action3"]}}'
        test_json = json.loads(test_json_str)

        action = get_actions.json_to_actions(test_json)

        self.assertListEqual(action, ["sn1:action1", "sn1:action2", "sn2:action1", "sn2:action2", "sn2:action3"])


class TestGenerateActionList(unittest.TestCase):
    """
    GIVEN aws service actions are available from a publicly accessible URL (to be mocked)
    """

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"serviceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action(self, mock_get):
        """
        WHEN this function is called without inputs
        THEN it will return a list of actions
        """

        action_list = get_actions.generate_action_list()
        self.assertListEqual(action_list, ["sn1:action1"])

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"serviceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn2","Actions": ["action1"]}, ' +
                             '"Service Name 2": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_sort(self, mock_get):
        """
        WHEN this function is called with the sort option
        THEN it will return a sorted list of actions (services then actions)
        """

        action_list = get_actions.generate_action_list(True)
        self.assertListEqual(action_list, ["sn1:action1", "sn2:action1"])

    @mock.patch('builtins.open', mock.mock_open())
    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"serviceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_write(self, mock_get):
        """
        WHEN this function is called with the save_to_file option
        THEN save the list of actions to a file
        """

        get_actions.generate_action_list(write_to_file=True)
        # noinspection PyUnresolvedReferences
        open.assert_called_with('aws_action_list.txt', 'w')

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig={"noServiceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_bad_response_no_servicemap_key(self, mock_get):
        """
        WHEN the 'serviceMap' key is unexpectedly missing/bad
        THEN the error should be gracefully handled and the program should exit
        """

        with self.assertRaises(SystemExit):
            get_actions.generate_action_list()

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig123={"noServiceMap": ' +
                             '{"Service Name 1": {"StringPrefix": "sn1","Actions": ["action1"]}}}')
    def test_gen_action_bad_response_no_split(self, mock_get):
        """
        WHEN the string splitting string is unexpectedly missing/bad
        Test the error should be gracefully handled and the program should exit
        """

        with self.assertRaises(SystemExit):
            get_actions.generate_action_list()

    @mock.patch('get_actions.get_policy_js',
                return_value='app.PolicyEditorConfig=["noServiceMap": ' +
                             '{"Service Name 1"')
    def test_gen_action_bad_response_bad_json(self, mock_get):
        """
        WHEN the JSON returned is unexpectedly bad
        Test the error should be gracefully handled and the program should exit
        """

        with self.assertRaises(SystemExit):
            get_actions.generate_action_list()


class TestPullActionList(unittest.TestCase):
    """
    GIVEN a file with actions already exists
    """

    @mock.patch('builtins.open', mock.mock_open(read_data="sn2:action1\nsn1:action1"))
    def test_get_actions_basic(self):
        """
        WHEN the function is called with no inputs
        THEN a list of actions is returned
        """
        action_list = get_actions.pull_action_list()
        self.assertEqual(action_list, ['sn2:action1', 'sn1:action1'])

    @mock.patch('builtins.open', mock.mock_open(read_data="sn2:action1\nsn1:action1"))
    def test_get_actions_sorted(self):
        """
        WHEN the function is called with sort option
        THEN a sorted list of actions is returned
        """
        action_list = get_actions.pull_action_list(sort=True)
        self.assertEqual(action_list, ['sn1:action1', 'sn2:action1'])

    @mock.patch('builtins.open', mock.mock_open())
    def test_get_actions_custom_file(self):
        """
        WHEN the function is called with a custom file
        THEN the custom file is opened
        """
        open_file_name = 'blabla.txt'
        get_actions.pull_action_list(file=open_file_name)
        # noinspection PyUnresolvedReferences
        open.assert_called_with(open_file_name, 'r')


if __name__ == '__main__':
    unittest.main()
