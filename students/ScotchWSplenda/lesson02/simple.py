import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"  # Add/modify these
logging.basicConfig(level=logging.DEBUG, format=log_format)                   # two lines

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)
