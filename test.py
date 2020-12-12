# shift right
a = bin(10)[2:]
print(a)
b = 2
c = ''
d = ''
for i in range(0, 8-len(a)):
    c = c + '0'
for i in range(0, b):
    d = d + '0'

print(c)

a = c + a
print(a)
a = d + a
a = a[:-b]
print(a)
print(int(a, 2))
print('===========')

# shift left
a = bin(2)[2:]
print(a)
b = 2
c = ''
d = ''
for i in range(0, 8-len(a)):
    c = c + '0'
for i in range(0, b):
    d = d + '0'

print(c)
a = c + a
print(a)
a = a + d
a = a[b:]
print(a)
print(int(a,2))