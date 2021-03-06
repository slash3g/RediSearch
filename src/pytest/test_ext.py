from rmtest import BaseModuleTestCase
import redis
import unittest
from hotels import hotels
import random
import time
import subprocess
import os
import os.path

# this file is 'pytest'

SELF_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_MODULE = SELF_DIR + '/../tests/ext-example/example.so'
class ExtensionTestCase(BaseModuleTestCase):
    @property
    def module_args(self):
        return super(ExtensionTestCase, self).module_args + ['EXTLOAD', TEST_MODULE]

    def testExt(self):
        if not os.path.exists(TEST_MODULE):
            subprocess.call(['make', '-C', os.path.dirname(TEST_MODULE)])
        with self.redis() as r:

            r.flushdb()
            N = 100
            self.assertOk(r.execute_command(
                'ft.create', 'idx', 'schema', 'f', 'text'))
            for i in range(N):

                self.assertOk(r.execute_command('ft.add', 'idx', 'doc%d' % i, 1.0, 'fields',
                                                'f', 'hello world'))
            res = r.execute_command('ft.search', 'idx', 'hello world')
            self.assertEqual(N, res[0])
            res = r.execute_command('ft.search', 'idx', 'hello world', 'scorer', 'filterout_scorer')
            self.assertEqual(0, res[0])

if __name__ == '__main__':

    unittest.main()
