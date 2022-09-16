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


# default
def demo6():
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int, help="base")
    parser.add_argument("y", type=int, help="exponent")
    parser.add_argument("-v",'--verbose',action="count", default=0) # 不设定默认值，当不传入-v时，判断那里会出错
    args = parser.parse_args()
    answer = args.x ** args.y
    
    if args.verbose>=2: # -v/--verbose出现两次, 如果不出现 args.verbose 为None
        print(f"{args.x} to the power {args.y} is {answer}")
    elif args.verbose>=1:
        print(f"{args.x}^{args.y}={answer}")
    else:
        print(answer)
    # python .\0_argparse.py 2 3 -vv --> 2 to the power 3 is 8
    # python .\0_argparse.py 2 3 --> 8

# argparse.add_multually_exclusive_group() # 添加互斥的选项
# argparse.ArgumentParser(description="") # description
def demo7():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    # ! -v 和 -q 只能出现其中一个
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v","--verbose",action="store_true",help="increase output verbosity")
    group.add_argument("-q","--quiet",action="store_true",help="decrease output verbosity")

    parser.add_argument("x", type=int, help="base")
    parser.add_argument("y", type=int, help="exponent")
    args = parser.parse_args()
    answer = args.x ** args.y
    
    if args.quiet:
        print(answer)
    elif args.verbose:
        print(f"{args.x} to the power {args.y} is {answer}")
    else:
        print(f"{args.x}^{args.y}={answer}")
    
demo7()
    
