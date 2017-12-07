#!/usr/bin/env python3
import argparse
import logging

# inspect
import inspect
import pkgutil
import importlib


from taskgen.distributors.multi_distributor import MultiDistributor
from taskgen.distributors.simple_distributor import SimpleDistributor
from taskgen.distributors.log_distributor import LogDistributor
from taskgen.taskset import TaskSet
from taskgen.optimization import Optimization
from taskgen.live import AbstractLiveHandler

if __name__ == '__main__':
    main()

def handle_logging(args):
    FORMAT = '%(asctime)-15s %(levelname)s [%(name)s]  %(message)s'

    # handle verbosity
    if args.verbosity == 0:
        LEVEL=logging.ERROR
        print("Verbosity: only errors")
    elif args.verbosity == 1:
        LEVEL=logging.WARNING
        print("Verbosity: errors & warning")
    elif args.verbosity == 2:
        LEVEL=logging.INFO
        print("Verbosity: errors, warning & info")
    else:
        LEVEL=logging.DEBUG
        print("Verbosity: errors, warning, info & debug")
    logging.basicConfig(format=FORMAT, level=LEVEL, filename=args.log)
    
    
def print_classes(class_type, submodule):
    is_class_type = lambda x: inspect.isclass(x) and issubclass(x, class_type)
    # submodules might be: tasksets, optimizations, lives
    submodules = pkgutil.iter_modules(["taskgen/{}".format(submodule)])
    for (module_loader, module_name, ispkg) in submodules:
        if not ispkg:
            module_path = 'taskgen.{}.{}'.format(submodule, module_name)
            module = importlib.import_module(module_path)
            # find all classes with subclass Taskset
            for class_name, obj in inspect.getmembers(module, is_class_type):
                if obj.__module__ == module_path:
                    #class_path = module_path + "." + class_name
                    class_path = module_name + "." + class_name
                    class_doc = "" if obj.__doc__ is None else obj.__doc__
                    print('{: <30} | {: <50}'.format(class_path, class_doc))
        
def command_list(args):
    if args.taskset:
        print('{: <30} | {}'.format("TaskSet Class Name", "Description"))
        print("-"*80)
        print_classes(TaskSet, "tasksets")
    if args.live:
        print('{: <30} | {}'.format("Live Handlers", "Description"))
        print("-"*80)
        print_classes(AbstractLiveHandler, "lives")
    if args.optimization:
        print('{: <30} | {}'.format("Optimization classes", "Description"))
        print("-"*80)
        print_classes(Optimization, "optimizations")


def initialize_class(path, submodule):
    if path is None:
        return None
    
    # submodules might be tasksets, optimization, lives
    module_name, class_name = "taskgen.{}.{}".format(submodule, path).rsplit(".", 1)
    ts_class = getattr(importlib.import_module(module_name), class_name)
    # TODO handle constructor parameters
    # TODO handle not found
    return ts_class()
    
def command_run(args):    
    handle_logging(args)
    
    # load tasksets  (right now, no parameters can be passed.)
    tasksets = initialize_class(args.taskset, "tasksets")

    # load optimization
    optimization = initialize_class(args.optimization, "optimizations")

    # load live handler
    live_handler = initialize_class(args.live, "lives")

    # initialize distributor
    if args.pretend:
        distributor = MultiDistributor(args.IP, args.port, ping=False,
                                       distributor_class=LogDistributor)
    else:
        distributor = MultiDistributor(args.IP, args.port)

    
    # start (and wait until finished)
    distributor.live_handler = live_handler
    distributor.start(tasksets, optimization, wait=True)

    # close everything
    distributor.close()
    

    
def main():
    parser = argparse.ArgumentParser(prog="taskgen")
    subparsers = parser.add_subparsers(dest='command')

    # run
    parser_run = subparsers.add_parser('run', help='runs a list of tasksets')
    # run -v
    parser_run.add_argument("-v", "--verbosity", action="count", default=0,
                            help="increase output verbosity")
    # run --log-file
    parser_run.add_argument('--log-file', metavar="FILE", dest="log",
                            help="write log to file", type=argparse.FileType('w'))
    # run -p
    parser_run.add_argument('-p', '--port', type=int, required=True, help='Port')

    # run -t
    parser_run.add_argument('-t', '--taskset', required=True, metavar="CLASS",
                        help='Select a taskset class.')
    # run -l
    parser_run.add_argument('-l', '--live', metavar="CLASS",
                            help='Select a handler for live request results.')
    # run -o
    parser_run.add_argument('-o', '--optimization', metavar="CLASS",
                            help='Select an optimization class.')
    # run --pretend
    parser_run.add_argument('--pretend', action='store_true',
                            help='Pretend to send the tasksets.')
    # run [IP]
    parser_run.add_argument('IP', nargs='+',
                            help='IP address or a range of IP addresses (CIDR format)')

    # list
    parser_list = subparsers.add_parser('list', help='lists available tasksets')
    group_list = parser_list.add_mutually_exclusive_group(required=True)

    # list -t
    group_list.add_argument('-t', '--taskset', action='store_true',
                            help="print all available taskset classes.")
    # list -o
    group_list.add_argument('-o', '--optimization', action='store_true',
                            help="print all available optimization classes.")
    # list -l
    group_list.add_argument('-l', '--live', action='store_true',
                            help="print all available live requesth handler.")

    # parse
    args = parser.parse_args()
    if args.command == 'run':
        command_run(args)
    elif args.command == 'list':
        command_list(args)
        
    
