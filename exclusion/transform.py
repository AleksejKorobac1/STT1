


with open('words'+'.txt') as f:
    content = f.read()
    replace = set(content.split())

with open('words2'+'.txt') as f:
    content = f.read()
    replace2 = set(content.split())

replace2 = replace2.difference(replace)

print(len(replace2))


f = open('words2' + '.txt', 'w')
for item in replace2:
    f.write(item + '\n')
