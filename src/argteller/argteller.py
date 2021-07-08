from .tree.tree_parser import parse_dsl
from .tree.tree_builder import construct_tree
from .builder.access_object import AccessObject
from .builder.get_control_panel import get_control_panel

try:
    
    from IPython.display import display

except ModuleNotFoundError:

    pass

import inspect
import os
import functools
import warnings


class ArgtellerClassDecorator():
    
    def __init__(self, dsl, override=False):
        
        if os.path.exists(dsl):
            with open(dsl) as f:
                self.dsl = f.read()

        elif isinstance(dsl, str):
            self.dsl = dsl
            
        self.override = override
        
    def __call__(self, cls):
        
        class Wrapped(cls):
            
            def __init__(cls_self, *args, **kwargs):
                
                source_obj_dict = {}
                
                # The signature of the class being decorated.
                original_signature = inspect.signature(cls.__init__)
                
                params = list(original_signature.parameters.values())
                
                param_names = [param.name for param in params]
                param_types = [param.kind for param in params]
                
                # Because the inner __init__ method signature only consists
                # of VAR_POSITIONAL and VAR_KEYWORD type parameter, we need
                # to check manually.
                
                # If **kwargs is not in the original_signature,
                # we cannot accept kwargs not in the param_names.
                if not inspect.Parameter.VAR_KEYWORD in param_types:
                    
                    for key, value in kwargs.items():
                    
                        if not key in param_names:

                            raise TypeError("__init__() got an unexpected keyword argument '{}'".format(
                                key))
                
                # If *args is not in the original_signagure,
                # we cannot accept args longer than there are
                # POSITIONAL_OR_KEYWORD type args in the signature.
                if not inspect.Parameter.VAR_POSITIONAL in param_types:
                    
                    num_pos_or_kw = len([param_type for param_type in param_types if
                                         param_type==inspect.Parameter.POSITIONAL_OR_KEYWORD])
                    
                    if len(args) > num_pos_or_kw - 1:  # -1 for the implicit self argument
                        
                        raise TypeError("__init__() takes {} positional arguments but {} were given".format(
                            num_pos_or_kw, len(args) + 1))  # +1 to count for the implicit self argument
                
                # Check the user passed arguments at the __init__ method invocation.
                check_pos_args = []
                
                for i, param in enumerate(params):
                    
                    if i==0:  # Skip the implicit self argument.
                        continue
                    
                    if param.kind==inspect.Parameter.POSITIONAL_OR_KEYWORD:
                        
                        if len(args)>=i:
                            
                            setattr(cls_self, param.name, args[i-1])
                            
                        elif param.name in kwargs:
                            
                            setattr(cls_self, param.name, kwargs[param.name])
                            del kwargs[param.name]
                            
                        else:
                            
                            if param.default==inspect._empty:
                            
                                check_pos_args.append(param.name)
                            
                            # The Method decorator will source from the source
                            # object here. But for Class decorator, because the 
                            # widgets are dynamic, we cannot do that.
                            
                            # We will only check to see if the missing argument
                            # is at least found in the widget param namespace.
                        
                # The Method decorator can check the missing_positional_arguments
                # to throw TypeError missing argument exception. But with the 
                # Class decorator, we cannot do that because we are waiting on the
                # user to interact with the widget. 
                # So instead, we will rely on the requirement signals of the widgets.

                parsed_node_data = parse_dsl(self.dsl)
                root, node_dicts = construct_tree(parsed_node_data)
                cls_self.__access_object__ = AccessObject(root, node_dicts)

                if cls_self.__access_object__.module_found:

                    cls_self.__control_panel__ = get_control_panel(cls_self.__access_object__)
                    display(cls_self.__control_panel__)
                
                    widget_params = cls_self.__access_object__.get_params()
                    cls_self.topic = None

                else:

                    warnings.filterwarnings('always')

                    warnings.warn("Please install 'IPython' and 'ipywidgets' modules to enable widgets.", ImportWarning)

                    warnings.filterwarnings(action='ignore', category=DeprecationWarning, module='ipykernel')
                    
                    widget_params = []

                # Below missing positional arguments cannot be found in the widget 
                # param namespace.
                
                missing_pos_args = []
                
                for check_pos_arg in check_pos_args:
                    
                    if check_pos_arg not in widget_params:
                        
                        missing_pos_args.append("'{}'".format(check_pos_arg))
                        
                if len(missing_pos_args) > 0:

                    missing_args = " and ".join(missing_pos_args)

                    raise TypeError("__init__() missing {} required positional arguments: {} !".format(
                        len(missing_pos_args), missing_args))

            def __getattr__(cls_self, elem):
                """This magic method is invoked when the __getattribute__ 
                magic method throws an exception. This is a natural way to
                query the widgets when the user has not supplied a required
                argument, or when the user queries for a parameter that is 
                not specified in the original signature.
                """
                if cls_self.__access_object__.module_found and elem in cls_self.__access_object__.get_params():

                    return cls_self.__access_object__.get_value(elem, cls_self.topic)

                else:
                    
                    raise AttributeError("'{}' object has no attribute '{}'!".format(cls.__name__, elem))
                
            def __settopic__(cls_self, topic):
                
                cls_self.topic = topic
                
            def __resettopic__(cls_self):
                
                cls_self.topic = None

            def __getparams__(cls_self):

                return cls_self.__access_object__.get_params(cls_self.topic)

            def __getvalue__(cls_self, param):

                return cls_self.__access_object__.get_value(param, cls_self.topic)

        return Wrapped

def ArgtellerMethodDecorator(source_name, topic=None):
    
    def decorator(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            
            original_signature = inspect.signature(func)
            
            new_args = [self]
    
            params = list(original_signature.parameters.values())
            
            has_VAR_POSITIONAL = inspect.Parameter.VAR_POSITIONAL in [param.kind for param in params]
            has_VAR_KEYWORD = inspect.Parameter.VAR_KEYWORD in [param.kind for param in params]
        
            
            if source_name in kwargs:
                
                __source_obj__ = kwargs[source_name]
                
                __source_obj__.__settopic__(topic)
                
                del kwargs[source_name]
                
            else:
                
                __source_obj__ = None

            missing_positional_arguments = []
            
            num_hard_pos = 0
            num_pos = 0
                
            for i, param in enumerate(params):      
                
                if i==0:  # Skip the implicit self argument.
                    continue
 
                if param.kind==inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    
                    # Keep track of the number of positional arguments to check
                    # excessive argument input error.
                    if param.default==inspect._empty:
                        num_hard_pos += 1
                    num_pos += 1
                    
                    # We can assume that the first args belong to the
                    # position argument list.
                    if len(args)>=i:
                        
                        print(args[i-1], args)
                        
                        new_args.append(args[i-1])
                    
                    elif param.name in kwargs:
                        
                        new_args.append(kwargs[param.name])
                        del kwargs[param.name]
                        
                    else:
                        
                        if __source_obj__ is not None:
                        
                            if param.name in __source_obj__.__getparams__():

                                new_args.append(__source_obj__.__getvalue__(param.name))

                        else:
                            
                            if param.default==inspect._empty:
                                
                                missing_positional_arguments.append("'{}'".format(param.name))
                            
                            new_args.append(param.default)
                            
            if not has_VAR_POSITIONAL and num_pos < len(args):
                
                # Add 1 for the implicit self argument.
                if num_hard_pos > 0:
                    
                    raise TypeError("__init__() takes {} positional arguments but {} were given".format(
                        num_pos+1, len(args)+1))
                    
                else:
                    
                    raise TypeError("__init__() takes from {} to {} positional arguments but {} were given".format(
                        num_hard_pos+1, num_pos+1, len(args)+1))

            if len(missing_positional_arguments) > 0:

                missing_args = " and ".join(missing_positional_arguments)

                raise TypeError("__init__() missing {} required positional arguments: {} !".format(len(missing_positional_arguments), missing_args))
                        
            cr = func(*new_args, **kwargs) # call original function

            return cr

        return wrapper
    
    return decorator

