class Symbols:
    def __init__(self):
        self.scopes = [{}]

    def __setitem__(self, symbol, value):
        self.scopes[-1][symbol] = value

    def __getitem__(self, symbol):
        for scope in reversed(self.scopes):
            if symbol in scope:
                return scope[symbol]

        raise KeyError(f"undefined symbol ({symbol})")

    def __contains__(self, symbol):
        for scope in reversed(self.scopes):
            if symbol in scope:
                return True

        return False

    def push(self):
        self.scopes.append({})
        return self

    def pop(self):
        if len(self.scopes) == 1:
            raise RuntimeError("attempted to remove base scope from symbol table")
        else:
            self.scopes.pop()
            return self

    def __str__(self):
        collection = {}

        for scope in self.scopes:
            collection.update(scope)

        return str(collection)
