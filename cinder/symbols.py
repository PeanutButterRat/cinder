class Symbols:
    def __init__(self):
        self.scopes = [{}]

    def __setitem__(self, symbol, data):
        self.scopes[-1][symbol] = data

    def __getitem__(self, symbol):
        for scope in reversed(self.scopes):
            if symbol in scope:
                return scope[symbol]

        raise KeyError(f"undefined symbol: '{symbol}'")

    def push(self):
        self.scopes.append({})
        return self

    def pop(self):
        if not (len(self.scopes) >= 2):
            raise RuntimeError("attempted to remove base scope from symbol table")

        self.scopes.pop()
        return self
