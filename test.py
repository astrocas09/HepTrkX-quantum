import sys,os,time
sys.path.append(os.path.abspath(os.path.join('.')))
import numpy as np
from sklearn import metrics
from tools import *
import tensorflow as tf
def test_validation(config,network):
	t_start = time.time()
	
	
	n_testing = config['n_valid']
	print('Starting testing the validation set with ' + str(n_testing) + ' subgraphs!')

	data = get_dataset(config['valid_dir'], n_testing)

	# Obtain predictions and labels
	preds   = []
	labels  = []
	for n_test in range(n_testing):
		graph_array, labels_ = preprocess(data[n_test])
		labels = np.append(labels,labels_)
		preds  = np.append(preds,network(graph_array))
	
	# Calculate weighted loss
	n_edges      = len(labels)
	n_class      = [n_edges - sum(labels), sum(labels)]
	class_weight = [n_edges/(n_class[0]*2), n_edges/(n_class[1]*2)]	
	loss         = tf.reduce_mean(tf.keras.losses.binary_crossentropy(labels,preds) * np.array([class_weight[int(labels[i])] for i in range(n_edges)]))
	
	# Log all predictons (takes some considerable time - use only for debugging)
	if config['log_verbosity']>=3:	
		with open(config['log_dir']+'log_validation_preds.csv', 'a') as f:
			for i in range(len(preds)):
				f.write('%.4f, %.4f\n' %(preds[i],labels[i]))
	
	# Calculate Metrics
	fpr,tpr,thresholds = metrics.roc_curve(labels.astype(int),preds,pos_label=1 )
	auc                = metrics.auc(fpr,tpr)		
	accuracy           = ((1-fpr[len(fpr)//2])*n_class[0]+tpr[len(tpr)//2]*n_class[1])/n_edges	
	precision          = metrics.average_precision_score(labels.astype(int),preds)
	tn, fp, fn, tp     = metrics.confusion_matrix(labels.astype(int),(preds > 0.5)*1).ravel() # get the confusion matrix for 0.5 threshold

	# Log Metrics
	with open(config['log_dir']+'log_validation.csv', 'a') as f:
		f.write('%.4f, %.4f, %.4f, %.4f, %d, %d, %d, %d\n' %(accuracy, auc, loss, precision,tn, fp, fn, tp))
	
	duration = time.time() - t_start

	# Print summary
	print(str(datetime.datetime.now()) + ': Validation Test:  Loss: %.4f,  Acc: %.4f, AUC: %.4f, Precision: %.4f -- Elapsed: %dm%ds' %(loss, accuracy*100, auc, precision, duration/60, duration%60))
	
def test_train(config,network):
	t_start = time.time()
	
	n_testing = config['n_train']
	print('Starting testing the training set with ' + str(n_testing) + ' subgraphs!')

	data = get_dataset(config['train_dir'], n_testing)

	preds   = []
	labels  = []

	for n_test in range(n_testing):
		graph_array, labels_ = preprocess(data[n_test])
		labels = np.append(labels,labels_)
		preds  = np.append(preds,network(graph_array))
	
	# Calculate weighted loss
	n_edges      = len(labels)
	n_class      = [n_edges - sum(labels), sum(labels)]
	class_weight = [n_edges/(n_class[0]*2), n_edges/(n_class[1]*2)]	
	loss         = tf.reduce_mean(tf.keras.losses.binary_crossentropy(labels,preds) * np.array([class_weight[int(labels[i])] for i in range(n_edges)]))
	
	# Log all predictons (takes some considerable time - use only for debugging)
	'''
	with open(config['log_dir']+'log_training_preds.csv', 'a') as f:
		for i in range(len(preds)):
			f.write('%.4f, %.4f\n' %(preds[i],labels[i]))
	'''

	# Calculate Metrics
	fpr,tpr,thresholds = metrics.roc_curve(labels.astype(int),preds,pos_label=1 )
	auc = metrics.auc(fpr,tpr)	
	accuracy = ((1-fpr[len(fpr)//2])*n_class[0]+tpr[len(tpr)//2]*n_class[1])/n_edges			
	
	# Log Metrics
	with open(config['log_dir']+'log_training.csv', 'a') as f:
			f.write('%.4f, %.4f, %.4f\n' %(accuracy,auc,loss))

	duration = time.time() - t_start

	# Print summary
	print(str(datetime.datetime.now()) + ': Training Loss: %.4f, Training Acc: %.4f, Training AUC: %.4f Elapsed: %dm%ds' %(loss, accuracy*100, auc, duration/60, duration%60))

