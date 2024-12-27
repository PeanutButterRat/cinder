from lark import Lark

with open("cinder/cinder.lark") as file:
    GRAMMAR = file.read()
    parser = Lark(GRAMMAR)
