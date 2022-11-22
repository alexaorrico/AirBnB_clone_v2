#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))

def main():
    cities, roads, capital = inlt()
    
    edges = defaultdict(list)
  
    for _ in range(roads):
        u,v = inlt()
        edges[u].append(v)
    def dfs(node,visited):
        if node in visited:
            return
        visited.add(node)
        for i in edges[node]:
            dfs(i,visited)
    visited = set()
    dfs(capital,visited)
    disconnected = 0
    for i in range(1,cities+1):
        if i not in visited:
            dfs(i,visited)
            disconnected += 1
    print(disconnected)