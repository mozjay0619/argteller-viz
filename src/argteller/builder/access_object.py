from ..tree.tree_node import TreeNode
from ..widgets.dynamic_widgets import DynamicWidget
from ..widgets.dynamic_widgets import DynamicSwitch

try:

    from IPython.display import display
    import ipywidgets as widgets
    from ipywidgets import HBox, Label, VBox
    from ipywidgets import Button, Layout, HTML

    module_found = True

except ModuleNotFoundError:

    module_found = False

from collections import defaultdict
from threading import Event


class AccessObject():
    """Creates the DynamicWidgets based on the input tree.
    """
    
    def __init__(self, root, node_dicts):

        initial_event = Event()
        param_setter_event = Event()

        self.module_found = module_found

        if not self.module_found:
            return
        
        self.root, self.node_dicts = root, node_dicts
        self.widget_dicts = defaultdict(dict)
        self.param_vboxes = {}

        for topic in self.root.children:

            param_widgets = []

            for param in topic.children:

                param_widget = DynamicWidget(topic.name, param, self.widget_dicts, initial_event, param_setter_event)

                param_widgets.append(param_widget)

            param_vbox = VBox(param_widgets)



            self.param_vboxes[topic.name] = param_vbox

        initial_event.set()

    def get_topics(self):
    
        return self.root.get_children_names()

    def get_params(self, topic=None):

        if topic:
    
            return list(self.widget_dicts[topic].keys())

        else:

            l = []
            self._find_params(self.root, l)

            return l

    def _find_params(self, node, l):

        depth = node.depth
        node_type = node.primary_type
        node_name = node.name

        if node_type != 'root':

            if node_type == 'topic':

                depth += 1
                
            if node_type in ['param', 'optional']:
                
                if node_name not in l:
                    l.append(node_name)

        for child in node.children:

            self._find_params(child, l)

    def get_value(self, param, topic=None):
        
        return self.get_widget(param, topic).value

    def set_value(self, value, param, topic=None):

        self.get_widget(param, topic).value = value

            
    def get_vbox(self, topic):
        
        return self.param_vboxes[topic]
    
    def get_widget(self, param, topic=None):
        
        if topic:
            
            try:
                return self.widget_dicts[topic][param].children[-1]

            except:

                print(param, topic, '=====')
                print(self.widget_dicts, '+++++')
        
        else:
            
            params = []
            topics = []
            
            for topic, param_dict in self.widget_dicts.items():
            
                if param in param_dict:
                    
                    params.append(param_dict[param])
                    topics.append(topic)
                    
            if len(params) > 1:
                
                raise TypeError('Specify the topic!', topics)

            
                
            return params[0].children[-1]
        
    def get_node(self, node, topic=None):
        
        if topic:
            
            return self.node_dicts[topic][node]
        
        else:
            
            nodes = []
            topics = []
            
            for topic, node_dict in self.node_dicts.items():
                
                if node in node_dict:
                    
                    nodes.append(node_dict[node])
                    topics.append(topic)
                    
            if len(nodes) > 1:
                
                raise TypeError('Specify the topic!', topics)
                    
            if len(nodes)==0:
                return None
                    
            return nodes[0]

    def node_exists(self, node, topic=None):

        node = self.get_node(node, topic)

        if node is None:
            return False
        else:
            return True

    def get_active_param_values(self):
    
        dsl_gen = [""]

        for topic in self.root.children:

            dsl_gen[0] += "{}\n".format(topic.name)

            for param in topic.children:  # genesis params

                self._follow_branch(param, topic, dsl_gen)
                
        return dsl_gen[0][0:-1]

    def _follow_branch(self, param, topic, dsl_gen):
        """Notice the similarity to _add_widgets method in DynamicWidget
        class
        """
        
        widget = self.get_widget(param.name, topic.name)
        input_value = widget.value
        
        dsl_gen[0] += "-{}:{}\n".format(param.name, input_value)
        
        for child_node in param.children:  # Since this is choice param, child_nodes are all options
            
            if child_node.name==input_value:
                
                for _child_node in child_node.children:
                    
                    self._follow_branch(_child_node, topic, dsl_gen)

