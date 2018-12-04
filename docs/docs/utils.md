## Importing
```
>>> from logagg_utils import utils
>>> dir(utils)
['DUMMY', 'Dummy', 'Thread', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'ensure_dir', 'is_number', 'utils.ispartial', 'log_exception', 'makedirs', 'numbers', 'path', 'start_daemon_thread', 'traceback']
>>> 
```
## Module Contents
- **DUMMY**
</br>
Abstraction that creates a dummy object that does no-operations on method invocations but logs all interactions.
```
>>> utils.DUMMY.foo()
<deeputil.misc.Dummy object at 0x7f0619e79ac8>
>>> utils.DUMMY.bar
<deeputil.misc.Dummy object at 0x7f0619e79ac8>
```

- **ensure_dir**
</br>
Checks if a given directory is there or not and creates one if not.
```
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
```

- **is_number**
</br>
Determines the type is number or not.
```
>>> utils.is_number('45')
False
>>> utils.is_number(45)
True
>>> utils.is_number(45.0)
True
>>> utils.is_number(45/56)
True
```

- **ispartial**
</br>
If log line starts with a space it is recognized as a partial line
```
>>> utils.ispartial('<time> <event> <some_log_line>')
False
>>> utils.ispartial(' <space> <traceback:> <some_line>')
True
>>> utils.ispartial('         <tab> <traceback:> <some_line>')
True
>>> utils.ispartial('   <white_space> <traceback:> <some_line>')
True
>>> utils.ispartial('')
False
```

- **start_daemon_thread**
</br>
Starts a deamon thread for a given target function and arguments.
```
>>> def hello():
...     for i in range(5): print('hello world!')

>>> th = utils.start_daemon_thread(hello).join()
hello world!
hello world!
hello world!
hello world!
hello world!
```
