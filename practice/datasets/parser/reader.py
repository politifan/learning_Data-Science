
with open("test.txt","r") as f:
    print(f.read())

with open("test.txt","w") as f:
    f.write("hello world")

with open("test.txt","r") as f:
    print(f.read())