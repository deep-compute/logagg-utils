#!/usr/bin/env python

import doctest
import unittest

from logagg_utils import utils

def suite_maker():
    suite= unittest.TestSuite()
    suite.addTests(doctest.DocTestSuite(utils))
    return suite

