import json
import sys
from urllib.request import urlopen

# Constants
_AWS_POLICY_URL = 'https://awspolicygen.s3.amazonaws.com/js/policies.js'
_SPLIT_STR = 'app.PolicyEditorConfig='


def get_policy_js():
    response = urlopen(_AWS_POLICY_URL)
    return response.read().decode()


def json_to_actions(service_map):
    service_actions = []
    for service in service_map:
        for action in service_map[service]["Actions"]:
            service_actions.append(service_map[service]["StringPrefix"] + ":" + action)
    return service_actions


def generate_action_list(sort=False, write_to_file=False):
    policy_js = get_policy_js()
    action_list = []

    try:
        full_json = json.loads(policy_js.split(_SPLIT_STR)[1])
        action_list = json_to_actions(full_json["serviceMap"])

    except (ValueError, KeyError, IndexError) as e:
        print("Unexpected response, check " + _AWS_POLICY_URL, file=sys.stderr)
        exit(e)

    if sort:
        action_list.sort()

    # Write list to file
    if write_to_file:
        with open('aws_action_list.txt', 'w') as f:
            for action in action_list:
                f.write(action + "\n")

    return action_list


def main():
    generate_action_list(True, True)


if __name__ == '__main__':
    main()
