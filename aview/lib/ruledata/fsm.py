"""
fsm.py: Finite State Machine
"""
from types import MethodType
from typing import Type

class State():

    def __init__(self, on_event=None, on_entry=None,
                 on_exit=None, name : str="") -> None:

        self.name = name

        if on_event:
            self.on_event = MethodType(on_event, self, State)
        if on_entry:
            self.on_entry = MethodType(on_entry, self, State)
        if on_exit:
            self.on_exit = MethodType(on_exit, self, State)


    def on_entry(self, e=None):
        # continue      --> self or None
        # transition(forward)
        #               --> state or (state, event)
        return self


    def on_event(self, e):
        # continue      --> self
        # transition    --> state or (state, event)
        # reopen        --> (self, event)
        # done          --> None
        raise RuntimeError("State '" + self.name + "' has no on_event handler.")


    def on_exit(self):
        return


class StateMachine(State):

    def __init__(self, on_event=None, on_entry=None,
                 on_exit=None, name : str="") -> None:
        super().__init__(on_event, on_entry, on_exit, name)

        self._state_list = []
        self._start : State = None
        self._state : State = None


    def add_state(self, state):
        if isinstance(state, State):
            self._state_list.append(state)
        else:
            raise TypeError(
                'state to add should be State or StateMachine(not "'
                + type(state) + '")')

        return self


    def on_entry(self, e=None):
        return self.start(e)

    def start(self, e=None):
        if self._start:
            self._state = self._start
        else:
            self._state = self._state_list[0]

        # continue      --> self or None
        # transition(forward)
        #               --> state or (state, event)
        r = self._state.on_entry(e)
        if r is self._state:
            r = self

        return r



    def on_event(self, e):
        return self.process_event(e)

    def process_event(self, e):

        if self._state is None:
            # Not yet started.
            # should raise.
            pass

        # continue      --> self
        # transition    --> state or (state, event)
        # reopen        --> (self, event)
        # done          --> None
        next = self._state.on_event(e)

        if next is None:
            self._state.on_exit()
            self._state = None
            next = None

        elif next is self._state:
            next = self

        else:
            if type(next) is tuple:
                _next = next[0]
                _e = next[1]
            else:
                _next = next
                _e = None

            self._state.on_exit()
            self._state = self._get_state(_next)

            if self._state is not None:
                self._state.on_entry(_e)
                next = self
            
            # if self._state is None(Not found), 
            # return the unfound state to upper layer.

        return next


    def on_exit(self):
        return self.stop()

    def stop(self):
        if self._state is not None:
            self._state.on_exit()
            self._state = None
        else:
            result = None


    def _get_state(self, next) -> State:
        state = None

        if isinstance(next, State):
            if next in self._state_list:
                state = next
        
        elif type(next) is str:
            for s in self._state_list:
                if s.name == next:
                    state = s
                    break

        else:
            # type error
            # should raise.
            pass

        return state
