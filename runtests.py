#!/usr/bin/env python3
import argparse
import os
import sys

import django
from django.test.runner import DiscoverRunner

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbosity',
                        type=int, default=1, help='verbosity')
    parser.add_argument('--failfast', action='store_true', default=False,
                        help='stop tests on the first failure')
    parser.add_argument('tests', nargs='*', default=['tests'],
                        help='which tests to run')

    return parser.parse_args()


def main():
    args = parse_args()
    verbosity = args.verbosity
    failfast = args.failfast
    tests = args.tests

    django.setup()

    test_runner = DiscoverRunner(verbosity=verbosity, failfast=failfast)
    failures = test_runner.run_tests(tests)

    sys.exit(failures)


if __name__ == '__main__':
    main()
