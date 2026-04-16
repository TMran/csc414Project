from dataclasses import dataclass

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class Const:
    value: int

@dataclass(frozen=True)
class Not:
    child: object

@dataclass(frozen=True)
class And:
    left: object
    right: object

@dataclass(frozen=True)
class Or:
    left: object
    right: object