import os
import logging.config
import argparse
from time import sleep

logging.config.fileConfig(os.path.join(os.getcwd(), "config/logging.conf"))

from library.systhaglib import SysthagLib


class SythagBot(SysthagLib):
    """
    Concrete classes have to implement all abstract operations of the base
    class. They can also override some operations with a default implementation.
    """

    def required_operations1(self) -> None:
        print("ConcreteClass1 says: Implemented Operation1")

    def required_operations2(self) -> None:
        print("ConcreteClass1 says: Implemented Operation2")


def client_code(sythagBot: SysthagLib) -> None:
    """
    The client code calls the template method to execute the algorithm. Client
    code does not have to know the concrete class of an object it works with, as
    long as it works with objects through the interface of their base class.
    """

    # ...
    sythagBot.template_method()
    # ...


if __name__ == "__main__":
    print("Same client code can work with different subclasses:")
    client_code(SysthagLib())
    print("")
