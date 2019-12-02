# Logger module by Ella J. (nimaid)
# 
# This module provides basic logging of STDOUT and STDERR to a text file
# Usage:
# 
# import logger
# logger.start("/path/to/my/log.txt")
# ...
# logger.stop()

import sys

_log = None

class _Logger:
    def __init__(self, file_path):
        self.path = file_path
        self._file = open(self.path, "w")
        self._stdout_logger = self._LoggerStdout(self._file)
        self._stderr_logger = self._LoggerStderr(self._file)
    
    def __del__(self):
        self._stdout_logger.__del__()
        self._stderr_logger.__del__()
        self._file.close()
    
    class _LoggerStdout:
        def __init__(self, file_in):
            self._file = file_in
            self._stdout = sys.stdout
            sys.stdout = self
        def __del__(self):
            sys.stdout = self._stdout
        def write(self, data):
            self._stdout.write(data)
            self._file.write(data)
            self._file.flush()
        def flush(self):
            self._file.flush()
    
    class _LoggerStderr:
        def __init__(self, file_in):
            self._file = file_in
            self._stderr = sys.stderr
            sys.stderr = self
        def __del__(self):
            sys.stderr = self._stderr
        def write(self, data):
            self._stderr.write(data)
            self._file.write(data)
            self._file.flush()
        def flush(self):
            self._file.flush()

def start(file_path):
    global _log
    if _log != None:
        raise FileExistsError("A log is already running: " + _log.path)
    else:
        _log = _Logger(file_path)

def stop():
    global _log
    if _log == None:
        raise FileNotFoundError("No log is currently running.")
    else:
        _log.__del__()
        _log = None