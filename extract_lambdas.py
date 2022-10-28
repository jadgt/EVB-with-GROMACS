import sys

init = []
final = []

filename = sys.argv[1]
zero = int(sys.argv[2])
one = int(sys.argv[3])
##Get data
def load_data (file):
    with open (file) as f:
        lines = f.readlines()
    for line in lines:
        if ("@" not in line) and ("#" not in line) and (" 0.0 " not in line):
            X = float(line.split()[zero])
            Y = float(line.split()[one])
            init.append(X)
            final.append(Y)
out=load_data(filename)
##Sort
res = "\n".join("{} {}".format(x, y) for x, y in zip(init, final))
##Print
name1 = filename.split(".")[0] + '.txt'
text_file = open(name1, "w")
text_file.write(res)
text_file.close()
