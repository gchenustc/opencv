import argparse

# type
def demo1():
    parser = argparse.ArgumentParser(description='proceee some integers')
    # parser.add_argument("square", help="display the square of a given number", type=int) # python file 2 --> 4
    parser.add_argument("--square", help="display the square of a given number", type=int) # python file --square 2 --> 4
    args = parser.parse_args()
    print(args.square **2)

# store_true
def demo2():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true") # action="store_true" : 出现--verbose，verbose则为True
    args = parser.parse_args()
    print(args.verbose) # python file --verbose --> True

# 位置参数结合--arg
def demo3():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",'--verbose', help="increase output verbosity", action="store_true")
    parser.add_argument("square", help="display the square of a given number", type=int)
    args = parser.parse_args()
    if args.verbose:
        print(f"the square of {args.square}, is {args.square ** 2}")
    else:
        print(args.square ** 2)
    # python .\0_argparse_1.py -v 4 --> 16
    # python .\0_argparse_1.py 4 -v --> 16

# choice
def demo4():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",'--verbose', help="increase output verbosity", type=int, choices=[0,1,2]) # type=int不能少，因为choice中的都是Int类型
    parser.add_argument("square", help="display the square of a given number", type=int)
    args = parser.parse_args()
    if args.verbose==2:
        print(f"the square of {args.square}, is {args.square ** 2}")
    elif args.verbose==1:
        print(f"{args.square}**2 = {args.square ** 2}")
    else:
        print(args.square ** 2)

# count
def demo5():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",'--verbose', help="increase output verbosity", action="count") 
    parser.add_argument("square", help="display the square of a given number", type=int)
    args = parser.parse_args()
    if args.verbose==2: # -v/--verbose出现两次, 如果不出现 args.verbose 为None
        print(f"the square of {args.square}, is {args.square ** 2}")
    elif args.verbose==1:
        print(f"{args.square}**2 = {args.square ** 2}")
    else:
        print(args.square ** 2)