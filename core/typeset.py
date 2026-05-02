class NoElementPresent(Exception):
    pass


class TypeSet:
    """
    A set where each element must have a unique type
    """
    def __init__(self, elements = None):
        if elements is None:
            self.elements = set()
        else:
            self.elements = set(elements) # todo: this does not strictly enforce the constraint

    def add(self, element):
        for e in self.elements:
            if type(element) == type(e):
                return
        self.elements.add(element)

    def discard(self, element_type):
        self.elements = set(filter(lambda x: type(x) != element_type, self.elements))

    def retrieve_instance(self, element_type) -> object:
        """
        Returns the element implementing the given class.
        :param element_type:
        :return:
        """
        match = list(filter(lambda x: type(x) == element_type, self.elements))
        if len(match) != 1:
            raise NoElementPresent()
        return match[0]

    def __iter__(self):
        yield from self.elements
