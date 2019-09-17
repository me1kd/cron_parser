# -*- coding: utf-8 -*-
import argparse
import sys
import logging

from cron_parser import __version__

__author__ = "Kewei Duan"
__copyright__ = "Kewei Duan"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def isInt(astring):
    """ Is the given string an integer? """
    try:
        int(astring)
    except ValueError:
        return 0
    else:
        return 1


def isLongmonth(s_check):
    for item in ['1 ', '3 ', '5 ', '7 ', '8 ', '10 ', '12 ']:
        if item in s_check:
            return True
    return False


def interpret_args(l_args):
    """ Interpret the args list

    Args:
      l_args ([str]): command line parameters as list of strings

    Returns:
      None
    """
    minute, hour, day_m, month, day_w, command = l_args
    _logger.info("Start to interpret each arguement")
    print('{:<15} {:<}'.format('minute', interpret_value(minute, 'min')))
    print('{:<15} {:<}'.format('hour', interpret_value(hour, 'hour')))
    month_result = interpret_value(month, 'month')
    if month_result == '2 ':
        print('{:<15} {:<}'.format('day of month',
                                   interpret_value(day_m, 'day_m', 1)))
    else:
        if isLongmonth(month_result):
            print('{:<15} {:<}'.format('day of month',
                                       interpret_value(day_m, 'day_m')))
        else:
            print('{:<15} {:<}'.format('day of month',
                                       interpret_value(day_m, 'day_m', 2)))
    print('{:<15} {:<}'.format('month', month_result))
    print('{:<15} {:<}'.format('day of week', interpret_value(day_w, 'day_w')))
    print('{:<15} {:<}'.format('command', command))


def interpret_value(s_value, s_type, option=0):
    """ Interpret each arg value

    Args:
      s_value (str): command line parameter
      s_type (str): command line parameter type from 
          ['min', 'hour', 'day_m', 'month', 'day_w']

    Returns:
      String: valid numbers for parameter type seperated by space
    """
    _logger.info("Start to interpret {} arguement".format(s_type))
    l_out = []
    s_out = ''
    allowed_start = 0
    allowed_end = 0
    if s_type == 'min':
        allowed_start = 0
        allowed_end = 59
    elif s_type == 'hour':
        allowed_start = 0
        allowed_end = 23
    elif s_type == 'day_m':
        if option == 1:
            allowed_start = 1
            allowed_end = 29
        elif option == 2:
            allowed_start = 1
            allowed_end = 30
        else:
            allowed_start = 1
            allowed_end = 31
    elif s_type == 'month':
        allowed_start = 1
        allowed_end = 12
    elif s_type == 'day_w':
        allowed_start = 1
        allowed_end = 7
    else:
        _logger.debug("s_type content is not expected")
        raise ValueError

    if s_value == '*':
        for i in range(allowed_start, allowed_end+1):
            s_out += str(i) + ' '
        return s_out
    else:
        values = filter(None, [x.strip() for x in s_value.split(',')])
        for value in values:
            if '-' in value:
                start = allowed_start
                end = allowed_end
                step = 1
                if '/' in value:
                    try:
                        start, tmp = [
                            x.strip()
                            for x in value.split('-')
                        ]
                        start = int(start)
                        if start < allowed_start:
                            _logger.debug(
                                "Value is smaller than allowed range of {}}", s_type)
                            raise ValueError
                        end, step = [
                            int(x.strip())
                            for x in tmp.split('/')
                        ]
                        if end > allowed_end:
                            _logger.debug(
                                "Value is greater than allowed range of {}}", s_type)
                            raise ValueError
                    except ValueError:
                        _logger.debug("ValueError raised")
                        raise ValueError
                else:
                    try:
                        start, end = [
                            int(x.strip())
                            for x in value.split('-')
                        ]
                    except ValueError:
                        _logger.debug("ValueError raised")
                        raise ValueError
                if start >= end:
                    _logger.debug("Start value is greater than end value")
                    raise ValueError
                else:
                    for i in range(0, end+1, step):
                        if i >= start and i <=end:
                            l_out.append(str(i))
                continue

            if '/' in value:
                v, interval = [x.strip() for x in value.split('/')]
                interval = int(interval)
                if v != '*':
                    _logger.debug("Value is not allowed in / clause")
                    raise ValueError
                else:
                    for i in range(0, allowed_end+1, interval):
                        if i >= allowed_start and i <= allowed_end:
                            l_out.append(str(i))
                continue

            if isInt(value):
                l_out.append(value)
            else:
                _logger.debug(
                    "The string is expected to be an Int, but it is not")
                raise ValueError
        l_out = sorted(list(set(l_out)))
        for item in l_out:
            s_out += item + ' '
        return s_out


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a cron string parser")
    parser.add_argument(
        dest="string",
        help="Input String",
        nargs='*',
        type=str,
        default=False,
        metavar="String")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    size_args = len(args.string)
    if size_args != 6:
        print("Wrong arguments size")
    interpret_args(args.string)
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
