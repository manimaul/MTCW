import md5sum, os

def isEven(i):
    return i%2 and True or False

out = ""

i=0;
dir = "/home/will/charts/gemfs/"
lst = os.listdir(dir)
lst.sort()
for p in lst:
    if p.endswith(".gemf"):
	print p
        out += "<item>" + str(md5sum.getFilesum(dir+p)) + "</item>"
        if isEven(i):
            out+="\n"
        i+=1

print out
