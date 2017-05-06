import numpy as np
import pandas as pd
import pydot 
from scipy.sparse import csr_matrix
engine='python'
np.set_printoptions(threshold = np.nan)


patient_CBC_with1 = pd.DataFrame(pd.read_csv('data/PC.txt', names = ['patient' , 'CBC', '1'], engine='python',sep="   "))
patient_CBC = patient_CBC_with1.drop(['1'], axis=1)

patient_metabolism_with1 = pd.DataFrame(pd.read_csv('data/PM.txt', names = ['patient' , 'metabolism', '1'], engine='python',sep="   "))
patient_metabolism = patient_metabolism_with1.drop(['1'], axis=1)

patient_ur_with1 = pd.DataFrame(pd.read_csv('data/PU.txt', names = ['patient' , 'ur', '1'],engine='python', sep="   "))
patient_ur = patient_ur_with1.drop(['1'], axis=1)

p,u,c= patient_ur['patient'],patient_ur['ur'],patient_CBC['CBC']


graph=pydot.Dot(graph_type='digraph',pad="0.5", nodesep="1", ranksep="1")
patient_node=[]
ur_node=[]
c_node=[]

for i in range (10):
	patient_node.append(pydot.Node("P"+str(i+1),shape="circle",style="filled",fillcolor="red"))
 	graph.add_node(patient_node[i])

for j in range (5):
	ur_node.append(pydot.Node("U"+str(j+1),shape="circle",style="filled",fillcolor="green"))
 	graph.add_node(ur_node[j]) 	

for x in range (20):
	c_node.append(pydot.Node("C"+str(x+1),shape="circle",style="filled",fillcolor="blue"))
 	graph.add_node(c_node[x]) 	

k=0
while (p[k]<11):
	m=p[k]-1
	n=u[k]-1
	l=c[k]-1
	graph.add_edge(pydot.Edge(patient_node[m],ur_node[n]))
	graph.add_edge(pydot.Edge(patient_node[m],c_node[l],style="dotted"))

	k+=1


graph.write_png('heteroHER.png') 	
