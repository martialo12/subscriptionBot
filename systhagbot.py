import os
import sys
import logging.config
import argparse
import yaml
from time import sleep

GET_URL = "http://www.systhag-online.cm:8080/SYSTHAG-ONLINE/faces/index.xhtml"

logging.config.fileConfig(os.path.join(os.getcwd(), "config/logging.conf"))

# create logger
logger = logging.getLogger('sythagBot')

from library.systhaglib import SysthagLib


class SythagBot(SysthagLib):
    """
    Concrete classes have to implement all abstract operations of the base
    class. They can also override some operations with a default implementation.
    """

    pass


def client_code(sythagBot: SysthagLib, execution, personal_information) -> None:
    """
    The client code calls the template method to execute the algorithm. Client
    code does not have to know the concrete class of an object it works with, as
    long as it works with objects through the interface of their base class.
    """

    # ...
    sythagBot.template_method(
        get_url=GET_URL,
        execution=execution,
        personal_information=personal_information
    )
    # ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--execution', dest='execution', type=str,
                        help='execution mode(interface/headless)', required=True)
    parser.add_argument('--config', '-c', type=argparse.FileType('r'),
                        help='config file in YAML format', default=None)

    args = parser.parse_args()
    personal_information = ''
    if args.config:
        config = yaml.load(args.config, Loader=yaml.FullLoader)
        # getting value from config file
        personal_information = config['PERSONAL_INFORMATION']
    # args.username
    print("Same client code can work with different subclasses:")
    client_code(
        sythagBot=SythagBot(),
        execution=args.execution,
        personal_information=personal_information
    )
    print("")
