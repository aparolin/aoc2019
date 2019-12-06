from queue import Queue

class Node:
  def __init__(self, name):
    self.name = name
    self.parent = None
    self.children = []
    self.level = 0

def get_node(name, nodes_map):
  if name in nodes_map:
    return nodes_map[name]
  else:
    n = Node(name)
    nodes_map[name] = n
    return n

def run_part1(orbits):
  nodes_map = {}
  root = None

  # create orbits tree
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

  # bfs to find direct and indirect orbits
  nodes = Queue()
  nodes.put(root)

  total_orbits = 0
  while nodes.qsize() > 0:
    node = nodes.get()
    for c in node.children:
      c.level = node.level + 1
      nodes.put(c)
      total_orbits += c.level

  return total_orbits

if __name__ == '__main__':
  orbits = [line.rstrip('\n') for line in open('input.txt')]

  print(run_part1(orbits))