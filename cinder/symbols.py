class Symbols:
    def __init__(self):
        self.scopes = [{}]

    def __setitem__(self, symbol, data):
        self.scopes[-1][symbol] = data

    def __getitem__(self, symbol):
        return self.scopes[-1][symbol]

    def push(self):
        self.scopes.append({})

    def pop(self):
        if not (len(self.scopes) >= 2):
            raise RuntimeError(
                "attempted to remove the base scope from the symbol table"
            )

        self.scopes.pop()
