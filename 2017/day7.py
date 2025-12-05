import re
from collections import defaultdict


def solve_part_1(input_data):
    """Find root program of tree structure."""
    lines = input_data.strip().split('\n')
    children = set()
    all_programs = set()

    for line in lines:
        parts = line.split(' -> ')
        program = parts[0].split()[0]
        all_programs.add(program)

        if len(parts) > 1:
            for child in parts[1].split(', '):
                children.add(child)

    # Root is the one program not in children
    return (all_programs - children).pop()


def solve_part_2(input_data):
    """Find correct weight to balance tree."""
    lines = input_data.strip().split('\n')
    weights = {}
    children = {}

    # Parse input
    for line in lines:
        parts = line.split(' -> ')
        name_weight = parts[0].split()
        name = name_weight[0]
        weight = int(name_weight[1][1:-1])  # Remove parentheses
        weights[name] = weight

        if len(parts) > 1:
            children[name] = parts[1].split(', ')
        else:
            children[name] = []

    def get_total_weight(node):
        total = weights[node]
        for child in children[node]:
            total += get_total_weight(child)
        return total

    def find_unbalanced(node):
        if not children[node]:
            return None

        child_weights = [(child, get_total_weight(child)) for child in children[node]]

        # Check if all children have same total weight
        weights_list = [w for _, w in child_weights]
        if len(set(weights_list)) <= 1:
            return None

        # Find the odd one out
        weight_counts = {}
        for child, weight in child_weights:
            if weight not in weight_counts:
                weight_counts[weight] = []
            weight_counts[weight].append(child)

        # Find which weight appears only once
        for weight, nodes in weight_counts.items():
            if len(nodes) == 1:
                wrong_node = nodes[0]
                # First check if the problem is deeper in the tree
                deeper_problem = find_unbalanced(wrong_node)
                if deeper_problem:
                    return deeper_problem

                # The problem is with this node's weight
                correct_weight = [w for w in weight_counts.keys() if w != weight][0]
                diff = correct_weight - weight
                return weights[wrong_node] + diff

        return None

    # Find root first
    all_programs = set(weights.keys())
    children_set = set()
    for child_list in children.values():
        children_set.update(child_list)
    root = (all_programs - children_set).pop()

    return find_unbalanced(root)
