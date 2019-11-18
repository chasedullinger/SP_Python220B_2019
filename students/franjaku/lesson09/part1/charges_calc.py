"""
    Returns total price paid for individual rentals
    Update this module to be able to toggle logging on and off with a decorator

"""
import argparse
import json
import datetime
import math
import logging

# Setup logging params
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

LOG_DICT = {'0': 60,
            '1': 40,
            '2': 30,
            '3': 10}


def logging_decorator(func):
    """Any functioned passed in turns console logging off for that function"""
    def turn_log_off(*args, **kwargs):
        LOGGER.setLevel(70)
        func(*args, **kwargs)
        LOGGER.setLevel(logging.DEBUG)
    return turn_log_off


def parse_cmd_arguments():
    """Parse the inputs/outputs to setup input and outout files"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', help='input JSON file', required=True)
    parser.add_argument('-o', '--output', help='output JSON file', required=True)
    parser.add_argument('-d', '--debug', help='debug level', required=False, default='1')

    return parser.parse_args()


def load_rentals_file(filename):
    """Load the rental file and inform the user if not possible."""
    logging.debug('Loading data from %s', filename)
    try:
        with open(filename) as file:
            data = json.load(file)
            logging.debug('Data successfully loaded.')
    except FileNotFoundError:
        logging.error('Failed to load data from %s', filename)
        data = []
    return data


def calculate_additional_fields(data):
    """Calculate additional data for each rental id in the data structure."""
    # capturing rental_id to better help debugging, changed var names to be more descriptive
    for rental_id, rental_data in data.items():
        # capturing beginning of each rental calculation
        logging.debug('Calculating additional data for %s', rental_id)

        # added try/except blocks to handle each step of the calculation
        try:
            # check if all values exist, raise error if they don't and exit program
            for data_id in rental_data.keys():
                if rental_data[f'{data_id}'] == '':
                    logging.warning('%s: %s is not defined.', rental_id, data_id)
                    raise ValueError

            rental_start = datetime.datetime.strptime(rental_data['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(rental_data['rental_end'], '%m/%d/%y')

            # catch if user start and end dates are flipped
            if rental_end < rental_start:
                logging.error('%s: Rental end date before rental start date.', rental_id)
                raise ValueError

            try:
                rental_data['total_days'] = (rental_end - rental_start).days
                rental_data['total_price'] = \
                    rental_data['total_days'] * rental_data['price_per_day']
                rental_data['sqrt_total_price'] = math.sqrt(rental_data['total_price'])

                # check that units rented is not zero
                if rental_data['units_rented'] == 0:
                    logging.error('%s: 0 rental units indicated.', rental_id)
                    raise ZeroDivisionError

                rental_data['unit_cost'] = rental_data['total_price'] / rental_data['units_rented']
            except ZeroDivisionError:
                logging.error('Could not calculate additional data for %s.', rental_id)

        except ValueError:
            logging.error('Could not calculate additional data for %s.', rental_id)

    return data


def save_to_json(filename, data):
    """Save the data to the output JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parse_cmd_arguments()
    # choose logging functions based on input or default to none
    # Toggle all console logging of if args.debug == 0
    if args.debug == '0':
        load_rentals_file = logging_decorator(load_rentals_file)
        calculate_additional_fields = logging_decorator(calculate_additional_fields)
        save_to_json = logging_decorator(save_to_json)

    logging.debug('Input file: %s Output file: %s', args.input, LOG_FILE)
    all_data = load_rentals_file(args.input)
    all_data = calculate_additional_fields(all_data)
    save_to_json(args.output, all_data)
