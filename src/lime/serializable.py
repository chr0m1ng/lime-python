PRIVATE_TOKEN = '_'

class Serializable:
    def to_json(self):
        return {k: v for k, v in vars(self).items() if not k.startswith(PRIVATE_TOKEN)}