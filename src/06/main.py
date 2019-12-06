from queue import Queue

class Node:
  def __init__(self, name):
    self.name = name
    self.parent = None
    self.children = []
    self.level = 0
    self.distance_from_you = 0

def get_node(name, nodes_map):
  if name in nodes_map:
    return nodes_map[name]
  else:
    n = Node(name)
    nodes_map[name] = n
    return n

def execute(orbits):
  # create orbits tree
  nodes_map = {}
  for o in orbits:
    [name1, name2] = o.split(')')

    node1 = get_node(name1, nodes_map)
    node2 = get_node(name2, nodes_map)

    node2.parent = node1
    node1.children.append(node2)

  # take any node to find the root
  root = None
  while node1.parent is not None:
    root = node1.parent
    node1 = root

  # BFS to find direct and indirect orbits
  nodes = Queue()
  nodes.put(root)

  total_orbits = 0
  while nodes.qsize() > 0:
    node = nodes.get()
    for c in node.children:
      c.level = node.level + 1
      nodes.put(c)
      total_orbits += c.level

  print(f'Part 1: {total_orbits}')

  # DFS to find shortest path between nodes
  visited = set()
  node = nodes_map['YOU']
  stack = [node]
  while len(stack) > 0:
    node = stack.pop()
    if node in visited:
      continue
    else:
      visited.add(node)

    if node.name == 'SAN':
      # -2 to disregard YOU and SAN nodes themselves
      print(f'Part 2: {node.distance_from_you-2}')
      break

    for c in node.children:
      stack.append(c)
      c.distance_from_you = node.distance_from_you + 1

    # ensure backtracking
    if node.parent is not None:
      node.parent.distance_from_you = node.distance_from_you + 1
      stack.append(node.parent)

if __name__ == '__main__':
  orbits = [line.rstrip('\n') for line in open('input.txt')]

  execute(orbits)
