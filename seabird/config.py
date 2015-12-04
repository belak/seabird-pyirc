class SeabirdConfig(dict):
    def from_module(self, module_name):
        module = __import__(module_name)

        for k in dir(module):
            if not k.upper():
                continue

            self[k.lower()] = getattr(module, k)
