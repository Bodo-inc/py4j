from __future__ import unicode_literals, absolute_import


from py4j.java_gateway import JavaGateway, GatewayParameters
from py4j.tests.java_gateway_test import (
    start_example_app_process)
from contextlib import contextmanager
from nose.tools import eq_, assert_in, assert_not_in

@contextmanager
def example_app_process():
    p = start_example_app_process()
    try:
        yield p
    finally:
        p.join()

@contextmanager
def gateway(*args, **kwargs):
    g = JavaGateway(
        gateway_parameters=GatewayParameters(*args, auto_convert=True, **kwargs))
    lineSep = g.jvm.System.lineSeparator()
    try:
        yield g
        # Call a dummy method to make sure we haven't corrupted the streams
        eq_(lineSep, g.jvm.System.lineSeparator())
    finally:
        g.shutdown()

def test_help_object():
    with example_app_process():
        with gateway() as g:
            ex = g.getNewExample()
            doc = g.help(ex, display=False)
            assert_in('Help on class ExampleClass in package py4j.examples', doc)
            assert_in('method1', doc)
            assert_in('method2', doc)

def test_doc_object():
    with example_app_process():
        with gateway() as g:
            ex = g.getNewExample()
            doc = ex.__doc__
            assert_in('Help on class ExampleClass in package py4j.examples', doc)
            assert_in('method1', doc)
            assert_in('getField1', doc)

def test_not_callable():
    with example_app_process():
        with gateway() as g:
            ex = g.getNewExample()
            try:
                ex()
                raise AssertionError
            except TypeError, e:
                assert_in('object is not callable', str(e))
