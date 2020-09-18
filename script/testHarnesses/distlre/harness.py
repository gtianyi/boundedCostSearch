#!/usr/bin/python
'''
Harness for running bounded cost search experiments on ai servers

Author: Tianyi Gu
Date: 09/18/2020
'''

from distlre import DistLRE, Task, RemoteHost

executor = DistLRE(local_threads=1)

task = Task(command='ls ~', meta='META', time_limit=10, memory_limit=10)
future = executor.submit(task)
executor.execute_tasks()
executor.wait()
print(future.result().output)


executor = DistLRE(remote_hosts=[RemoteHost(
    'ai1.cs.unh.edu', username='gu', key_file_path = "/home/aifs1/gu/.ssh/id_rsa"
)])

task = Task(command='ls ~', meta='META', time_limit=10, memory_limit=10)
future = executor.submit(task)
executor.execute_tasks()
executor.wait()
print(future.result().output)
