#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.cache import cache


class a:
    def __init__(self):
        print("hh")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CheckBill.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    #
    # cache.set('flag', 0, 60 * 60 * 24)
    # res = cache.get('flag')


    # a_1  = a()
    # a_2 = a()
    #cache.delete('work_status')
    # cache.set('flag', a_1, 60 * 60 * 24)
    # res_1 = cache.get('flag')
    # print(hash(res_1))
    # cache.set('flag', a_1, 60 * 60 * 24)
    # res_2 = cache.get('flag')
    # print(hash(res_2))
    # res = cache.get('flag')
    # print(res)
    # print(type(res))


if __name__ == '__main__':
    main()
