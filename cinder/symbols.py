class Symbols(dict):
    def __init__(self, previous=None):
        super().__init__()
        self.previous = previous

    def __getitem__(self, symbol):
        if super().__contains__(symbol):
            return super().__getitem__(symbol)
        elif self.previous is None:
            raise KeyError(f"undefined symbol ({symbol})")
        else:
            return self.previous[symbol]

    def __contains__(self, symbol):
        if super().__contains__(symbol):
            return True
        elif self.previous is None:
            return False
        else:
            return symbol in self.previous

    def push(self):
        return Symbols(self)

    def pop(self):
        if self.previous is None:
            raise RuntimeError("attempted to remove base scope from symbol table")
        else:
            return self.previous
