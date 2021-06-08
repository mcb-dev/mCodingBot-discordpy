class SpecialType:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<SpecialType {self.name}>"

    def __str__(self):
        return self.name


MISSING = SpecialType("missing")

ZWS = "\u200B"
