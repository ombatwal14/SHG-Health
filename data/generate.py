from random import randint 
count =0;
val=1
i=1
while (i<=3000):
	j=randint(1,4)
	for m in range (j):
		print i,"  ",randint(1,5),"  ",val
	i+=1

