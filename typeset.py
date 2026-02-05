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

    def __iter__(self):
        yield from self.elements
