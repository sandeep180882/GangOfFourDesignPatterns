"""LSP violations: subclasses that break the base-class contract."""


class Bird:
    def fly(self) -> str:
        return "flying"


class Sparrow(Bird):
    pass


class Penguin(Bird):
    def fly(self) -> str:
        # Strengthens the precondition: callers of Bird.fly() never expected this.
        raise NotImplementedError("penguins cannot fly")


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def set_width(self, w: float) -> None:
        self.width = w

    def set_height(self, h: float) -> None:
        self.height = h

    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    # Breaks the postcondition "setting width leaves height unchanged".
    def set_width(self, w: float) -> None:
        self.width = self.height = w

    def set_height(self, h: float) -> None:
        self.width = self.height = h
