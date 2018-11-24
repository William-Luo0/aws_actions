# AWS Actions
Obtain a list of all AWS actions. This utilises the same JS file that the AWS policy generator uses.

Can also be used to expand wildcard actions in AWS policies to their fully qualified action.

# Usage
## Standalone
The script can be run in standalone mode and will output a list of actions to `aws_action_list.txt` Simply run:

```python
python3 get_actions.py
```

## Imported module
The script can also be imported into other python scripts

```python
import get_actions
action_list = get_actions.generate_action_list(sort=False, write_to_file=False)
```

If you do not wish to connect to the web, you can also load a local file. Defaults to `aws_action_list.txt`

```python
import get_actions
action_list = get_actions.pull_action_list(sort=False, file='local_file.txt')
```

## Expanding wildcard actions
Wildcard expansion turns actions like `application-autoscaling:Describe*` into:
```
application-autoscaling:DescribeScalableTargets
application-autoscaling:DescribeScalingActivities
application-autoscaling:DescribeScalingPolicies
application-autoscaling:DescribeScheduledActions
```

Import the module and provide your policy, the full list of AWS actions and optionally if unknown services should be discarded.
```python
import expand_permissions
full_actions = expand_permissions.expand_permissions(aws_policy, all_actions, discard_unknown=False)
```
