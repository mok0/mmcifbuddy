from abc import ABC, abstractmethod
from enum import Enum


class StateName(Enum):
    sBEGIN = 1
    sLOOP = 2
 

# Abstract base class State
class State(ABC):
    @abstractmethod
    def set_state(self, state: StateName):
        ...
 
 
class BeginState(State):
    def __init__(self, context):
        self.context = context

    def __str__(self):
        return __class__.__name__

    def set_state(self, state: StateName) -> None:
        self.context.set_state(StateName.sLOOP, self.context.loop_state)
   

class LoopState(State):
    def __init__(self, context):
        self.context = context

    def __str__(self):
        return __class__.__name__

    def set_state(self, state: StateName) -> None:
        self.context.set_state(StateName.sBEGIN, self.context.begin_state)
 
