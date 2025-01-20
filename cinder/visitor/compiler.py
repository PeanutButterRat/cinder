from llvmlite import ir

from cinder.ast import _Node
from cinder.symbols import Symbols
from cinder.visitor.visitor import Interpreter


class TreeCompiler(Interpreter):
    def __init__(self, globals):
        super().__init__()
        self.symbols = globals
        self.module = ir.Module()
        self.builder = None

        printf = ir.Function(
            self.module,
            ir.FunctionType(
                ir.IntType(32), [ir.PointerType(ir.IntType(8))], var_arg=True
            ),
            name="printf",
        )

        format = ir.GlobalVariable(
            self.module, ir.ArrayType(ir.IntType(8), count=4), name="format"
        )
        format.global_constant = True
        format.initializer = ir.Constant(
            ir.ArrayType(ir.IntType(8), count=4),
            bytearray("%d\n".encode("utf8") + b"\0"),
        )

        self.symbols["printf"] = printf

    def Program(self, functions):
        for function in functions:
            name = function.name
            type = self.symbols[name].to_llvm()
            self.symbols[name] = ir.Function(self.module, type, name)

        for function in functions:
            self.visit(function)

        return self.module

    def Print(self, expression):
        printf = self.symbols["printf"]
        format = self.builder.bitcast(
            self.module.get_global("format"), ir.PointerType(ir.IntType(8))
        )
        return self.builder.call(printf, [format, self.visit(expression)])

    def Addition(self, left, right):
        return self.builder.add(self.visit(left), self.visit(right))

    def Subtraction(self, left, right):
        return self.builder.sub(self.visit(left), self.visit(right))

    def Multiplication(self, left, right):
        return self.builder.mul(self.visit(left), self.visit(right))

    def Division(self, left, right):
        return self.builder.sdiv(self.visit(left), self.visit(right))

    def Number(self, value):
        return ir.Constant(ir.IntType(32), value)

    def Boolean(self, boolean):
        return ir.Constant(ir.IntType(1), 1 if boolean else 0)

    def Identifier(self, name):
        address = self.symbols[name]
        return self.builder.load(address)

    def Assign(self, identifier, type, expression):
        address = self.builder.alloca(type.to_llvm(), name=identifier)
        self.symbols[identifier] = address
        self.builder.store(self.visit(expression), address)

    def Block(self, statements):
        self.symbols = self.symbols.push()

        for statement in statements:
            self.visit(statement)

        self.symbols = self.symbols.pop()

    def IfElse(self, conditions, blocks, otherwise):
        value = self.visit(conditions[0])
        predicate = self.builder.icmp_signed(
            "!=", value, ir.Constant(ir.IntType(32), 0)
        )

        if len(conditions) >= 2:
            with self.builder.if_else(predicate) as (then, other):
                with then:
                    self.visit(blocks[0])
                with other:
                    self.IfElse(conditions[1:], blocks[1:], otherwise)

        elif otherwise:
            with self.builder.if_else(predicate) as (then, other):
                with then:
                    self.visit(blocks[0])
                with other:
                    self.visit(otherwise)

        else:
            with self.builder.if_then(predicate):
                self.visit(blocks[0])

    def GreaterThan(self, left, right):
        return self.builder.icmp_signed(">", self.visit(left), self.visit(right))

    def GreaterEqual(self, left, right):
        return self.builder.icmp_signed(">=", self.visit(left), self.visit(right))

    def LessThan(self, left, right):
        return self.builder.icmp_signed("<", self.visit(left), self.visit(right))

    def LessEqual(self, left, right):
        return self.builder.icmp_signed("<=", self.visit(left), self.visit(right))

    def NotEqual(self, left, right):
        return self.builder.icmp_signed("!=", self.visit(left), self.visit(right))

    def Equal(self, left, right):
        return self.builder.icmp_signed("==", self.visit(left), self.visit(right))

    def And(self, left, right):
        result = self.builder.and_(self.visit(left), self.visit(right))
        return self.builder.icmp_signed("!=", result, ir.Constant(ir.IntType(32), 0))

    def Or(self, left, right):
        result = self.builder.or_(self.visit(left), self.visit(right))
        return self.builder.icmp_signed("!=", result, ir.Constant(ir.IntType(32), 0))

    def Not(self, expression):
        result = self.builder.not_(self.visit(expression))
        return self.builder.icmp_signed("!=", result, ir.Constant(ir.IntType(32), 0))

    def Function(self, name, return_type, body):
        function = self.symbols[name]
        block = function.append_basic_block()
        self.builder = ir.IRBuilder(block)

        self.visit(body)

    def Call(self, name):
        function = self.symbols[name]
        return self.builder.call(function, [])

    def Return(self, expression):
        self.builder.ret(self.visit(expression))
