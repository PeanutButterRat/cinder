from lark import Lark

with open("cinder/cinder.lark") as file:
    parser = Lark(file.read())
