'''
This class is used for control flow, which is generally not optimal, but I
think it can be justified here. I'll ask on SO or Reddit later!
'''

from typing import Any

class Break(Exception):
    '''
    Control flow exception to unwind callstack on return statement.
    '''
    def __init__(self):
        super().__init__()
