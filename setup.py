import sys
path = input("Input path to myfreecadlib: \n").replace(" ","'")
sys.path.append(path)
def f1():
    return True
f1()