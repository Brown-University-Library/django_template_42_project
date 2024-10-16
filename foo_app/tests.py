import json, logging

from django.conf import settings as project_settings
# from django.test import TestCase                  # TestCase requires db
from django.test import SimpleTestCase as TestCase  # SimpleTestCase does not require db
from django.test.utils import override_settings


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


import doctest, unittest            # python built-in modules
from typing import Optional         # python built-in module
from foo_app.lib import bar, baz    # local modules

def load_tests( 
        loader: unittest.TestLoader, 
        tests: unittest.TestSuite,
        pattern: Optional[str]
        ):
    """
    load_tests() info...
        Django's test runner is built on top of Python's unittest framework. 
        When running `python ./manage.py test`, Django uses unittest to discover and run tests.
        The load_tests() function is a special hook used by Python's unittest framework. 
        When the test runner is discovering tests, it looks for the load_tests() function in your test modules. 
        The `loader` and `pattern` arguments, not used here, offer options for customizing the test loading process.
        The `tests` argument is a TestSuite object containing the tests unittest has found.
    """
    tests.addTests( doctest.DocTestSuite(bar) )
    tests.addTests( doctest.DocTestSuite(baz) )
    return tests







class ErrorCheckTest( TestCase ):
    """ Checks urls. """

    @override_settings(DEBUG=True)  # for tests, DEBUG autosets to False
    def test_dev_errorcheck(self):
        """ Checks that dev error_check url triggers error.. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        try:
            log.debug( 'about to initiate client.get()' )
            response = self.client.get( '/error_check/' )
        except Exception as e:
            log.debug( f'e, ``{repr(e)}``' )
            self.assertEqual( "Exception('Raising intentional exception to check email-admins-on-error functionality.')", repr(e) )

    def test_prod_errorcheck(self):
        """ Checks that production error_check url returns 404. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        response = self.client.get( '/error_check/' )
        self.assertEqual( 404, response.status_code )
