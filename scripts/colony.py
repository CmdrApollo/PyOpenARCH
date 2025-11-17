from dataclasses import dataclass

# TODO i don't actually want this to be a dataclass.
@dataclass
class Colony:
    attractiveness: int
    defense       : int
    fertility     : int
    resources     : int