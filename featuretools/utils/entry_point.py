import time
from functools import wraps

import pkg_resources


def entry_point(name):
    def inner_function(func):
        @wraps(func)
        def function_wrapper(*args, **kwargs):
            """ function_wrapper of greeting """

            # collect and initialize all registered entry points
            entry_points = []
            for entry_point in pkg_resources.iter_entry_points(name):
                entry_point = entry_point.load()
                entry_points.append(entry_point())

            # send arguments before function is called
            for ep in entry_points:
                # todo: update kwargs with args but named
                ep.on_call(kwargs)

            try:
                # call function
                start = time.time()
                return_value = func(*args, **kwargs)
                runtime = time.time() - start
            except Exception as e:
                runtime = time.time() - start
                # send error
                for ep in entry_points:
                    ep.on_error(error=e,
                                runtime=runtime)
                raise e

            # send return value
            for ep in entry_points:
                ep.on_return(return_value=return_value,
                             runtime=runtime)

            return return_value

        return function_wrapper
    return inner_function