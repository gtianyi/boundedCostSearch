#!/usr/bin/python
'''
Memory limit and time limit wrapper for commands

Author: Tianyi Gu
Date: 09/18/2020
'''

__author__ = 'TianyiGu'

import argparse
from distlre.distlre import DistLRE, Task

def parseArugments():

    parser = argparse.ArgumentParser(description='limitWrapper')

    parser.add_argument(
        '-c',
        action='store',
        dest='command',
        help='command: (default) ls ~',
        default='ls ~')

    parser.add_argument(
        '-m',
        action='store',
        type=float,
        dest='memory',
        help='memory limit:(default) 7.5 (GB)',
        default='7.5')

    parser.add_argument(
        '-t',
        action='store',
        type=int,
        dest='time',
        help='time limit:(default) 600 (seconds)',
        default='600')

    return parser

def main():
    parser = parseArugments()
    args = parser.parse_args()
    print(args)

    executor = DistLRE(local_threads=1)

    task = Task(command=args.command, meta='META', time_limit=args.time, memory_limit=args.memory)
    future = executor.submit(task)
    executor.execute_tasks()
    executor.wait()
    print(future.result().output)


if __name__ == '__main__':
    main()
