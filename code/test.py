from preprocess import load_data_dict

result = load_data_dict('../data/ensemble_result.txt')
test = load_data_dict('../data/test.txt')
train = load_data_dict('../data/train.txt')
ans1 = 0
ans2 = 0
ans3 = 0
for i in range(4039):
	if not result.has_key(i):
		x = 0
	else: x = len(result[i])
	if not test.has_key(i):
		y = 0
	else: y = len(test[i])
	if not train.has_key(i):
		z = 0
	else: z = len(train[i])
	print i,' result: ', x,', test: ', y, ', train: ', z
	if x > y:
		ans1+=1
	elif x < y:
		ans2+=1
	else:
		ans3+=1
print ans1
print ans2
print ans3