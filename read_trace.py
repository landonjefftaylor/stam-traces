import os
import sys

class State:
  def __init__(self,id):
    self.id = id
    self.children = []
    self.transitions = []
    # print("init state " + str(self.id))
  
  def __str__(self):
    return str(self.id) + " with children " + str(self.children) + " with transitions " + str(self.transitions)
  
  def __repr__(self):
    return str(self.id)
  
  def add_kid(self,newState,transition):
    self.children.append(newState)
    self.transitions.append(transition)
    if not(len(self.children) == len(self.transitions)):
      print("ERROR 1: CHILDREN AND TRANSITIONS OF DIFFERENT LENGTHS")
      exit()
    # print("Added kid from " + str(self.id) + " to " + str(self.children[len(self.children) - 1].id) + " via " + str(self.transitions[len(self.transitions) - 1]))
  
  def path_exists(self,path):
    if len(path) == 0:
      print("PATH FOUND SUCCESSFULLY!")
      return True
    # print("self.transitions = " + str(len(self.transitions)))
    if path[0] in self.transitions:
      # print("::: " + str(path) + " :::")
      # print("\t\t(FOUND)")
      if len(path) == 1:
        new_path = []
      else:
        new_path = path[:1]
      # print(";;; " + str(new_path) + " ;;;")
      return self.children[self.transitions.index(path[0])].path_exists(new_path)
    return False

  # def check_duplicates(self,looking_for,index):
  #   # print("called check duplicates")
  #   if index > 2:
  #     return
  #   for child in self.children:
  #     if child.id == looking_for:
  #       print("LOOP FOUND! Child id: " + str(child.id) + " Looking for: " + str(looking_for) + " at index " + str(index))
  #       return
  #     child.check_duplicates(looking_for, index + 1)
  
  # def find_initial_states(self, incoming):
  #   for child in self.children:
  #     incoming[child.id] = True


sys.setrecursionlimit(1000)
# print(sys.getrecursionlimit())

if len(sys.argv) == 3:
  filename = str(sys.argv[1])
  conefilename = str(sys.argv[2])
elif len(sys.argv) == 2:
  filename = str(sys.argv[1])
  conefilename = str(input("Cone file? "))
else:
  filename = str(input("What stamina output file? "))
  conefilename = str(input("Cone file? "))

state_list = []
working_index = -1

with open(filename,'r') as stam:
  for line in stam:
    words = line.split()
    state_id = int(words[0])
    if state_id > working_index:
      new_state = State(state_id)
      state_list.append(new_state)
      # print("made state " + str(new_state))
      working_index = state_id
  print("made " + str(len(state_list)) + " states.")

with open(filename,'r') as stam:
  for line in stam:
    if not("[" in line):
      break
    words = line.split()
    from_state = int(words[0])
    to_state = int(words[1])
    transition = str(words[3])
    if "__" in transition:
      transition = transition.split("__")[1]
    transition = transition.replace("]",'').replace("[",'').lower()
    # print(transition)
    state_list[from_state].add_kid(state_list[to_state],transition)

with open(filename + "_states.txt", 'w') as result:
  for state in state_list:
    result.write(str(state) + "\n")

print("Now checking paths")
good_path_count = 0
bad_path_count = 0

with open(filename + "_" + conefilename + "_final_result.txt", 'w') as result:
  result.write("Below are the traces that IVy found that STAMINA did not find:\n\n")
  with open(conefilename, 'r') as conefile:
    for line in conefile:
      # print("evaluating " + line.rstrip("\n"))
      path_ok = False
      for state in state_list:
        if state.path_exists(line.rstrip("\n").split()):
          path_ok = True
          # print("+++ good trace: " + line.rstrip("\n"))
          good_path_count = good_path_count + 1
          break
      if not(path_ok):
        result.write(line.rstrip("\n") + "\n")
        bad_path_count = bad_path_count + 1
        # print("--- --- bad trace: " + line.rstrip("\n"))
      # print(str(state_list[0].path_exists(line.rstrip("\n").split())))

with open(filename + "_facts.txt","w") as wf:
  wf.write("All done. " + str(good_path_count) + " paths matched, with " + str(bad_path_count) + " mismatched.")
  print("All done. " + str(good_path_count) + " paths matched, with " + str(bad_path_count) + " mismatched.")
  wf.write("\n")
  wf.write(str((float(bad_path_count)*100.0)/float(good_path_count)) + "% mismatched paths ")
  print(str((float(bad_path_count)*100.0)/float(good_path_count)) + "% mismatched paths ")



# state_list[1].check_duplicates(1,0)
# for state in state_list:
#   state.check_duplicates(state.id,0)
# incoming = [False]*len(state_list)
# for state in state_list:
#   state.find_initial_states(incoming)
# with open(filename + "_incoming.txt", 'w') as result:
#   result.write(str(incoming))
# state_list[0].print_all_paths("result.txt","")
