import os
import sys
import logging.config
import argparse
import yaml
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup

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

    def extract_table(self, browser) -> None:
        logging.info('extracting table....')
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # logging.info(soup.prettify())
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        table = soup.find('table', {'class': 'panelGrig'})  # Grab the first table
        for row in table.find_all('tr'):
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
            # Handle column names if we find them
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")
        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        logging.info(f'Datafame credentials: {df}')
        sleep(80)


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

    try:
        if args.config:
            config = yaml.load(args.config, Loader=yaml.FullLoader)
            # getting value from config file
            personal_information = config['PERSONAL_INFORMATION']

        client_code(
            sythagBot=SythagBot(),
            execution=args.execution,
            personal_information=personal_information
        )
    except Exception as e:
        logging.error(f'something went wrong while scraping data from SYSTHAG portal: {e}')

    logging.info('end systhag bot\'s execution.')


