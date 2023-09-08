import sys
import inspect
import argparse
from uuid import uuid4

class EasyArgParser:
    def __init__(self):
        self.registry = []
    def register(self, func):
        self.registry.append(func)
        return func
    def run(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest=(dest := uuid4()))
        funcs = {}
        for func in self.registry:
            funcs[func.__name__] = func
            sig = inspect.signature(func)
            p = subparsers.add_parser(func.__name__, help=func.__doc__)
            for param in sig.parameters:
                if type(param.annotation) == inspect._empty:
                    raise Exception(f"You must annotate all parameters. Parameter {param.name} is not annotated.")
                if type(param.default) == inspect._empty:
                    p.add_argument(f'--{param.name}', type=param.annotation)
                else:
                    p.add_argument(param.name, type=param.annotation)


        args = vars(parser.parse_args(sys.argv[1:]))
        func = funcs[args[dest]]
        del args[dest]
        func(*args)

                
        

        
            
