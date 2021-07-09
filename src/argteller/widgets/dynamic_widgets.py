from .widgets import ParamChoiceWidget
from .widgets import Custom1
from .widgets import ParamTextWidget
from .widgets import ParamSetterWidget

try:

    from IPython.display import display
    import ipywidgets as widgets
    from ipywidgets import HBox, Label, VBox
    from ipywidgets import Button, Layout, HTML
    from traitlets import MetaHasTraits

except ModuleNotFoundError:

    class VBox():
        pass

    class MetaHasTraits():
        pass


class DynamicWidget(VBox):
    # https://stackoverflow.com/questions/60998665/is-it-possible-to-make-another-ipywidgets-widget-appear-based-on-dropdown-select
    
    def __init__(self, topic, node, widget_dicts, initial_event):

        if not isinstance(VBox, MetaHasTraits):
            return
        
        self.initial_event = initial_event

        self.topic = topic
        self.node = node
        
        self.widget_dicts = widget_dicts

        default_value = None
        preset_value = None

        if node.primary_type=='param' or node.primary_type=='optional':

            is_optional_param = node.primary_type=='optional'

            # Set aside the default and preset values
            default_value = node.default_value
            preset_value = node.preset_value

            # if choiceable param, add choices here
            if node.secondary_type=='option':
                
                options = node.get_children_names() 

                if self.node.name in self.widget_dicts[self.topic]:

                    self.widget = self.widget_dicts[self.topic][self.node.name]

                else:
                    
                    self.widget = ParamChoiceWidget(
                        name=self.node.name, 
                        options=options, 
                        default_value=default_value, 
                        preset_value=preset_value, 
                        optional=is_optional_param,
                        initial_event=self.initial_event)
                    
                    self.widget_dicts[self.topic][self.node.name] = self.widget.widget
                   
            elif node.secondary_type=='string':

                if self.node.name in self.widget_dicts[self.topic]:

                    widget = self.widget_dicts[self.topic][self.node.name]

                    self.widget = ParamTextWidget(
                        name=self.node.name, 
                        default_value=default_value,
                        preset_value=preset_value,
                        optional=is_optional_param, 
                        widget=widget,
                        initial_event=self.initial_event)

                else:
                
                    self.widget = ParamTextWidget(
                        name=self.node.name, 
                        default_value=default_value,
                        preset_value=preset_value,
                        optional=is_optional_param,
                        initial_event=self.initial_event)
                    
                    self.widget_dicts[self.topic][self.node.name] = self.widget.widget
                   
            elif node.secondary_type=='string_sample':

                if self.node.name in self.widget_dicts[self.topic]:

                    self.widget = self.widget_dicts[self.topic][self.node.name]

                else:
                
                    string_sample_node = node.children[0]
                    string_sample = string_sample_node.name
                    
                    self.widget = ParamTextWidget(
                        name=self.node.name, 
                        example=string_sample, 
                        default_value=default_value,
                        preset_value=preset_value,
                        initial_event=self.initial_event)
                    
                    self.widget_dicts[self.topic][self.node.name] = self.widget.widget
                
        elif node.primary_type=='custom1':
            
            self.widget = Custom1()
            
            self.widget_dicts[self.topic][self.node.name] = 'custom1'

        elif node.primary_type=='param_setter':

            topic, node_name = node.name.split('/')

            # print(topic, node_name)
            # print(self.widget_dicts[topic])

            widget = self.widget_dicts[topic][node_name]

            self.widget = ParamSetterWidget(
                name=self.node.name, 
                widget=widget, 
                default_value=self.node.default_value,
                preset_value=preset_value,
                initial_event=self.initial_event)
        
        self.dynamic_widget_holder = VBox()
        
        children = [
            self.widget, 
            self.dynamic_widget_holder
        ]
        
        self.widget.children[1].observe(self._add_widgets, names=['value'])

        super().__init__(children=children)

        # Manually trigger the children widget node initialization if there
        # is default or preset value
        if (node.primary_type=='param' or node.primary_type=='optional') and (default_value or preset_value) and not self.initial_event.isSet():

            child_node = self.node.get_child_by_name(preset_value)

            new_widgets = []
            
            for child_node in self.node.children:

                # This is so that if the default value and preset value were different,
                # the widgets do not follow down both of the branches.
                if preset_value is not None:
                    checked_value = preset_value
                elif default_value is not None:
                    checked_value = default_value
                else:
                    checked_value = None
                
                if child_node.name==checked_value and (child_node.secondary_type=='param' or child_node.secondary_type=='param_setter'):
                    
                    for _child_node in child_node.children:
                    
                        widget = DynamicWidget(self.topic, _child_node, self.widget_dicts, self.initial_event)
                        new_widgets.append(widget)
            
            self.dynamic_widget_holder.children = tuple(new_widgets)

    def _add_widgets(self, widg):
        
        # if node is choiceable param
        # and if any of the choice node has param nodes
        
        # check the choice of current widget
        # and that choice has value1
        
        # look at the choice param value1, and see if that has any children
        # then loop over those children and add them all to the new_widgets
        
        input_value = widg['new']

        # print('asdfasdfasdfasdfasdf', input_value)
        
        child_node = self.node.get_child_by_name(input_value)

        # print(child_node)

        new_widgets = []
        
        for child_node in self.node.children:

            print(child_node, '1')
            
            if child_node.name==input_value and (child_node.secondary_type=='param' or child_node.secondary_type=='param_setter'):

                print(child_node.name, '2')
                
                for _child_node in child_node.children:

                    print(_child_node, '3')
                
                    widget = DynamicWidget(self.topic, _child_node, self.widget_dicts, self.initial_event)
                    new_widgets.append(widget)
        
        self.dynamic_widget_holder.children = tuple(new_widgets)

    # def get_param_names(self):
        
    def set_input(self, key, value):
         
        self.recur(self, key, value)

    def recur(self, node, key, value):

        if not (isinstance(node, widgets.widget_box.VBox) or 
                isinstance(node, DynamicWidget)):
            return

        if isinstance(node, DynamicWidget):

            if key in node.widget_dicts:

                node.widget_dicts[key].value = str(value)

        for child in node.children:

            self.recur(child, key, value)


class DynamicSwitch(VBox):
    
    def __init__(self, widget1, widget2):

        if not isinstance(VBox, MetaHasTraits):

            return
        
        self.widget1 = widget1
        self.widget2 = widget2
        
        self.widget = widgets.Button()
        
        self.widget.description = "Next"
        
        self.dynamic_widget_holder = VBox()

        self.dynamic_widget_holder.children = [self.widget1]
        
        children = [
            self.dynamic_widget_holder,
            self.widget
        ]
        
        self.widget.on_click(self._switch_widgets)
        
        super().__init__(children=children)
        
    def _switch_widgets(self, widg):
        
        if self.widget.description=='Back':

            new_widget = self.widget1
            self.widget.description = "Next"
            
        else:
            
            new_widget = self.widget2
            self.widget.description = "Back"
        
        self.dynamic_widget_holder.children = [new_widget]
        
