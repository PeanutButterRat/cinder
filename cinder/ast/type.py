from dataclasses import dataclass
from typing import List

from llvmlite import ir


@dataclass
class Type:
    def to_ir(self):
        pass

    @staticmethod
    def from_string(name):
        symbols = globals()

        if name in symbols and isinstance(symbols[name], type):
            return symbols[name]()
        else:
            raise ValueError(f"unknown type ({name})")

    def __str__(self):
        return type(self).__name__


@dataclass
class i32(Type):
    def to_ir(self):
        return ir.IntType(32)


@dataclass
class bool(Type):
    def to_ir(self):
        return ir.IntType(1)


@dataclass
class Function(Type):
    return_type: Type

    def to_ir(self):
        return ir.FunctionType(self.return_type.to_ir(), [])
