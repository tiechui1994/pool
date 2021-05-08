"""
文本当中插入变量:
方式一: 使用字符串的格式化输出. %(NAME)TYPE -> 输入字典 ,  %TYPE -> 输入元组
方式二: 使用str的format {NAME} 或者是 {NAME:TYPE} -> 输入k-v
方式三: 使用string模板  $NAME -> 输入字典
"""
import string

form = """\
Dear %(name)s,
Please send back my %(item)s or pay me $%(amount)0.2f.
                            Sincerely  yours,
                             Joe Python User
"""
print(form % {
    'name': 'Mr. Bush',
    'item': 'blender',
    'amount': 50.00
})

form = """\
Dear {name},
Please send back my {item} or pay me ${amount:0.2f}.
                            Sincerely  yours,
                             Joe Python User
"""
print(form.format(name='Mr. Bush', item='blender', amount=50.0))

form = string.Template("""\
Dear $name,
Please send back my $item or pay me $amount.
                            Sincerely  yours,
                             Joe Python User
""")

print(form.substitute({
    'name': 'Mr. Bush',
    'item': 'blender',
    'amount': '$%0.2f' % 50.00
}))
