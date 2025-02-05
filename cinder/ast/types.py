from dataclasses import dataclass
from typing import List

from llvmlite import ir


@dataclass
class Type:
    @staticmethod
    def from_string(type):
        if type == "i32":
            return Integer(32)
        elif type == "bool":
            return Boolean()
        elif type is None:
            return Void()
        else:
            raise ValueError(f"unknown type ({type})")

    def to_llvm(self):
        raise NotImplementedError


@dataclass
class Integer(Type):
    size: int
    signed: bool = True

    def to_llvm(self):
        return ir.IntType(self.size)


@dataclass
class Boolean(Type):
    def to_llvm(self):
        return ir.IntType(1)


@dataclass
class Function(Type):
    parameters: List[Type]
    return_type: Type

    def to_llvm(self):
        args = [arg.type.to_llvm() for arg in self.parameters]
        return ir.FunctionType(self.return_type.to_llvm(), args)


@dataclass
class Void(Type):
    def to_llvm(self):
        return ir.VoidType()
