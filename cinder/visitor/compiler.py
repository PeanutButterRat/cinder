from llvmlite import ir

from cinder.ast import _Node
from cinder.ast.expressions import String
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

        for format, name in [("%d\n\0", "integer_format"), ("%s\n\0", "string_format")]:
            print_string_type = ir.ArrayType(ir.IntType(8), count=len(format))
            print_string = ir.GlobalVariable(self.module, print_string_type, name=name)
            print_string.global_constant = True
            print_string.initializer = ir.Constant(
                print_string_type, bytearray(format.encode("utf8"))
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
        format_name = (
            "string_format" if isinstance(expression, String) else "integer_format"
        )
        format = self.builder.bitcast(
            self.module.get_global(format_name), ir.PointerType(ir.IntType(8))
        )

        return self.builder.call(printf, [format, self.visit(expression)])

    def String(self, string):
        raw_bytes = bytearray(string.encode("utf8") + b"\0")
        global_name = f"str_{id(string)}"
        global_type = ir.ArrayType(ir.IntType(8), count=len(raw_bytes))

        global_variable = ir.GlobalVariable(self.module, global_type, name=global_name)
        global_variable.global_constant = True
        global_variable.initializer = ir.Constant(global_type, raw_bytes)
        zero = ir.Constant(ir.IntType(32), 0)

        return self.builder.gep(global_variable, [zero, zero], inbounds=True)

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
        return address

    def Assign(self, identifier, type, expression):
        address = self.builder.alloca(type.to_llvm(), name=identifier)
        self.builder.store(self.visit(expression), address)
        self.symbols[identifier] = self.builder.load(address)

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

    def Function(self, name, parameters, return_type, body):
        function = self.symbols[name]

        for parameter, arg in zip(parameters, function.args):
            self.symbols[parameter.name] = arg

        block = function.append_basic_block()
        self.builder = ir.IRBuilder(block)

        self.visit(body)

    def Call(self, name, expressions):
        function = self.symbols[name]
        return self.builder.call(
            function, [self.visit(expression) for expression in expressions]
        )

    def Return(self, expression):
        self.builder.ret(self.visit(expression))
