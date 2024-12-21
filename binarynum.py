import operator

# twos_complement = lambda num, bits: (bin(num)[2:].zfill(bits) if num >= 0 else bin((1 << bits) + num)[2:])
#
# def calculate_jump_address(jump_label, current_label):
#     return twos_complement((jump_label*2) - (current_label*2 + 2) >> 1, 12)

twos_complement = lambda num, bits: (bin(num)[2:].zfill(bits) if num >= 0 else bin((1 << bits) + num)[2:])

class BinaryNum():

    def __init__(self, base10_num, size):
        self.binary = twos_complement(base10_num, size)
        self.decimal = base10_num

    def __performOp(self,num,op):
        if isinstance(num, int):
            result = op(self.decimal,num)
        elif isinstance(num, BinaryNum):
            result = op(self.decimal,num.decimal)
        else:
            raise TypeError(f"class BinaryNum doesn't support operations with {type(num)}")
        
        return BinaryNum(result, len(self.binary))

    locals().update({
        '__add__' : lambda self, num: self.__performOp(num, operator.__add__),
        '__sub__' : lambda self, num: self.__performOp(num, operator.__sub__),
        '__mul__' : lambda self, num: self.__performOp(num, operator.__mul__),
        '__and__' : lambda self, num: __performOp(num, operator.__and__),
        '__or__' : lambda self, num: __performOp(num, operator.__or__),
        '__xor__' : lambda self, num: __performOp(num, operator.__xor__),
        '__rshift__' : lambda self, num: __performOp(num, operator.__rshift__),
        '__lshift__' : lambda self, num: __performOp(num, operator.__lshift__),
        '__inv__' : lambda self: BinaryNum(not self.decimal, len(bin(self.decimal))),
        '__neg__' : lambda self: BinaryNum(-self.decimal, len(bin(self.decimal))),
        '__int__' : lambda self: self.decimal,
        '__str__' : lambda self: self.binary,
        'hex' : lambda self: hex(self.decimal),
        'resize' : lambda self, size: BinaryNum(self.decimal, size)
    })

print(x + y)
print((x+y).resize(30))
# print(int(x[1]))
