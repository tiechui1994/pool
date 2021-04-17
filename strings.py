"""
字符串的格式化:
format(*args,**kwargs)  #返回一个格式化后的字符串,原字符串的替换字段被适当格式化后的参数所替代.
    每个替换字段都是由包含在花括号中的字段名标识的.如果字段名是简单的整数,就将被作为传递给format()方法的一
    个参数的索引位置。即名为0的字段被第一个参数所替代,名为1的字段被第二个参数所替代。(切记字段名必须从0开始,
    否则无法赋值.
    s="Hello,{0},{1},{2}"
    s.format("Java","Python","Netty") --> 'Hello,Java,Python,Netty'
    如果字段名是字符串(不能以数字开头,或者是数字),那么format()方法中将使用的格式:字段名=值
    s="Hello,{A1},{A2},{A3}"
    s.format(A1="Java",A2="Python",A3="Netty") --> 'Hello,Java,Python,Netty'
    当然上述两者可以混合或者是嵌套使用,但是,使用数字的时候必须从0开始,依次增加,(在整个字符串当中,
    但是对于对于每个数字所处的位置没有强制性要求)而且在format()当中处于参数前半部分,而字段的依旧使用
    上述的格式,处于参数的后半部分.
    s="Hello,{name},{1},{0}"
    s.format("Python","Netty",name="Java") --> 'Hello,Java,Python,Netty'
    **列表,元组,集合,类的替换:
    s="Hello,{0[0]},{0[1]},{0[2]}"
    name=["Python","Netty","Java"]
    s.format(name) --> 'Hello,Java,Python,Netty'
    s="math.pi={0.pi}"
    s.format(math) --> 'math.pi=3.14159265359'
    在作用范围内的局部变量可以使用locals()函数传递format()参数,前提是字符串中使用的是字段名,
    而且这些字段名在当前的作用范围内都是变量名,且已经赋值了,则可以这样写format(**locals())
    Aa="Java"
    Bb="Python"
    s="Hello,{Aa},{Bb}"
    s.format(**locals())  --> 'Hello,Java,Python'
    locals()--->Directory,产生当前作用范围的key-value字典对
规约格式(可选):
    [fill][align][sign][#][0][width][.][.precision][type]
参数解析:
    fill: any character except '}', 填充字符
    align: "<" left, ">" right, "^" center对齐方式, "=" 用于在符号与数字之间进行分割
    sign: "+" | "", 数字是否带正负标识 (+表示正数带符号标识, ""标识正数带空白标识)
    #: 整数前缀为0b,0o,0x
    width: 最小宽度
    precision: 浮点型小数位数或字符串的最大长度
    type: "b" | "c" | "d" | "e" | "E" | "f" | "g" | "G" | "n" | "o" | "x" | "X" | "%" 类型
字符串格式规约是使用冒号(:)引入的, 其后跟随可选的字符 -- 一个填充字符(也可没有) 与一个对齐字符(<用于左对齐,
>用于右对齐, ^用于中间对齐), 之后跟随的是可选的最小宽度(整数), 若需要指定最大宽度, 就在其后
使用句点, 句点后跟随一个整数.
填充: 数字或者字符串包含对齐方式的长度达不到width时候,会发送在字符串前填充达到最小宽度
    '{0:.<12}'.format('hello') --> 'hello.......'
    '{0:p=12}'.format(1234)  --> 'pppppppp1234'
    '{0:0=12}'.format(1234)或者'{0:012}'.format(1234) --> '000000001234'
width与precision
    格式化的是字符串: width指明最终的输出字符串的长度, 不够则在后面补空格.
    '{0:5}'.format('abc') --> 'abc  '
    格式化的是数字: width指明最终的输出字符串的长度,不够则在前面补空格(默认情况,可以通过设置填充字符).
    '{0:5}'.format(123) --> '  123'
    '{0:05}'.format(123) --> '00123'
    格式化的是字符串或者浮点数: precision指明输出字符串的最大长度, 对于超过的部分截断. 浮点数超过最大长度,
    则转换为科学计数法(小数点不计入长度当中).
    '{0:1.2}'.format('abc') --> 'ab'
    '{0:1.5}'.format(123.0) --> 123.0
type:数字的格式化
    "b" 二进制
    "d" 十进制
    "o" 八进制
    "g" 和 "n" 十二进制(整数前面需要添加至少0, 否则还是十进制)
    "x" 十六进制
    "e" 科学计数
    "f" 浮点数
    "%" 百分制
"""

print('{0:p=12}'.format(1234))
print('{0:5}'.format('123'))
print('{0:1.2}'.format(123.11))
