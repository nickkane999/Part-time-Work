import re

search = "</\w+>"
string = "<body><h2>Some stuff</h2><p>Hello</p><ul><li>Data1</li><li>Data2</li></ul></body>"
count = 0
for m in re.finditer(r''+search, string):
	string = string[:m.end()+count] + "\n" + string[m.end()+count:]
	count+=1															# Keeps track of "new string" position
print(string)