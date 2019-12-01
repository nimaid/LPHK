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

log = None

class _Logger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(self.file_path, "w")
        self.stdout_logger = self._LoggerStdout(self.file)
        self.stderr_logger = self._LoggerStderr(self.file)
    def __del__(self):
        self.stdout_logger.__del__()
        self.stderr_logger.__del__()
        self.file.close()
    class _LoggerStdout:
        def __init__(self, file_in):
            self.file = file_in
            self.stdout = sys.stdout
            sys.stdout = self
        def __del__(self):
            sys.stdout = self.stdout
        def write(self, data):
            self.file.write(data)
            self.file.flush()
            self.stdout.write(data)
        def flush(self):
            self.file.flush()
    class _LoggerStderr:
        def __init__(self, file_in):
            self.file = file_in
            self.stderr = sys.stderr
            sys.stderr = self
        def __del__(self):
            sys.stderr = self.stderr
        def write(self, data):
            self.file.write(data)
            self.file.flush()
            self.stderr.write(data)
        def flush(self):
            self.file.flush()

def start(file_path):
    global log
    if log != None:
        raise Exception("A log is already running: " + log.file_path)
    else:
        log = _Logger(file_path)

def stop():
    global log
    if log == None:
        raise Exception("No log is currently running.")
    else:
        log.__del__()
        log = None