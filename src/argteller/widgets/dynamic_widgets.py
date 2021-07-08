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
    
    def __init__(self, topic, node, widget_dicts):

        if not isinstance(VBox, MetaHasTraits):
            return
        
        self.topic = topic
        self.node = node
        
        self.widget_dicts = widget_dicts

        if node.primary_type=='param' or node.primary_type=='optional':

            is_optional_param = node.primary_type=='optional'

            # if choiceable param, add choices here
            if node.secondary_type=='option':
                
                options = node.get_children_names() 

                default_value = node.default_value

                if self.node.name in self.widget_dicts[self.topic]:

                    self.widget = self.widget_dicts[self.topic][self.node.name]

                else:
                    
                    self.widget = ParamChoiceWidget(self.node.name, options, default_value, optional=is_optional_param)
                    
                    self.widget_dicts[self.topic][self.node.name] = self.widget.widget
                   
            elif node.secondary_type=='string':

                if self.node.name in self.widget_dicts[self.topic]:

                    widget = self.widget_dicts[self.topic][self.node.name]

                    self.widget = ParamTextWidget(self.node.name, optional=is_optional_param, widget=widget)

                else:
                
                    self.widget = ParamTextWidget(self.node.name, optional=is_optional_param)
                    
                    self.widget_dicts[self.topic][self.node.name] = self.widget.widget
                   
            elif node.secondary_type=='string_sample':

                if self.node.name in self.widget_dicts[self.topic]:

                    self.widget = self.widget_dicts[self.topic][self.node.name]

                else:
                
                    string_sample_node = node.children[0]
                    string_sample = string_sample_node.name
                    
                    self.widget = ParamTextWidget(self.node.name, string_sample)
                    
                    self.widget_dicts[self.topic][self.node.name] = self.widget.widget
                
        elif node.primary_type=='custom1':
            
            self.widget = Custom1()
            
            self.widget_dicts[self.topic][self.node.name] = 'custom1'

        elif node.primary_type=='param_setter':

            topic, node_name = node.name.split('/')

            widget = self.widget_dicts[topic][node_name]

            self.widget = ParamSetterWidget(self.node.name, widget, self.node.default_value)
        
        self.dynamic_widget_holder = VBox()
        
        children = [
            self.widget, 
            self.dynamic_widget_holder
        ]
        
        self.widget.children[1].observe(self._add_widgets, names=['value'])
        
        super().__init__(children=children)
        
    def _add_widgets(self, widg):
        
        # if node is choiceable param
        # and if any of the choice node has param nodes
        
        # check the choice of current widget
        # and that choice has value1
        
        # look at the choice param value1, and see if that has any children
        # then loop over those children and add them all to the new_widgets
        
        input_value = widg['new']
        
        child_node = self.node.get_child_by_name(input_value)

        new_widgets = []
        
        for child_node in self.node.children:
            
            if child_node.name == input_value and (child_node.secondary_type=='param' or child_node.secondary_type=='param_setter'):
                
                for _child_node in child_node.children:
                
                    widget = DynamicWidget(self.topic, _child_node, self.widget_dicts)
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
        
