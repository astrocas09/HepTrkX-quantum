# Calculates gradients of a pennylane quantum circuit using tensorflow
import sys, os, time, datetime, csv, yaml, argparse
sys.path.append(os.path.abspath(os.path.join('.')))
# import scripts
from datasets.hitgraphs import get_datasets
from tools.tools import *
from qnetworks.GNN2 import GNN
from test import *
# import external
import tensorflow as tf
import numpy as np
from random import shuffle
############################################################################################
def gradient(edge_array,label):
	# Calculate weights for labels
	n_edges      = len(labels)
	n_class      = [n_edges - sum(labels), sum(labels)]
	class_weight = [n_edges/(n_class[0]*2), n_edges/(n_class[1]*2)]	

	# Calculate weighted loss and gradients
	with tf.GradientTape() as tape:
		loss = tf.reduce_mean(tf.keras.losses.binary_crossentropy(label,block(edge_array)) * np.array([class_weight[int(labels[i])] for i in range(n_edges)]))
		return loss, tape.gradient(loss,block.trainable_variables)
############################################################################################
if __name__ == '__main__':
	# Tensorflow settings
	tf.keras.backend.set_floatx('float64')
	#tf.config.threading.set_inter_op_parallelism_threads(4)
	
	# Read config file
	args = parse_args()
	config = load_config(args)

	# Set CPU or GPU
	os.environ["CUDA_VISIBLE_DEVICES"] = config['gpu']
	
	# Delete old logs
	delete_all_logs(config['log_dir'])
	 	
	# Load data
	train_data, _ = get_datasets(config['train_dir'], config['n_train'], 0)
	train_list  = [i for i in range(config['n_train'])]
	_, valid_data = get_datasets(config['valid_dir'], 0, config['n_valid'])

	# Setup the network
	block = GNN(config['hid_dim'],config['n_iters'])
	opt = tf.keras.optimizers.Adam(learning_rate=config['lr'])

	# Log Learning variables
	log_tensor_array(block.trainable_variables[0],config['log_dir'], 'log_params_IN.csv') 
	log_tensor_array(block.trainable_variables[1],config['log_dir'], 'log_params_EN.csv') 
	log_tensor_array(block.trainable_variables[2],config['log_dir'], 'log_params_NN.csv') 

	# Test the validation set
	test_validation(config,block,valid_data)
	
	##################### BEGIN TRAINING #####################  
	print(str(datetime.datetime.now()) + ': Training is starting!')
	for epoch in range(config['n_epoch']): 
		shuffle(train_list) # shuffle the order every epoch
		for n_step in range(config['n_train']):
			t0 = time.time()

			# Update Learning Variables
			graph_array, labels = preprocess(train_data[train_list[n_step]])
			loss, grads = gradient(graph_array,labels)
			opt.apply_gradients(zip(grads, block.trainable_variables))
			
			t = time.time() - t0

			# Print summary
			print(str(datetime.datetime.now()) + ": Epoch: %d, Batch: %d, Loss: %.4f, Elapsed: %dm%ds" % (epoch+1, n_step+1, loss ,t / 60, t % 60) )

			# Start Logging

			# Log summary 
			with open(config['log_dir']+'summary.csv', 'a') as f:
				f.write('Epoch: %d, Batch: %d, Loss: %.4f, Elapsed: %dm%ds\n' % (epoch+1, n_step+1, loss, t / 60, t % 60) )
			
			# Log loss
			with open(config['log_dir'] + 'log_loss.csv', 'a') as f:
				f.write('%.4f\n' %loss)	
				
			# Log gradients
			log_tensor_array(grads,config['log_dir'], 'log_grads.csv')

			# Log Learning variables
			log_tensor_array(block.trainable_variables,config['log_dir'], 'log_params.csv') 
			
			# Test every TEST_every
			if (n_step+1)%config['TEST_every']==0:
					test_validation(config,block,valid_data)
					#test(train_data,config['n_train'],testing='train')

		# Test the validation set after every epoch
		test_validation(config,block,valid_data)

	print(str(datetime.datetime.now()) + ': Training completed!')
	##################### END TRAINING ##################### 


	





