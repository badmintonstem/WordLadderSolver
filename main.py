from collections import deque

class Queue():
  #FIFO Queue
  def __init__(self, parent = None):
    self.list = []
    self.parent = parent
  def append(self, value):
    self.list.append(value)
  def pop(self):
    return self.list.pop(0)

class Node():
  #Node of a tree
  def __init__(self, value, parent=None):
    self.value = value
    self.parent = parent

# --------- Distance Functions
def hamming(s1,s2):
  return sum(ch1 != ch2 for ch1, ch2 in zip(s1,s2))

def levenshtein(s1,s2):
  if len(s1) < len(s2):
    return levenshtein(s2,s1)
  if len(s2) == 0:
    return len(s1)
  previous_row = range(len(s2)+1)
  for i, c1 in enumerate(s1):
    current_row = [i+1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1
      deletions = current_row[j] + 1
      substitutions = previous_row[j] + (c1 != c2)
      current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row
  return previous_row[-1]

# ---------------IO
#print sequence from root to node
def print_words(node):
  values = []
  while isinstance(node, Node):
    values.append(node.value)
    node = node.parent
  print(list(reversed(values)))

def read_file(filename='./words'):
  with open(filename) as f:
    return set(map(str.lower, map(str.strip, f)))

# Get all input
all_words = read_file()
input_words = input("Enter list of words, seperated by spaces: ").split()
input_mode = int(input("Enter 1 for swap-only mode, or 2 for swap-add-rem mode: "))

# Validate user input
if not 1 <= input_mode <= 2:
  raise ValueError("Invalid mode: ", input_mode)

for word in input_words:
  if word not in all_words:
      raise ValueError("Invalid word: " + word)

# Adapt to mode
distance = [hamming, levenshtein][input_mode - 1]
if input_mode == 1:
    all_words = [word for word in all_words if len(word) == len(input_words[0])]

# --------------BFS
def fill(node, to_check, checked):
  checked.add(node.value)
  for word in all_words:
    if 1 >= len(word) - len(node.value) >= -1 and distance(word, node.value) == 1:
      to_check.append(Node(word, node))

for i in range(len(input_words) - 1):
  root = Node(input_words[i])
  checked = set()
  to_check = deque([root])

  fill(root, to_check, checked)
  while to_check:
    node = to_check.pop()
    if node.value == input_words[i + 1]:
      print_words(node)
      break
    if node.value not in checked:
      fill(node, to_check, checked)