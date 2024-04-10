class TableEntry:
    def __init__(self, identifier, kind, type_):
        self.identifier = identifier
        self.kind = kind
        self.type = type_

    def to_dict(self):
        return {"identifier": self.identifier, "kind": self.kind, "type": self.type}

    @staticmethod
    def from_dict(data):
        return TableEntry(data['identifier'], data['kind'], data['type'])
