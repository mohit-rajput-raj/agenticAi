from langgraph.graph import StateGraph ,START ,END
# from IPython.display import display , Image
from typing import TypedDict
class AgentState(TypedDict):
  a:int
  b:int
  c:int
  d:int
  e:int
  f:int
  g:int
  h:int
  i:int
  j:int
  k:int
  result:int
def C(state:AgentState)->AgentState:
  """mul in c"""
  return {'c': state['a'] * state['b']}

def D(state:AgentState)->AgentState:
  """add in d"""
  return {'d': state['c'] + state['a']}

def E(state:AgentState)->AgentState:
  """divide in e"""
  return {'e': state['b'] / state['c']}

def F(state:AgentState)->AgentState:
  """sub in F"""
  return {'f': state['e'] - state['b']}

def G(state:AgentState)->AgentState:
  """sub in G"""
  return {'g': state['a'] - state['d']}

def H(state:AgentState)->AgentState:
  """divide in h"""
  return {'h': state['d'] / state['c']}

def I(state:AgentState)->AgentState:
  """divide in i"""
  return {'i': state['e'] / state['f']}

def J(state:AgentState)->AgentState:
  """add in j"""
  print("j called")
  return {'j': state['g'] + state['h']}

def K(state:AgentState)->AgentState:
  """add in k"""
  return {'k': state['h'] +  state['e'] + state['i']}

def L(state:AgentState)->AgentState:
  """sub in l"""
  return {'result': state['j'] - state['k']}


graph = StateGraph(AgentState)
graph.add_node("C" ,C)
graph.add_node("D" ,D )
graph.add_node("E" ,E )
graph.add_node("F" ,F )
graph.add_node("G" ,G )
graph.add_node("H" ,H )
graph.add_node("I" ,I )
graph.add_node("J" ,J )
graph.add_node("K" ,K )
graph.add_node("L" ,L )
graph.add_edge(START, "C") # C computes 'c', needed by D, E, H

graph.add_edge("C" , "D") # D needs 'c'
graph.add_edge("C" , "E") # E needs 'c'

graph.add_edge("D" , "G") # G needs 'd'
graph.add_edge("D" , "H") # H needs 'd' (and 'c', which D implicitly handles by running after C)

graph.add_edge("E" , "F") # F needs 'e'

graph.add_edge("F" , "I") # I needs 'f'

graph.add_edge("G" , "J") # J needs 'g'

graph.add_edge("H" , "J") # J needs 'h'
graph.add_edge("H" , "K") # K needs 'h'

graph.add_edge("I" , "K") # K needs 'i'

graph.add_edge("J" , "L") # L needs 'j'
graph.add_edge("K" , "L") # L needs 'k'

graph.add_edge("L" , END)
app = graph.compile()

res = app.invoke({
    "a":1,
    "b":2 ,
    "result":0 
    ,
    "c":0,
    "d":0,
    "e":0,
    "f":0,
    "g":0,
    "h":0,
    "i":0,
    "j":0,
    "k":0,
    })

# res = app.invoke(res)
print(res)