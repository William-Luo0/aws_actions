import unittest

import expand_permissions


class TestExpandPermissions(unittest.TestCase):
    """
    GIVEN an aws managed policy and a full list of possible actions
    """

    def test_unknown_service_expansion(self):
        """
        WHEN the given policy has a service/action that is not known
        THEN the unknown service/action should be returned unchanged
        """
        test_policy = '{"Version": "2012-10-17", ' + \
                      '"Statement": [{"Action": ["unknownService:*"], ' + \
                      '"Effect": "Allow", ' + \
                      '"Resource": "*"}]}'
        test_actions = ['service:action1', 'service:action2', 'service:action3']

        full_policy = expand_permissions.expand_permissions(test_policy, test_actions)

        expected_policy = '{"Version": "2012-10-17", ' + \
                          '"Statement": [{"Action": ["unknownService:*"], ' + \
                          '"Effect": "Allow", ' + \
                          '"Resource": "*"}]}'
        self.assertEqual(full_policy, expected_policy)

    def test_discard_unknown_service(self):
        """
        WHEN the given policy has a service/action that is not known
        THEN the unknown service/action should be discarded
        """
        test_policy = '{"Version": "2012-10-17", ' + \
                      '"Statement": [{"Action": ["unknownService:*"], ' + \
                      '"Effect": "Allow", ' + \
                      '"Resource": "*"}]}'
        test_actions = ['service:action1', 'service:action2', 'service:action3']

        full_policy = expand_permissions.expand_permissions(test_policy, test_actions, True)

        expected_policy = '{"Version": "2012-10-17", ' + \
                          '"Statement": [{"Action": [], ' + \
                          '"Effect": "Allow", ' + \
                          '"Resource": "*"}]}'
        self.assertEqual(full_policy, expected_policy)

    def test_full_service_expansion(self):
        """
        WHEN the given policy has a known service with * permissions
        THEN all possible actions for the service should be returned
        """
        test_policy = '{"Version": "2012-10-17", ' + \
                      '"Statement": [{"Action": ["service:*"], ' + \
                      '"Effect": "Allow", ' + \
                      '"Resource": "*"}]}'
        test_actions = ['service:action1', 'service:action2', 'service:action3']

        full_policy = expand_permissions.expand_permissions(test_policy, test_actions)

        expected_policy = '{"Version": "2012-10-17", ' + \
                          '"Statement": [{"Action": ["service:action1", "service:action2", "service:action3"], ' + \
                          '"Effect": "Allow", ' + \
                          '"Resource": "*"}]}'
        self.assertEqual(full_policy, expected_policy)

    def test_partial_service_expansion(self):
        """
        WHEN the given policy has a service with partial * actions (e.g. Get*)
        THEN all matching actions for the service should be returned
        """
        test_policy = '{"Version": "2012-10-17", ' + \
                      '"Statement": [{"Action": ["service:Get*"], ' + \
                      '"Effect": "Allow", ' + \
                      '"Resource": "*"}]}'
        test_actions = ['service:GetAction1', 'service:GetAction2', 'service:PutAction1', 'service:PutAction2']

        full_policy = expand_permissions.expand_permissions(test_policy, test_actions)

        expected_policy = '{"Version": "2012-10-17", ' + \
                          '"Statement": [{"Action": ["service:GetAction1", "service:GetAction2"], ' + \
                          '"Effect": "Allow", ' + \
                          '"Resource": "*"}]}'
        self.assertEqual(full_policy, expected_policy)


if __name__ == '__main__':
    unittest.main()
