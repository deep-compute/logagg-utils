import traceback
from threading import Thread
from os import path, makedirs
import numbers

from deeputil import Dummy

DUMMY = Dummy()


def log_exception(self, __fn__):
    '''
    Logging traceback in keeprunning methods
    '''
    self.log.exception('error_during_run_Continuing', fn=__fn__.__name__,
                tb=repr(traceback.format_exc()))


def start_daemon_thread(target, args=()):
    '''
    Starts a deamon thread for a given target function and arguments

    >>> def hello():
    ...     for i in range(5): print('hello world!')
    >>> th = start_daemon_thread(hello).join()
    hello world!
    hello world!
    hello world!
    hello world!
    hello world!
    '''
    th = Thread(target=target, args=args)
    th.daemon = True
    th.start()
    return th


def is_number(x):
    '''
    Determines the type is number or not

    >>> is_number('45')
    False
    >>> is_number(45)
    True
    >>> is_number(45.0)
    True
    >>> is_number(45/56)
    True
    '''
    return isinstance(x, numbers.Number)


def ispartial(x):
    '''
    If log line starts with a space it is recognized as a partial line

    >>> ispartial('<time> <event> <some_log_line>')
    False
    >>> ispartial(' <space> <traceback:> <some_line>')
    True
    >>> ispartial('         <tab> <traceback:> <some_line>')
    True
    >>> ispartial('   <white_space> <traceback:> <some_line>')
    True
    >>> ispartial('')
    False
    '''
    spaces = (' ', '\t', '\n')
    try:
        if x[0] in spaces:
            return True
    except IndexError:
        return False
    else:
        return False

def ensure_dir(dir_path):
    '''
    >>> import os
    >>> dir = '/tmp/orange/apple/banana'
    >>> os.path.isdir(dir)
    False
    >>> os.path.isdir(dir)
    False
    >>> ensure_dir(dir)
    '/tmp/orange/apple/banana'
    >>> os.path.isdir('/tmp/orange')
    True
    >>> os.path.isdir('/tmp/orange/apple')
    True
    >>> os.path.isdir('/tmp/orange/apple/banana')
    True
    '''
    if not path.exists(dir_path):
        makedirs(dir_path)
    return dir_path
