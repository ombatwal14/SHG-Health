# SHG-Health
It includes implementation of SHG-Health algorithm in python and dummy database with test results 


Data Set (Heterogeneous Version):
	In the dataset we have the following files: 
	
	PC.txt: stores the undirected relations between patient and CBC. The first column is the patient ID, starting from 1, and the second column is the CBC_test ID, starting from 1.
	
	PM.txt: stores the undirected relations between patient and metabolic tests. The first column is the patient ID, starting from 1, and the second column is the metabolic_test ID, starting from 1.
	
	PU.txt: stores the undirected relations between patient and urinalysis tests. The first column is the patient ID, starting from 1, and the second column is the urinalysis_test ID, starting from 1.
	
	patient_label.txt: contains patient label information. The first column is patient id, and the second column is class id, starting from 1.
	CBC_label.txt: contains CBC_test label information.  The first column is CBC id, and the second column is class id, starting from 1.
	metabolic_label.txt: contains metabolic_test label information.  The first column is metabolic_test id, and the second column is class id, starting from 1.
	ur_label.txt: contains urinalysis_test label information.  The first column is urinalysis_test id, and the second column is class         id, starting from 1.
	
	trainId_patient.txt: contains patient IDs, whose label information will be used as prior knowledge.
	trainId_CBC.txt: contains CBC_test IDs, whose label information will be used as prior knowledge.
	trainId_metabolic.txt: contains metabolic_test IDs, whose label information will be used as prior knowledge.
	trainId_ur.txt: contains urinalysis_test IDs, whose label information will be used as prior knowledge.
	
	
	testId_patient.txt: contains patient IDs, whose label information will be used in evaluation.
	testId_CBC.txt: contains CBC_test IDs, whose label information will be used in evaluation.
	testId_metabolic.txt: contains metabolic_test IDs, whose label information  will be used in evaluation.
	testId_ur.txt: contains urinalysis_test IDs, whose label information  will be used in evaluation.
