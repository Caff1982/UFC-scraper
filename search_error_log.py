
count = 0
val_err = 0
key_err = 0
with open('scrapy.log') as f:
	for line in f:
		if 'ERROR' in line:
			count +=1
		if 'ValueError' in line:
			val_err +=1
		if 'KeyError' in line:
			key_err +=1

print(count, 'total errors')
print(val_err, 'value errors, fighters missing reach/height/weight. Will make optional fields')
print(key_err, 'index error, result invalid due to disqualification, overturned etc. Will probably leave out')