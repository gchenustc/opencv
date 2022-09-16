import argparse
import sys
print(sys.argv[0]) # 获得当前文件文件名

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

# 在代码中直接添加args
# parser.parse_args("2 4".split())
# parser.parse_args(["2","4"])
def demo8():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v","--verbose",action="store_true",help="increase output verbosity")
    group.add_argument("-q","--quiet",action="store_true",help="decrease output verbosity")

    parser.add_argument("x", type=int, help="base")
    parser.add_argument("y", type=int, help="exponent")

    # ! 添加args
    # args = parser.parse_args("2 4".split())
    args = parser.parse_args(["2","4"])
    # ! 打印帮助
    parser.print_help()

    answer = args.x ** args.y
    
    if args.quiet:
        print(answer)
    elif args.verbose:
        print(f"{args.x} to the power {args.y} is {answer}")
    else:
        print(f"{args.x}^{args.y}={answer}")

# metavar # 仅改变显示的名称
# 关于dest # 使用这个名字当做传入的属性的新的代号，但是传入参数的时候依然用原来的属性名 eg: name="x", dest="X" ; python file -x 1
def demo9():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v","--verbose",action="store_true",help="increase output verbosity")
    group.add_argument("-q","--quiet",action="store_true",help="decrease output verbosity")

    parser.add_argument("x", metavar="X", type=int, help="base")
    parser.add_argument("y", metavar="Y", type=int, help="exponent")

    # ! 添加args
    # args = parser.parse_args("2 4".split())
    args = parser.parse_args(["2","4","-v"])

    # 
    print(parser.print_help())

    answer = args.x ** args.y
    
    if args.quiet:
        print(answer)
    elif args.verbose:
        print(f"{args.x} to the power {args.y} is {answer}")
    else:
        print(f"{args.x}^{args.y}={answer}")

def demo9_1():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("-x", dest="X", type=int)
    parser.add_argument("-y", metavar="Y" )

    # ! 添加args
    args = parser.parse_args("-x 1 -y 2".split())

    print(parser.print_help())
    print(args.X)
    print(args.y)

# nargs：ArgumentParser对象通常将一个动作与一个命令行参数关联。nargs关键字参数将一个动作与不同数目的命令行参数关联在一起：
#nargs=N，一个选项后可以跟多个参数（action='append'时，依然是一个选项后跟一个参数，只不过选项可以多次出现），参数的个数必须为N的值，这些参数会生成一个列表，当nargs=1时，会生成一个长度为1的列表。
#nargs=?，如果没有在命令行中出现对应的项，则给对应的项赋值为default。特殊的是，对于可选项，如果命令行中出现了此可选项，但是之后没有跟随赋值参数，则此时给此可选项并不是赋值default的值，而是赋值const的值。并且只能接收一个参数
#nargs=*，和N类似，但是没有规定列表长度。
#nargs=+，和*类似，但是给对应的项当没有传入参数时，会报错error: too few arguments。
#nargs=argparse.REMAINDER，所有剩余的参数，均转化为一个列表赋值给此项，通常用此方法来将剩余的参数传入另一个parser进行解析。如果nargs没有定义，则可传入参数的数量由action决定，通常情况下为一个，并且不会生成长度为一的列表。
def demo10():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("x", metavar="X", nargs=2, type=int)
    parser.add_argument("y", metavar="Y", nargs=argparse.REMAINDER)

    # ! 添加args
    args = parser.parse_args("1 2 3 4 5".split())
    # args = parser.parse_args(["2","4","-v"])

    # print(parser.print_help())
    print(args.x)
    print(args.y)

def demo11():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("-x", metavar="X", nargs="?", type=int, default=1, const=2)

    # ! 添加args
    # args = parser.parse_args("-x".split())
    args = parser.parse_args("".split())
    # args = parser.parse_args(["2","4","-v"])

    print(args.x)


# required=True: 次属性是必须得传入的
def demo12():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("-x", required=True)

    # ! 添加args
    # args = parser.parse_args("-x".split())
    args = parser.parse_args("".split())
    # args = parser.parse_args(["2","4","-v"])

    print(args.x)
# demo12() # error: the following arguments are required: -x

# vars
# args_0 = parser.parse_args("-x 2 -y 4".split())
# args_1 = vars(parser.parse_args("-x 2 -y 4".split()))
# print(args_0) --> 
def demo13():
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("-x", type=int, required=True)
    parser.add_argument("-y", type=int, required=True)
    args_0 = parser.parse_args("-x 2 -y 4".split())
    args_1 = vars(parser.parse_args("-x 2 -y 4".split()))
    print(args_0, args_1)
demo13()

