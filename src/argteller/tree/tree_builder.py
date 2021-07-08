from collections import defaultdict

from .tree_node import TreeNode

def construct_tree(parsed_node_data):

    parent_nodes = {}

    node_dicts = defaultdict(dict)

    root = TreeNode(-2, 'root', None, 'root')
    parent_nodes[-2] = root

    for node_data in parsed_node_data:

        node_name, primary_type, secondary_type, depth, default_value = node_data

        if primary_type=='topic':
            depth = -1
            current_topic = node_name  # Topic has to be on the top of the dsl

        node = TreeNode(depth, node_name, default_value, primary_type, secondary_type)
        parent_nodes[depth] = node

        if not primary_type=='topic':

            node_dicts[current_topic][node_name] = node

        parent_nodes[depth-1].add_child(node)

    return root, node_dicts


def display_tree(root):
        
    _display_tree(root)
    
def _display_tree(node):

    depth = node.depth
    node_type = node.primary_type
    node_name = node.name

    if node_type != 'root':

        if node_type == 'topic':
            print()

            depth += 1

        print('    '*depth, node_name, ':', node.primary_type, node.secondary_type, node.default_value)

    for child in node.children:

        _display_tree(child)

        