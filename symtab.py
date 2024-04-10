from tabEntry import TableEntry

class SymbolTable:
    def __init__(self):
        self.entries = []
        self.parent = None
        self.children = []

    def insert(self, identifier, kind, type_):
        if any(entry.identifier == identifier for entry in self.entries):
            return False
        self.entries.append(TableEntry(identifier, kind, type_))
        return True

    def lookup(self, identifier):
        for entry in self.entries:
            if entry.identifier == identifier:
                return entry
        return self.parent.lookup(identifier) if self.parent else None

    def delete(self, identifier):
        for i, entry in enumerate(self.entries):
            if entry.identifier == identifier:
                del self.entries[i]
                return True
        return False

    def enter_scope(self):
        new_scope = SymbolTable()
        new_scope.parent = self
        self.children.append(new_scope)
        return new_scope

    def exit_scope(self):
        return self.parent if self.parent else self

    def serialize(self):
        return {
            "entries": [entry.to_dict() for entry in self.entries],
            "children": [child.serialize() for child in self.children]
        }

    def deserialize(self, data):
        self.entries = [TableEntry.from_dict(entry) for entry in data.get("entries", [])]
        self.children = [child for child in (SymbolTable().deserialize(child_data) for child_data in data.get("children", [])) if child]
