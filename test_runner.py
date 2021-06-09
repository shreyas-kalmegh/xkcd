# tests/runner.py
import unittest

# import your test modules
import src.tests.test_api_helpers as tah
import src.tests.test_db_helpers as tbh
import src.tests.test_task_one_helpers as ttoh
import src.tests.test_db as tdb

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(tah))
suite.addTests(loader.loadTestsFromModule(tbh))
suite.addTests(loader.loadTestsFromModule(ttoh))
suite.addTests(loader.loadTestsFromModule(tdb))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)