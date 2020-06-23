import pennylane as qml 
from pennylane import numpy as np
import tensorflow as tf
from tools.tools import get_params
import pennylane_qulacs
import os
##################################################################################################
# Use default.qubit for default pennylane simulation
# use tf.interface for TF integration
dev1 = qml.device("qulacs.simulator", wires=16, gpu=True)
@qml.qnode(dev1,interface='tf')
def TTN_edge_forward(edge,theta_learn):
	# STATE PREPARATION
	for i in range(16):
		qml.RY(edge[i],wires=i)
	# APPLY forward sequence
	# First Layer
	qml.RY(theta_learn[0],wires=0)
	qml.RY(theta_learn[1],wires=1)
	qml.CNOT(wires=[0,1])
	qml.RY(theta_learn[2],wires=2)
	qml.RY(theta_learn[3],wires=3)
	qml.CNOT(wires=[3,2])

	qml.RY(theta_learn[4],wires=4)
	qml.RY(theta_learn[5],wires=5)
	qml.CNOT(wires=[4,5])
	qml.RY(theta_learn[6],wires=6)
	qml.RY(theta_learn[7],wires=7)
	qml.CNOT(wires=[7,6])

	qml.RY(theta_learn[8],wires=8)
	qml.RY(theta_learn[9],wires=9)
	qml.CNOT(wires=[8,9])
	qml.RY(theta_learn[10],wires=10)
	qml.RY(theta_learn[11],wires=11)
	qml.CNOT(wires=[11,10])

	qml.RY(theta_learn[12],wires=12)
	qml.RY(theta_learn[13],wires=13)
	qml.CNOT(wires=[12,13])
	qml.RY(theta_learn[14],wires=14)
	qml.RY(theta_learn[15],wires=15)
	qml.CNOT(wires=[15,14])


	# Second Layer
	qml.RY(theta_learn[16],wires=1)
	qml.RY(theta_learn[17],wires=2)
	qml.CNOT(wires=[1,2])

	qml.RY(theta_learn[18],wires=5)
	qml.RY(theta_learn[19],wires=6)
	qml.CNOT(wires=[6,5])

	qml.RY(theta_learn[20],wires=9)
	qml.RY(theta_learn[21],wires=10)
	qml.CNOT(wires=[9,10])

	qml.RY(theta_learn[22],wires=13)
	qml.RY(theta_learn[23],wires=14)
	qml.CNOT(wires=[14,13])

	# Third Layer
	qml.RY(theta_learn[24],wires=2)
	qml.RY(theta_learn[25],wires=5)
	qml.CNOT(wires=[2,5])
	qml.RY(theta_learn[26],wires=10)
	qml.RY(theta_learn[27],wires=13)
	qml.CNOT(wires=[13,10])
	# Forth Layer
	qml.RY(theta_learn[28],wires=5)
	qml.RY(theta_learn[29],wires=10)
	qml.CNOT(wires=[5,10])
	#Last Layer
	qml.RY(theta_learn[30],wires=10)		
	return qml.expval(qml.PauliZ(wires=10))
##################################################################################################
# Use default.qubit for default pennylane simulation
# use tf.interface for TF integration
dev2 = qml.device("qulacs.simulator", wires=24,gpu=True)
@qml.qnode(dev2,interface='tf')
def TTN_node_forward(edge,theta_learn):
	# STATE PREPARATION
	for i in range(24):
		qml.RY(edge[i],wires=i)
	# APPLY forward sequence
	# First Layer
	qml.RY(theta_learn[0],wires=0)
	qml.RY(theta_learn[1],wires=1)
	qml.CNOT(wires=[0,1])
	qml.RY(theta_learn[2],wires=2)
	qml.RY(theta_learn[3],wires=3)
	qml.CNOT(wires=[3,2])

	qml.RY(theta_learn[4],wires=4)
	qml.RY(theta_learn[5],wires=5)
	qml.CNOT(wires=[4,5])
	qml.RY(theta_learn[6],wires=6)
	qml.RY(theta_learn[7],wires=7)
	qml.CNOT(wires=[7,6])

	qml.RY(theta_learn[8],wires=8)
	qml.RY(theta_learn[9],wires=9)
	qml.CNOT(wires=[8,9])
	qml.RY(theta_learn[10],wires=10)
	qml.RY(theta_learn[11],wires=11)
	qml.CNOT(wires=[11,10])

	qml.RY(theta_learn[12],wires=12)
	qml.RY(theta_learn[13],wires=13)
	qml.CNOT(wires=[12,13])
	qml.RY(theta_learn[14],wires=14)
	qml.RY(theta_learn[15],wires=15)
	qml.CNOT(wires=[15,14])

	qml.RY(theta_learn[16],wires=16)
	qml.RY(theta_learn[17],wires=17)
	qml.CNOT(wires=[16,17])
	qml.RY(theta_learn[18],wires=18)
	qml.RY(theta_learn[19],wires=19)
	qml.CNOT(wires=[19,18])

	qml.RY(theta_learn[20],wires=20)
	qml.RY(theta_learn[21],wires=21)
	qml.CNOT(wires=[20,21])
	qml.RY(theta_learn[22],wires=22)
	qml.RY(theta_learn[23],wires=23)
	qml.CNOT(wires=[23,22])

	# Second Layer
	qml.RY(theta_learn[24],wires=1)
	qml.RY(theta_learn[25],wires=2)
	qml.CNOT(wires=[1,2])
	qml.RY(theta_learn[26],wires=5)
	qml.RY(theta_learn[27],wires=6)
	qml.CNOT(wires=[6,5])

	qml.RY(theta_learn[28],wires=9)
	qml.RY(theta_learn[29],wires=10)
	qml.CNOT(wires=[9,10])
	qml.RY(theta_learn[30],wires=13)
	qml.RY(theta_learn[31],wires=14)
	qml.CNOT(wires=[14,13])

	qml.RY(theta_learn[32],wires=17)
	qml.RY(theta_learn[33],wires=18)
	qml.CNOT(wires=[17,18])
	qml.RY(theta_learn[34],wires=21)
	qml.RY(theta_learn[35],wires=22)
	qml.CNOT(wires=[22,21])

	# Third Layer

	qml.RY(theta_learn[36],wires=2)
	qml.RY(theta_learn[37],wires=5)
	qml.CNOT(wires=[2,5])

	qml.RY(theta_learn[38],wires=10)
	qml.RY(theta_learn[39],wires=13)
	qml.CNOT(wires=[13,10])

	qml.RY(theta_learn[40],wires=18)
	qml.RY(theta_learn[41],wires=21)
	qml.CNOT(wires=[21,18])

	# Fourth Layer

	qml.RY(theta_learn[42],wires=5)
	qml.RY(theta_learn[43],wires=10)
	qml.CNOT(wires=[5,10])

	# Fifth Layer

	qml.RY(theta_learn[44],wires=10)
	qml.RY(theta_learn[45],wires=18)
	qml.CNOT(wires=[10,18])

	# 6th Layer

	qml.RY(theta_learn[46],wires=5)
	qml.RY(theta_learn[47],wires=10)
	qml.CNOT(wires=[10,5])

	qml.RY(theta_learn[48],wires=18)
	qml.RY(theta_learn[49],wires=21)
	qml.CNOT(wires=[18,21])

	# 7th Layer

	qml.RY(theta_learn[50],wires=2)
	qml.RY(theta_learn[51],wires=5)
	qml.CNOT(wires=[5,2])

	# Last Layer
	qml.RY(theta_learn[52],wires=2)		
	qml.RY(theta_learn[53],wires=5)
	qml.RY(theta_learn[54],wires=10)		
	qml.RY(theta_learn[55],wires=18)	
	qml.RY(theta_learn[56],wires=21)		

	return qml.expval(qml.PauliZ(wires=2)), qml.expval(qml.PauliZ(wires=5)), qml.expval(qml.PauliZ(wires=10)), qml.expval(qml.PauliZ(wires=18)), qml.expval(qml.PauliZ(wires=21))
#################################################
def edge_forward(edge_array,theta_learn):
	# executes TTN_edge circuit for each edge in edge_array
	# To Do: can parallize the for loop
	outputs = []
	for i in range(len(edge_array[:,0])):
		out = tf.constant((1-TTN_edge_forward(edge_array[i,:],theta_learn))/2.,dtype=tf.float64)
		outputs.append(out)
	return tf.stack(outputs)
#################################################
def node_forward(node_array,theta_learn):
	# executes TTN_node circuit for each node in node_array
	# To Do: can parallize the for loop
	outputs = []
	for i in range(len(node_array[:,0])):
		out = tf.constant(2*np.pi*(1-TTN_node_forward(node_array[i,:],theta_learn))/2.,dtype=tf.float64)
		outputs.append(out)
	return tf.stack(outputs) # output is between [0,4*pi]
#################################################
class EdgeNet(tf.keras.layers.Layer):
	def __init__(self,config,name='EdgeNet'):
		super(EdgeNet, self).__init__(name=name)
		# can only work with hid_dim = 2
		# read parameters of the network from file
		# params are created using tools/init_params.py
		#self.theta_learn = tf.Variable(get_params('EN',config)[0])
		self.theta_learn =  tf.Variable(tf.random.uniform(shape=[31,],minval=0,maxval=np.pi*2,dtype=tf.float64))
	def call(self,X, Ri, Ro):
		bo = tf.matmul(Ro,X,transpose_a=True)
		bi = tf.matmul(Ri,X,transpose_a=True)
		# Shape of B = N_edges x 6 (2x (3 coordinates))
		# each row consists of two node that are possibly connected.
		B  = tf.concat([bo, bi], axis=1)  
		return edge_forward(B,self.theta_learn)
#################################################
class NodeNet(tf.keras.layers.Layer):
	def __init__(self,config,name='NodeNet'):
		super(NodeNet, self).__init__(name=name)
		# can only work with hid_dim = 1
		# read parameters of the network from file
		# params are created using tools/init_params.py
		#self.theta_learn = tf.Variable(get_params('NN',config)[0])
		self.theta_learn =  tf.Variable(tf.random.uniform(shape=[57,],minval=0,maxval=np.pi*2,dtype=tf.float64))
	def call(self, X, e, Ri, Ro):
		bo  = tf.matmul(Ro, X, transpose_a=True) 
		bi  = tf.matmul(Ri, X, transpose_a=True) 
		Rwo = tf.math.multiply(Ro,e)
		Rwi = tf.math.multiply(Ri,e)
		mi = tf.matmul(Rwi, bo)
		mo = tf.matmul(Rwo, bi)
		M = tf.concat([mi, mo, X], axis=1)
		return node_forward(M,self.theta_learn)
#################################################
class InputNet(tf.keras.layers.Layer):
	def __init__(self, config, name):
		super(InputNet, self).__init__(name=name)
		self.num_outputs = config['hid_dim'] # num_outputs = number of hidden dimensions
		# read parameters of the network from file
		# params are created using tools/init_params.py
		#init = tf.constant_initializer(get_params('IN',config)[0])
		# setup a Dense layer with the given config
		self.layer = tf.keras.layers.Dense(self.num_outputs,input_shape=(3,),activation='sigmoid')
	def call(self, arr):
		return self.layer(arr)*2*np.pi # to map to output to [0,2*pi]
#################################################
class GNN(tf.keras.Model):
	def __init__(self, config):
		super(GNN, self).__init__(name='GNN')

		self.InputNet = InputNet(config,name='InputNet')
		self.EdgeNet  = EdgeNet(config,name='EdgeNet')
		self.NodeNet  = NodeNet(config,name='NodeNet')
		self.n_iters = config['n_iters']

	def call(self, edge_array):
		X,Ri,Ro = edge_array
		H = self.InputNet(X) 
		H = tf.concat([H,X],axis=1)
		for i in range(self.n_iters):
			e = self.EdgeNet(H, Ri, Ro)
			H = self.NodeNet(H, e, Ri, Ro)
			H = tf.concat([H,X], axis=1)
		e = self.EdgeNet(H, Ri, Ro)
		return e
#################################################
