from ..tree.tree_parser import parse_dsl
from ..tree.tree_builder import construct_tree
from ..builder.access_object import AccessObject
from ..builder.get_control_panel import get_control_panel

try:
    
    from IPython.display import display

except ModuleNotFoundError:

    pass

import inspect
import os
import warnings


class ArgtellerClassDecorator():
    
    def __init__(self, dsl, presetter=None, override=False):
        
        if os.path.exists(dsl):
            with open(dsl) as f:
                self.dsl = f.read()

        elif isinstance(dsl, str):
            self.dsl = dsl
            
        self.override = override
        self.presetter = presetter
        
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
                root, node_dicts, value_dicts = construct_tree(parsed_node_data)
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

            def __getattr__(cls_self, param):
                """This magic method is invoked when the __getattribute__ 
                magic method throws an exception. This is a natural way to
                query the widgets when the user has not supplied a required
                argument, or when the user queries for a parameter that is 
                not specified in the original signature.
                """
                if cls_self.__access_object__.module_found and param in cls_self.__access_object__.get_params():

                    return cls_self.__getvalue__(param)

                else:
                    
                    raise AttributeError("'{}' object has no attribute '{}'!".format(cls.__name__, param))
                
            def __settopic__(cls_self, topic):
                
                cls_self.topic = topic
                
            def __resettopic__(cls_self):
                
                cls_self.topic = None

            def __getparams__(cls_self):

                return cls_self.__access_object__.get_params(cls_self.topic)

            def __getvalue__(cls_self, param):
                """The return values will be automatically typecasted. 

                '' from Text widget will be None
                int castable values will be casted to int
                float castable values will be casted to float (assuming it was not int)
                """
                try:
                    value = cls_self.__access_object__.get_value(param, cls_self.topic)
                except TypeError as e:
                    raise TypeError(str(e) + ' Invoke  obj.__settopic__(topic) method to set topic. Invoke obj.__resettopic__() to reset it.')

                if value is None:
                    return value

                try:    
                    value = int(value)
                    return value
                except ValueError:
                    pass
                
                try:
                    value = float(value)
                    return value
                except ValueError:
                    pass
                
                try:
                    value = eval(value)
                    return value
                except (SyntaxError, NameError):
                    pass

                if value=='':
                    return None
                
                return value

        return Wrapped

