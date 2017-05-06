import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
engine='python'
np.set_printoptions(threshold = np.nan)

trainId_patient = pd.DataFrame(pd.read_csv('data/trainId_patient.txt', names = ['patient']))
testId_patient = pd.DataFrame(pd.read_csv('data/testId_patient.txt', names = ['patient']))

trainId_CBC = pd.DataFrame(pd.read_csv('data/trainId_CBC.txt', names = ['CBC']))
testId_CBC = pd.DataFrame(pd.read_csv('data/testId_CBC.txt', names = ['CBC']))

trainId_metabolic = pd.DataFrame(pd.read_csv('data/trainId_metabolic.txt', names = ['metabolic']))
testId_metabolic = pd.DataFrame(pd.read_csv('data/testId_metabolic.txt', names = ['metabolic']))

trainId_ur = pd.DataFrame(pd.read_csv('data/trainId_ur.txt', names = ['urinalysis']))
testId_ur = pd.DataFrame(pd.read_csv('data/testId_ur.txt', names = ['urinalysis']))


patient_label = pd.DataFrame(pd.read_csv('data/patient_label.txt', names = ['patient', 'label'],engine='python', sep = "   "))
CBC_label = pd.DataFrame(pd.read_csv('data/CBC_label.txt', names = ['CBC', 'label'],engine='python', sep = "  "))
metabolic_label = pd.DataFrame(pd.read_csv('data/Metabolic_label.txt', names = ['metabolic', 'label'],engine='python', sep = "   "))
ur_label = pd.DataFrame(pd.read_csv('data/ur_label.txt', names = ['urinalysis', 'label'],engine='python', sep = "  "))

patient_CBC_with1 = pd.DataFrame(pd.read_csv('data/PC.txt', names = ['patient' , 'CBC', '1'], engine='python',sep="   "))
patient_CBC = patient_CBC_with1.drop(['1'], axis=1)

patient_metabolism_with1 = pd.DataFrame(pd.read_csv('data/PM.txt', names = ['patient' , 'metabolism', '1'], engine='python',sep="   "))
patient_metabolism = patient_metabolism_with1.drop(['1'], axis=1)

patient_ur_with1 = pd.DataFrame(pd.read_csv('data/PU.txt', names = ['patient' , 'ur', '1'],engine='python', sep="   "))
patient_ur = patient_ur_with1.drop(['1'], axis=1)

num_patient = patient_label['patient'].max()
print "Total patients: ",num_patient
num_CBC = patient_CBC['CBC'].max()
print "Total CBC tests: ",num_CBC
num_metabolism = patient_metabolism['metabolism'].max()
print "Total metabolism tests: ",num_metabolism
num_ur = patient_ur['ur'].max()
print "Total urinalysis tests: ",num_ur
num_label = patient_label['label'].max()
print "Total labels: ",num_label


def generate_zeros(row, column):
	matrix_zeros = np.zeros(shape = (row, column))
	return matrix_zeros

def get_rij(i, j, relation):
	matrix = generate_zeros(i, j)
	r = pd.DataFrame(matrix)
	for index, x, y in relation.itertuples():
		r.set_value(x-1, y-1, r.ix[x-1, y-1]+1)
	return r

def get_yij(i, j, relation):
	matrix = generate_zeros(i, j)
	r = pd.DataFrame(matrix)
	for index, x, y in relation.itertuples():
		r.set_value(x-1, y-1, 1)
	return r

def get_dij(rij):
    sum_row = rij.sum(axis=1)
    sqrt = sum_row ** (0.5)
    sqrt = 1.0 / sqrt
    d = np.zeros((rij.shape[0], rij.shape[0]))
    np.fill_diagonal(d, sqrt)
    return d

def get_sij(rij):
    rji = rij.transpose()
    dij = csr_matrix(get_dij(rij))
    dji = csr_matrix(get_dij(rji))
    rijcsr = csr_matrix(rij)
    res = dij.dot(rijcsr).dot(dji)
    return res.todense()

R_patient_CBC = get_rij(num_patient, num_CBC, patient_CBC)
R_patient_metabolism = get_rij(num_patient, num_metabolism,patient_metabolism)
R_patient_ur = get_rij(num_patient, num_ur,patient_ur)


S_pc = get_sij(R_patient_CBC.values)
S_cp = get_sij(R_patient_CBC.T.values)
S_pm = get_sij(R_patient_metabolism.values)
S_mp = get_sij(R_patient_metabolism.T.values)
S_pu = get_sij(R_patient_ur.values)
S_up = get_sij(R_patient_ur.T.values)


train_patient = trainId_patient.merge(patient_label)
train_CBC = trainId_CBC.merge(CBC_label)
train_metabolism = trainId_metabolic.merge(metabolic_label)
train_ur= trainId_ur.merge(ur_label)

Y_p = get_yij(num_patient, num_label, train_patient)
Y_c = get_yij(num_CBC, num_label, train_CBC)
Y_m = get_yij(num_metabolism, num_label, train_metabolism)
Y_u = get_yij(num_ur, num_label, train_ur)

temp_p = Y_p
temp_m = Y_m
temp_c = Y_c
temp_u = Y_u


lamb = 0.2
alpha = 0.1

for x in xrange(1,7):
	f_p = (lamb * (S_pc.dot(temp_c) + S_pm.dot(temp_m) + S_pu.dot(temp_u)) + alpha * Y_p) / (3 * lamb + alpha)
	f_m = (lamb * S_mp.dot(temp_p) + alpha * Y_m ) / (lamb + alpha)
	f_u = (lamb * S_up.dot(temp_p) + alpha * Y_u ) / (lamb + alpha)
	f_c = (lamb * S_cp.dot(temp_p) + alpha * Y_c ) / (lamb + alpha)

	temp_p = f_p
	temp_m = f_m
	temp_u = f_u
	temp_c = f_c



result_a = 0
truth_patient = testId_patient.merge(patient_label)
pred_patient = (pd.DataFrame(np.take(np.argmax(f_p, axis = 1), testId_patient - 1)) + 1).T
for index, patient, label in truth_patient.itertuples():
	if pred_patient.iloc[index][0] == label:
		result_a = result_a + 1
print "\nAccuracy of patient class prediction:", result_a*100/750.0,"%"


result_m = 0
truth_m = testId_metabolic.merge(metabolic_label)
pred_m = (pd.DataFrame(np.take(np.argmax(f_m, axis = 1), testId_metabolic - 1)) + 1).T
for index, metabolic, label in truth_m.itertuples():
	if pred_m.iloc[index][0] == label:
		result_m = result_m + 1
print "Accuracy of metabolic tests:", result_m*100/5.0,"%"


result_c = 0
truth_c = CBC_label
pred_c = (pd.DataFrame(np.take(np.argmax(f_c, axis = 1), np.arange(20))) + 1).T
for index, CBC, label in truth_c.itertuples():
	if pred_c.iloc[index][0] == label:
		result_c = result_c + 1
print "Accuracy of CBC tests:", result_c*100/20.0,"%"


result_u = 0
truth_u = testId_ur.merge(ur_label)
pred_u = (pd.DataFrame(np.take(np.argmax(f_u, axis = 1), testId_ur - 1)) + 1).T
for index, ur, label in truth_u.itertuples():
	if pred_u.iloc[index][0] == label:
		result_u = result_u + 1
print "Accuracy of urinalysis tests:", result_u*100/3.0,"%"



