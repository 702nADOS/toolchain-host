#!/usr/bin/env python3
import argparse
import logging

# inspect
import inspect
import pkgutil
import importlib


from taskgen.distributor import Distributor, AbstractSession
from taskgen.sessions.genode import GenodeSession

from taskgen.taskset import TaskSet
from taskgen.optimization import Optimization
from taskgen.live import AbstractLiveHandler, DefaultLiveHandler

if __name__ == '__main__':
    main()




FORMAT = '%(asctime)-15s %(levelname)s [%(name)s]  %(message)s'

def handle_logging(args):
    _level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format=FORMAT, filename=args.log, level=_level)
    
    
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
    if args.session:
        print('{: <30} | {}'.format("Session classes", "Description"))
        print("-"*80)
        print_classes(AbstractSession, "sessions")


def load_class(path, submodule):
    if path is None:
        return None
    
    # submodules might be tasksets, optimization, lives
    module_name, class_name = "taskgen.{}.{}".format(submodule, path).rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)
    # TODO handle constructor parameters
    # TODO handle not found

def initialize_class(path, submodule):
    _class =load_class(path, submodule)
    if _class is not None:
        return _class()
    
def command_run(args):    
    handle_logging(args)
    
    # load tasksets  (right now, no parameters can be passed.)
    tasksets = initialize_class(args.taskset, "tasksets")

    # load optimization
    optimization = initialize_class(args.optimization, "optimizations")

    # load live handler
    if args.live:
        live_handler = initialize_class(args.live, "lives")
    else:
        live_handler = DefaultLiveHandler()

    # session class
    if args.session:
        session = load_class(args.session, "sessions")
    else:
        session = GenodeSession

    try:
        # initialize distributor
        distributor = Distributor(args.IP,
                                  args.port,
                                  session,
                                  rescan = True,
                                  max_starter = 20, # max pinging threads
                                  max_duration = 60, # be finished in 60 seconds
                                  max_ping = 4) # ping max. 4 seconds
    
        # start (and wait until finished)
        distributor.start(tasksets, optimization, live_handler, wait=True)

        # TODO print current state
    except KeyboardInterrupt:
        # CTRL-C
        pass
    finally:
        distributor.close()
    

    
def main():
    parser = argparse.ArgumentParser(prog="taskgen")
    subparsers = parser.add_subparsers(dest='command')

    # run
    parser_run = subparsers.add_parser('run', help='runs a list of tasksets')
    # run -d
    parser_run.add_argument("-d", "--debug", action='store_true',
                            help="Print debugging information.")
    # run --log-file
    parser_run.add_argument('--log-file', metavar="FILE", dest="log",
                            help="write log to file", type=argparse.FileType('w'))
    # run -p
    parser_run.add_argument('-p', '--port', default=3001, type=int,
                            help='Port, default is port number 3001.')
    # run -t
    parser_run.add_argument('-t', '--taskset', required=True, metavar="CLASS",
                        help='Select a taskset class.')
    # run -l
    parser_run.add_argument('-l', '--live', metavar="CLASS",
                            help='Select a handler for live request results.')
    # run -o
    parser_run.add_argument('-o', '--optimization', metavar="CLASS",
                            help='Select an optimization class.')
    # run -s
    parser_run.add_argument('-s', '--session', metavar="CLASS",
                            help='Select a session class. Default: GenodeSession')
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
    # list -s
    group_list.add_argument('-s', '--session', action='store_true',
                            help="print all available session classes.")

    # parse
    args = parser.parse_args()
    if args.command == 'run':
        command_run(args)
    elif args.command == 'list':
        command_list(args)
        
    