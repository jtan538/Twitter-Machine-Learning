import json

total = []
with open('data.txt','r') as file:
	for line in file:
		if not line.isspace():
			tweet = json.loads(line)
			total.append(tweet)
			print(tweet['text'])
			print('-----------------------------------')


