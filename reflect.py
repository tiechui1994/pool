"""
classmethod 	①注解,用来说明这个方式是个类方法
                ②类方法即可被类调用,也可以被实例调用(类方法类似于Java中的static方法, 类方法第一个参数是cls)
staticmethod	声明静态方法,是个注解


compile(source, filename, mode) 将source编译为代码或者AST对象. 代码对象能够通过exec语句来执行或者eval()进行求值.
                ①参数source: 字符串或者AST(Abstract Syntax Trees)对象.
                ②参数filename: 给出读取代码的文件;如果不从文件中读取,则传递一些可识别的值(通常使用'<string>').
                ③参数model: 指定编译代码的种类.'exec'编译模块，'single'编译单个(交互式)语句,或'eval'编译表达式
eval(expression [,globals [,locals]])	计算表达式expression的值
exec(str [,globals [,locals]]) 执行str命令
execfile(filename [,globals [,locals]])	用法类似exec(),不同的是execfile的参数filename为文件名,而exec的参数为字符串.


dir([object])	①不带参数时,返回当前范围内的变量、方法和定义的类型列表;
                ②如果是类实例化的对象, 且实现了__dir__()方法,则调用该对象的__dir__()方法.
                ③带参数的其他情况时,返回参数的属性,方法列表.
callable(object)  检查对象object是否可调用, ①类是可以被调用的;
                                          ②实例是不可以被调用的,除非类中声明了__call__方法

delattr(object, name)	删除object对象名为name的属性
getattr(object, name [,defalut])	获取一个类的属性
hasattr(object, name)	判断对象object是否包含名为name的特性
setattr(object, name, value)	设置属性值
property([fget[,fset[,fdel[,doc]]]]) 属性访问的包装类,设置后可以通过c.x=value等来访问setter和getter

globals()	返回一个描述当前全局符号表的字典, 在同一个文件当中globals() == locals()
locals() 	返回当前的变量列表

hash(object) 如果对象object为哈希表类型,返回对象object的哈希值
id(object)	 返回对象的唯一标识
len(s) 	返回集合长度

isinstance(object, classinfo)	判断object是否是class的实例
issubclass(class, classinfo)	判断是否是子类


filter(function, iterable)	构造一个序列,等价于[item for item in iterable if function(item)]
                ①参数function: 返回值为True或False的函数,可以为None
                ②参数iterable: 序列或可迭代对象
map(function, iterable, ...) 	遍历每个元素,执行function操作
memoryview(obj) 	返回一个内存镜像类型的对象
next(iterator[, default]) 	类似于iterator.next()

reduce(function, iterable[,initializer]) 合并操作,从第一个开始是前两个参数,然后是前两个的结果与第三个合并进行处理,以此类推
reload(module) 	重新加载模块
slice()         分片操作

super(type[,object-or-type]) 	引用父类
type(object)	返回该object的类型
vars([object]) 	返回对象的变量,若无参数与dict()方法类似

bytearray([source [,encoding [,errors]]])	返回一个byte数组
                ①如果source为整数,则返回一个长度为source的初始化数组;
                ②如果source为字符串,则按照指定的encoding将字符串转换为字节序列;
                ③如果source为可迭代类型,则元素必须为[0 ,255]中的整数;
                ④如果source为与buffer接口一致的对象,则此对象也可以被用于初始化bytearray.

zip([iterable, ...])  实在是没有看懂,只是看到了矩阵的变幻方面
"""


class Text(object):
    name = 'www'

    @classmethod
    def get(cls):
        return cls.name

    def __dir__(self):
        return 'www'

    def getName(self):
        return self.name


source = 'for i in range(0,10): print(i)'

code = compile(source, '<string>', 'exec')
print(code)
# exec(code)
# eval(code)

print(dir())

print(dir(Text))
text = Text()
print(dir(text))
print(repr(text))

glob = globals()
print(glob)

local = locals()
print(local)

print(text.name)
