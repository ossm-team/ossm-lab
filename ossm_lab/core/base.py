class Protocol:
    """ Analysis protocol that can be applied to a model. """

    def __call__(self, model):
        """ Apply the protocol to a model and return a result. """
        raise NotImplementedError


class Result:
    """ Result of applying a protocol to a model. """

    pass

class Visualization:
    """ Visualization of a model or result. """

    def __call__(self, result):
        """ Visualize the result. """
        raise NotImplementedError