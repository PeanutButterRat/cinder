from dataclasses import dataclass

from llvmlite import ir

from cinder.ast.node import _Expression, _Statement


@dataclass
class Prt(_Statement):
    expression: _Expression

    def compile(self, module=None, builder=None, symbols=None):
        printf = symbols["printf"]
        expression = self.expression.compile(module, builder, symbols)
        format = builder.bitcast(
            module.get_global("format"), ir.PointerType(ir.IntType(8))
        )
        return builder.call(printf, [format, expression])
