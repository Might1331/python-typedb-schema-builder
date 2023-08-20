class MyType:
    def __init__(self, name: str):
        self.name = name
        self.super_types = set()
        self.abstract = False
        self.roles = set()
        self.attributes = set()

    def AddSuperType(self, type: str):
        self.super_types.add(type)

    def SetAbstract(self, positive: bool):
        self.abstract = positive

    def AddRole(self, relation: str, role: str):
        self.roles.add([relation, role])

    def AddAttribute(self, attribute: str):
        self.attributes.add(attribute)