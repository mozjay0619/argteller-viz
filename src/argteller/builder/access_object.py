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


class AccessObject():
    
    def __init__(self, root, node_dicts):


        self.module_found = module_found

        if not self.module_found:
            return
        
        self.root, self.node_dicts = root, node_dicts
        self.widget_dicts = defaultdict(dict)
        self.param_vboxes = {}

        for topic in self.root.children:

            param_widgets = []

            for param in topic.children:

                param_widget = DynamicWidget(topic.name, param, self.widget_dicts)

                param_widgets.append(param_widget)

            param_vbox = VBox(param_widgets)

            self.param_vboxes[topic.name] = param_vbox

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

            
    def get_vbox(self, topic):
        
        return self.param_vboxes[topic]
    
    def get_widget(self, param, topic=None):
        
        if topic:
            
            return self.widget_dicts[topic][param]
        
        else:
            
            params = []
            topics = []
            
            for topic, param_dict in self.widget_dicts.items():
            
                if param in param_dict:
                    
                    params.append(param_dict[param])
                    topics.append(topic)
                    
            if len(params) > 1:
                
                raise TypeError('Specify the topic!', topics)
                
            return params[0]
        
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
                    
                    
            return nodes[0]

