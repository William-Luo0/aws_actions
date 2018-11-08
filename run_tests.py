import os
import shutil
import unittest

import xmlrunner

# Constants
_test_report_dir = 'test-reports'

# Remove previous tests
try:
    shutil.rmtree(_test_report_dir)
except FileNotFoundError:
    pass

# Run tests
suite = unittest.TestLoader().discover('tests')
xmlrunner.XMLTestRunner(output=os.environ.get('CIRCLE_TEST_REPORTS', _test_report_dir)).run(suite)
