import math


def print_string():
    string = "hello"

    # %s打印时结果是hello
    print("string=%s" % string)  # output: string=hello

    # %2s意思是字符串长度为2，当原字符串的长度超过2时，按原长度打印,不当原字符串的长度小于2时，在原字符串左侧补空格
    print("string=%2s" % string)  # output: string=hello

    # %-7s意思是字符串长度为7,当原字符串的长度小于7时，在原字符串右侧补空格，
    # 所以%-7s的打印结果是  hello
    print("string=%-7s!" % string)  # output: string=hello  !

    """
    %.2s是截取字符串的前2个字符,当原字符串长度小于2时，是字符串本身
    """
    print("string=%.2s" % string)  # output: string=he

    """
    %a.bs 长度.截取长度
    %a.bs 这种格式是上面两种格式的综合，首先根据小数点后面的数b截取字符串,当截取的字符串长度小于a时,还需要在
    其左侧补空格
    """
    print("string=%7.2s" % string)  # output: string=     he
    print("string=%2.7s" % string)  # output: string=hello
    print("string=%-10.7s!" % string)  # output: string=     hello

    # 还可以用%*.*s来表示精度，两个*的值分别在后面小括号的前两位数值指定
    print("string=%*.*s" % (7, 2, string))  # output: string=     he


def print_integer():
    num = 14

    # %d打印时结果是14
    print("num=%d" % num)  # output: num=14

    # %nd: 为n位整数，当整数的位数不够n位时，在整数左侧补空格
    # %3d的打印结果是 14
    print("num=%3d" % num)  # output: num= 14

    # %-nd: 为n位整数，当整数的位数不够n位时，在整数右侧补空格
    # %3d的打印结果是14
    print("num=%-3d" % num)  # output: num=14

    # %0nd: 为n位整数，当整数的位数不够n位时，在整数左侧补0
    # %05d的打印结果是00014
    print("num=%05d" % num)  # output: num=00014

    """
    %.nd 整数位保留n位, 不足了在前面补充0, 位数超过n位不管 <==> %0nd: 为n位整数，当整数的位数不够n位时，在
    整数左侧补0所以%.3d的打印结果是014
    """
    print("num=%.3d" % num)  # output: num=014

    """
    %m.nd 实际长度.有效长度
    %m.nd 两种补齐方式的综合,当整数的位数不够n时，先在左侧补0，还是不够m位时，再在左侧补空格，最终的长度选数
    值较大的那个.
    %5.3d的打印结果还是  014
    """
    print("num=%5.3d" % num)  # output: num=  014

    """
    %m.nd 实际长度.有效长度
    %m.nd 两种补齐方式的综合,当整数的位数不够n时，先在左侧补0，还是不够m位时，再在左侧补0，最终的长度选数值较
    大的那个.
    %05.3d的打印结果还是00014
    """
    print("num=%05.3d" % num)  # output: num=00014

    # 还可以用%*.*d来表示精度，两个*的值分别在后面小括号的前两位数值指定
    # 如下，不过这种方式04就失去补0的功能，只能补空格，只有小数点后面的3才能补0
    print("num=%*.*d" % (4, 3, num))  # output: num= 014


def print_float():
    """
    %m.nf，m表示浮点数的打印长度，n表示浮点数小数点后面的精度
    """

    # 只是%f时表示原值，默认是小数点后5位数
    print("PI=%f" % math.pi)  # output: PI=3.141593

    # 只是%9f时，表示打印长度9位数，小数点也占一位，不够左侧补空格
    print("PI=%9f" % math.pi)  # output: PI= 3.141593

    # 只是%9f时，表示打印长度9位数，小数点也占一位，不够左侧补0
    print("PI=%09f" % math.pi)  # output: PI= 3.141593

    """只有.没有后面的数字时，表示去掉小数输出整数，3表示不够3位数左侧补空白"""
    print("PI=%5.f" % math.pi)  # output: PI=003

    """只有.没有后面的数字时，表示去掉小数输出整数，03表示不够3位数左侧补0"""
    print("PI=%05.f" % math.pi)  # output: PI=003

    # %6.3f表示小数点后面精确到3位，总长度6位数，包括小数点，不够左侧补空格
    print("PI=%6.3f" % math.pi)  # output: PI= 3.142

    # %-6.3f表示小数点后面精确到3位，总长度6位数，包括小数点，不够右侧补空格
    print("PI=%-6.3f" % math.pi)  # output: PI=3.142

    # 还可以用%*.*f来表示精度，两个*的值分别在后面小括号的前两位数值指定
    # 如下，不过这种方式06就失去补0的功能，只能补空格
    print("PI=%*.*f" % (6, 3, math.pi))  # output: PI= 3.142


def print_hex():
    # d,i   带符号的十进制整数
    # o     不带符号的八进制
    # u     不带符号的十进制
    # x     不带符号的十六进制（小写）
    # X     不带符号的十六进制（大写）
    # e     科学计数法表示的浮点数（小写）
    # E     科学计数法表示的浮点数（大写）
    # f,F   十进制浮点数
    # C     单字符（接受整数或者单字符字符串）
    # s     字符串（使用str转换任意python对象）
    num = 80812
    print('num=%X' % num)


if __name__ == '__main__':
    print_integer()
    # print_float()
    # print_hex()
