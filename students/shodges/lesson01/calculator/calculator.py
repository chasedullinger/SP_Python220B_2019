class Calculator(object):
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        result = operator.calc(self.stack[0], self.stack[1])

        self.stack = [result]
        return result

    def add(self):
        return self._do_calc(self.adder)

    def subtract(self):
        return self._do_calc(self.subtracter)

    def multiply(self):
        return self._do_calc(self.multipler)

    def divide(self):
        return self._do_calc(self.divider)
