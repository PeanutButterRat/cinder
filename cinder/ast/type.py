from dataclasses import dataclass

from llvmlite import ir


@dataclass
class Type:
    def to_ir(self):
        pass

    @staticmethod
    def from_string(type):
        if type == "i32":
            return i32()
        else:
            raise ValueError(f"unknown type ({type})")

    def __str__(self):
        return type(self).__name__


@dataclass
class i32(Type):
    def to_ir(self):
        return ir.IntType(32)
