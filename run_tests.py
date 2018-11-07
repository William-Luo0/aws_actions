import os
import unittest

import xmlrunner

suite = unittest.TestLoader().discover('tests')
xmlrunner.XMLTestRunner(output=os.environ.get('CIRCLE_TEST_REPORTS', 'test-reports')).run(suite)
