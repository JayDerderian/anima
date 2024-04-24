"""
Base class for each container
"""


class Container(object):
    """
    Base class for holding metadata about an
    individual melody, chord, or note object
    """

    def __init__(self):

        self.info = "None"
        self.pcs = []  # pitch classes for this container
        self.source_data = []  # source data for this container
        self.source_notes = []  # source scale for this container

    def __str__(self):
        raise NotImplementedError("This is an abstract base class!")

    def __repr__(self):
        raise NotImplementedError("This is an abstract base class!")

    # context manager support
    def __enter__(self):
        raise NotImplementedError("This is an abstract base class!")

    def __exit__(self, exc_type, exc_value):
        raise NotImplementedError("This is an abstract base class!")
