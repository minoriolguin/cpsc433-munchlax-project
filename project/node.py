from scheduler import Scheduler

class Node:
    def __init__(self, schedule=None, sol="?"):
        if schedule is None:
            schedule = Scheduler() 
        self.schedule = schedule
        self.sol = sol
        self.children = []
    
    def add_child(self, child_node):
        self.children.append(child_node)
