import fnmatch
import json
import sys


def expand_permissions(aws_policy, all_actions, discard_unknown=False):
    policy_json = []
    try:
        policy_json = json.loads(aws_policy)

    except (ValueError) as e:
        print("ERR: Given 'aws_policy' is not valid JSON", file=sys.stderr)
        exit(e)

    # noinspection PyTypeChecker
    for statement in policy_json["Statement"]:
        replace_actions = []
        for action in statement["Action"]:
            matched_actions = fnmatch.filter(all_actions, action)
            if len(matched_actions) == 0 and not discard_unknown:
                replace_actions.append(action)
                print("WARN: Could not match '" + action + "'", file=sys.stderr)
            else:
                replace_actions.extend(matched_actions)
        statement['Action'] = replace_actions
    return json.dumps(policy_json)


def main():
    print("ERR: This module can't be directly run. Please import as a module.", file=sys.stderr)
    exit(1)


if __name__ == '__main__':
    main()
