class Scope:
    def __init__(self, data, parent={}):
        self.data = data
        self.parent = parent
        
    def __getitem__(self, key):
        if key in self.data.keys():
            return self.data[key]
        if key in self.parent.keys():
            return self.parent[key]
        raise KeyError(key)
        
    def __setitem__(self, key, value):
        self.data[key] = value
        
    def __delitem__(self, key):
        del self.data[key]
        
    def __str__(self):
        return str(self.data)
        
    def keys(self):
        for key in self.data.keys():
            yield key
        for key in self.parent.keys():
            yield key