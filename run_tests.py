import unittest

suite = unittest.TestLoader().discover('tests')
tests = unittest.TextTestRunner(verbosity=2).run(suite)