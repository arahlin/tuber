#!/usr/bin/env python3


class DeviceDriver:
    """
    This is a simple device driver class.  A more complicated driver might be
    written in C or C++ and bound to python using pybind11 or similar.
    """

    # Mark this class as an object that the tuber server should inspect for
    # methods and attributes
    __tuber_object__ = True

    # Static property: cached on the client once at resolve time.
    MODEL = "XR-7000"

    # Dynamic @property: the descriptor signals to tuber that this attribute
    # should be fetched from or pushed to the server on every client access.
    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, value):
        self._button = bool(value)

    # Opt-in dynamic property: listed in __tuber_dynamic__ so tuber treats it
    # as a live server-side value rather than caching it on the client.
    __tuber_dynamic__ = {"knob"}

    def __init__(self):
        self._button = False
        self.knob = 1

    def push_button(self):
        self.button = not self.button
        return self.button

    def get_all(self):
        return {"button": self.button, "knob": self.knob}


if __name__ == "__main__":
    from tuber.server import main

    # create device registry, with the driver initialized with sensible defaults.
    registry = {"driver": DeviceDriver()}

    # run the server
    main(registry)
