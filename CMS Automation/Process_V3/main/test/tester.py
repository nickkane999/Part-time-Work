file1 = "test1.html"
file2 = "test2.html"

with open(file1, 'r') as file:
	content1 = file.read().strip()
	file.close()

with open(file2, 'r') as file:
	content2 = file.read().replace("\n\n", "\n").strip()
	file.close()

print(content1)
print(content2)

if content1 == content2:
	print("True")