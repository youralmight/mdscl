# DSCI 511 Quiz 1：Python 知识复习

## 范围状态（2026-09-13）

**Quiz 1 的逐项范围尚未由本学期教师公开。** 课程 README 确认有 Quiz 1（25%）；Canvas 的 Quiz 1 成绩项没有题目或范围，Canvas 的 Quizzes 页面也没有已发布 quiz。PrairieLearn 已发布 `Practice Quiz 1` 和 Quiz 1 cheatsheet 上传项，但练习题须在诚信声明后才可开始，故未访问其题目；cheatsheet 截止为 9 月 14 日 23:59，但这不是范围说明。
- **已确认的 MDS 通用 logistics：**每次 quiz 为 50 分钟、在 PrairieLearn（PL）交付；学生在 ORCA 机房以异步方式应考并通过 PrairieTest 预约。除非教师明确允许单面一页 Letter 大小的 digital cheatsheet，否则为闭卷。具体到本课的资源/cheatsheet 政策仍须等教师说明。

因此，本笔记覆盖目前已确认在 Quiz 1 准备期前教过、且由已发布的 Worksheet 1–2 与 Lab 1 练习支持的 **Lecture 1–4**：Python 基础、控制流与函数、函数设计/OOP、NumPy。把这些当作**有证据支持的复习范围推断**，而不是教师公布的边界。课程仓库虽已含 Lecture 5（pandas），但没有范围公告把它纳入 Quiz 1，故不把 pandas 当作本笔记的 Quiz 1 内容。

- [未确认] Quiz 1 是否恰好截止于 Lecture 4，以及是否有 Lecture 1–4 中的排除主题。
- [未确认] Practice Quiz 1 的具体题型、题目和其是否另有范围说明。
- [未确认] 本课 Quiz 1 的确认考试窗口/预约安排，以及允许资源与 cheatsheet 的具体政策和格式。

---

## 1. Python 如何执行代码

### 解释器、脚本与 notebook

- **编译器**先把源代码翻译成机器码；**解释器**让 Python 代码在运行时由 Python 执行。这个二分是帮助理解的近似模型；关键是 Python 通常不要求你手动完成一个独立的编译步骤。
- **解释器（REPL）**适合逐行试验：表达式的结果会自动显示。
- **脚本**是 `.py` 文件；`python file.py` 顺序执行其中的语句。脚本中表达式的值不会自动显示，需 `print(...)`。
- **Jupyter/IPython notebook**按 cell 执行，共享同一个内核状态。重新运行早期 cell 不会自动重新运行依赖它的后续 cell；乱序执行会留下过时的变量值。遇到奇怪结果时，按依赖顺序 Restart/Run All，而不是只盯当前 cell。

Python 是通用编程语言；本课把它用于数据工作。之后的 NumPy、pandas 是库，不是另一门语言。

### 值、名字、表达式与语句

- **对象/值**有类型；`type(x)` 返回对象的类型，例如 `int`、`list`、`NoneType`。
- `name = value` 是**赋值语句**：名字绑定到对象，并不必然复制对象。`x = y` 常使两个名字指向同一对象。
- **表达式**会求值为一个值，例如 `2 + 3`、`x`、`len(items)`；**语句**执行动作，例如赋值、`if`、`for`、`def`。
- 调用 `f(a, b)` 时，先求值函数对象 `f` 和每个实参表达式，再调用函数；嵌套调用从内到外完成。可逐层把子表达式替成它的值来手算。

```python
from operator import add, mul
add(mul(2, 3), mul(add(1, 1), 5))
# mul(2, 3) -> 6；add(1, 1) -> 2；mul(2, 5) -> 10；add(6, 10) -> 16
```

### 基本类型、运算与比较

| 类型 | 例子 | 要点 |
|---|---|---|
| `int` | `5`, `-2` | 整数 |
| `float` | `5.0`, `-0.3` | 浮点数；`5 / 2` 是 `2.5`（`float`） |
| `bool` | `True`, `False` | 布尔值首字母大写 |
| `str` | `"data"` | 不可变的字符序列 |
| `NoneType` | `None` | 明确表示“没有值”；不是字符串 `"None"` |

- `+ - * / ** // %` 分别为加、减、乘、除、幂、整除、余数。
- `//` 是**向下取整**，不是简单截小数：`7 // 3 == 2`，但 `-7 // 3 == -3`。
- `%` 是余数；常用于整除判断：`n % 2 == 0`。Python 满足 `a == (a // b) * b + (a % b)`。
- `== != < <= > >=` 比较**值**，结果是 `bool`。`2 == 2.0` 为 `True`；`2 != "2"` 为 `True`。
- `is`/`is not` 比较是否是**同一个对象**，不是值是否相等。通常只用 `x is None` / `x is not None`；不要用 `is` 比较普通数值或字符串。
- `and`、`or`、`not` 用于布尔逻辑。用在非布尔对象时，`and`/`or` 返回其中一个操作数，而不一定返回 `True`/`False`；例如 `user_name or "default"` 在空字符串时给默认值。

### 类型转换与纯函数

- `int(x)`、`float(x)`、`str(x)` 尝试创建新类型的对象：`int(5.9)` 为 `5`（向 0 截断），`str(5.0)` 为 `"5.0"`。不合法的转换会抛异常，如 `float("hello")`。
- **纯函数**只依赖输入并返回值，不改变外部可观察状态；相同输入给相同输出。
- **有副作用（non-pure）**的调用还会改变状态或做 I/O。`print("hi")` 显示文字且返回 `None`；`lst.append(x)` 改变列表且也返回 `None`。不要把返回 `None` 的原地方法误当成新列表。

---

## 2. 内置容器、索引与可变性

### 选对容器

| 容器 | 写法 | 顺序/访问 | 可变？ | 典型用途 |
|---|---|---|---|---|
| `list` | `["a", "b"]` | 有序；按 0-based index | 是 | 可增删改的序列 |
| `tuple` | `(3, 5)` | 有序；按 index | 否 | 固定记录、可作 dict key |
| `dict` | `{"name": "Ada"}` | 按 key 查 value | 是 | 键到值的映射 |
| `set` | `{1, 2, 3}` | 无 index；唯一元素 | 是 | 去重、成员检查 |
| `str` | `"abc"` | 有序字符；按 index | 否 | 文本 |

- list、tuple、str 都是**序列**：支持 `len`、成员测试 `x in seq`、索引和切片。
- dict 的 key 必须可哈希（实践中用不可变值，如 `str`、`int`、tuple）；`[1, 2]` 不能作 key。set 的元素也必须可哈希。
- `{}` 是空 `dict`，空 set 写 `set()`。
- set 会去重且不能按位置索引；用它时不要依赖显示或迭代顺序。

### 索引与切片：`start:stop:step`

Python 从 0 开始索引；负 index 从末尾数起，`-1` 是最后一个元素。切片的 `stop` **不包含**：

```python
items = ["a", "b", "c", "d", "e"]
items[1]       # "b"
items[-1]      # "e"
items[1:4]     # ["b", "c", "d"]
items[:3]      # ["a", "b", "c"]
items[::2]     # ["a", "c", "e"]
items[::-1]    # 反转后的新 list
```

- 单一索引越界是 `IndexError`；切片越过端点通常只取可得部分。
- `d[key]` 取 dict value；不存在的 key 是 `KeyError`。它不是“第 key 个元素”。
- 嵌套结构逐层索引：`movies["Coco"]["genres"][0]`。每个 `[]` 都是在前一步结果上继续取值。

### 修改 list 和 dict；返回值陷阱

```python
fruits = ["apple", "banana"]
fruits.append("pear")          # 原地加一个元素；返回 None
fruits.extend(["mango", "kiwi"])  # 原地逐个加入 iterable
fruits.insert(1, "orange")     # 原地插在 index 1 前
removed = fruits.pop()          # 删除并返回最后一个元素（也可 pop(i)）
fruits.remove("banana")        # 删除第一个匹配值；返回 None

scores = {"Ada": 95}
scores["Grace"] = 98           # 新增/覆盖 value
removed_score = scores.pop("Ada")  # 删除并返回 value
del scores["Grace"]            # 删除；不返回值
```

- `append(["mango", "pear"])` 加的是**一个 list 元素**；要追加其中各元素用 `extend(...)`。
- `list.index(value)` 返回首次出现的位置；找不到会 `ValueError`。
- `dict.keys()`、`.values()`、`.items()` 分别给 key/value/`(key, value)` 的可迭代 view；需要 list 行为时显式 `list(d.items())`。用 key 访问 dict，而不要把 dict 当可按位置取的 list。
- `collections.Counter` 是适合计数的 dict-like 类型：缺失 key 的计数从 0 开始。

### 可变、不可变与 alias

赋值复制的是**名字绑定**，不是一般意义的深拷贝：

```python
original = [1, 2, 3]
alias = original
alias.append(4)
# original 也是 [1, 2, 3, 4]：两个名字指向同一可变 list

copied = original.copy()  # 或 original[:]
copied.append(5)          # 不会改变 original（浅拷贝）
```

- list、dict、set 可原地修改；tuple、str、int、float、bool 不可原地修改。对不可变值写 `x = x + 1` 是把 `x` **重新绑定**到新对象，不会改变先前绑定给 `y` 的整数。
- `.copy()`/`[:]` 对嵌套对象通常是**浅拷贝**：内层可变对象仍可能共用。
- `id(obj)` 显示对象 identity 的实现相关整数，可用来检查两个名字是否引用同一对象；不要把它当可移植的“内存地址”。
- tuple 可解包：`x, y = (3, 5)`。逗号本身会造 tuple：`result = a, b`。

### 字符串操作与 f-string

str 不可变；下列方法返回**新字符串/新 list**，不改变原来的 `text`：

| 操作 | 返回值与用途 |
|---|---|
| `text.lower()`, `.upper()` | 改大小写后的 `str` |
| `text.strip()` / `.lstrip()` / `.rstrip()` | 去两端/左端/右端空白后的 `str` |
| `text.find(sub)` | 子串起点；找不到为 `-1` |
| `text.index(sub)` | 子串起点；找不到为 `ValueError` |
| `text.replace(old, new)` | 替换后的 `str` |
| `text.split(sep)` | 按分隔符切出的 `list[str]`；无参数按空白切分 |
| `sep.join(parts)` | 用 `sep` 把字符串 iterable 连成一个 `str` |

`join` 的调用方向常错：`" ".join(["data", "science"])`，不是 `words.join(" ")`。

```python
name, score = "Ada", 9.5
f"{name}: {score:.1f}"       # "Ada: 9.5"
f"item {3:02}"               # "item 03"
```

f-string 在引号前写 `f`；`{...}` 内是可求值的 Python 表达式。格式 `:.2f` 表示浮点数保留两位小数，`:02` 表示至少两位、用 0 补齐。

---

## 3. 控制流、迭代与 comprehension

### 条件与缩进

```python
if x > 0:
    label = "positive"
elif x < 0:
    label = "negative"
else:
    label = "zero"
```

- `if`/`elif` 从上到下测试，遇到第一个真条件后跳过同一链其余分支；`else` 只在前面都假时执行。
- 不要把应互斥的分类写成多个独立 `if` 再接一个 `else`：该 `else` 只属于紧邻的最后一个 `if`。
- 冒号后的缩进块（suite）是语法和语义的一部分；通常用 4 个空格，退回原缩进即离开该块。
- 假值（falsy）包括 `False`、`None`、数值 0、空 `str`、空 list/tuple/dict/set；其他对象通常为真。条件可直接写 `if items:`，但在“缺失”与“合法的 0/空值”不同的情形应明确比较。
- 单行条件表达式是 `a if condition else b`；仅在很简单时使用。

### `while`、`for`、`break`、`continue`

```python
n = 3
while n > 0:
    print(n)
    n -= 1                 # 必须推动条件变为 False

for i, value in enumerate([10, 20]):
    print(i, value)        # 0 10；1 20
```

- `while condition:` 每轮先检查 condition；若循环体不改变终止条件，可能无限循环。
- `for name in iterable:` 依次把 iterable 的元素绑定给 `name`。list、tuple、set、dict、str 都可迭代；遍历 dict 默认给 **keys**，需要 value 或 pair 时用 `.values()` / `.items()`。
- 字符串也是字符 iterable。意外得到单个字符时，检查是否把一个 `str` 当成“字符串列表”来遍历。
- `range(stop)` 产生 `0` 到 `stop - 1`；`range(start, stop, step)` 的 stop 同样不含。`range(len(seq))` 可按 index 访问；同时需要 index 和值时 `enumerate(seq)` 更直接。
- `break` 立即退出最内层循环；`continue` 跳过本轮剩余语句，开始下一轮。二者之后同一轮的代码不会运行。

### Comprehension：由 iterable 构造容器

```python
words = ["Ada", "grace", "Lin"]
lengths = [len(word) for word in words]
caps = [word for word in words if word[0].isupper()]
first_to_word = {word[0]: word for word in words}
unique_lengths = {len(word) for word in words}
flat = [x for row in [[1, 2], [3]] for x in row]
```

读法是：对每个 `for` 值，计算最左侧表达式；末尾 `if` 是过滤条件。dict comprehension 写 `{key_expr: value_expr for ...}`。

- `for key, value in d.items()` 和 `for i, x in enumerate(xs)` 是**解包**：每次迭代产物的长度/形状必须匹配左侧名字数，否则报错。
- 嵌套 comprehension 中后一个 `for` 是内层循环；`[x for row in rows for x in row]` 扁平化一层。
- `(x for x in xs)` 是 generator expression，不是 tuple；若要 tuple 用 `tuple(x for x in xs)`。

---

## 4. 函数：接口、作用域与可靠性

### 定义、调用和返回

```python
def repeat(text: str, n: int = 2) -> str:
    """Return text repeated n times."""
    return text * n
```

- `def` 定义函数，不执行函数体；调用 `repeat("ha", 3)` 才执行。
- **parameter** 是定义中的名字（`text`, `n`）；**argument** 是调用传入的值。
- `return value` 立即结束函数并把 value 交给调用者。没有 `return`（或只执行到末尾）时返回 `None`；`print` 不是 return。
- Python 只返回一个对象；`return low, high` 返回一个 tuple，可用 `low, high = min_and_max(xs)` 解包。
- 函数也是对象：可赋给名字、作为实参传递；`lambda x: x + 1` 造一个单表达式的匿名 function，适合很小的局部操作。

### 实参与默认值

```python
def describe(value, unit="items"):
    return f"{value} {unit}"
```

本课核心调用规则：

1. 无默认值的 required parameter 必须在有默认值的 optional parameter 之前。
2. positional argument 按位置绑定；keyword argument 按 parameter 名绑定。
3. positional argument 不能放在 keyword argument 之后：`f(a=1, 2)` 是语法错误。
4. 可用 keyword 指定某个 optional 参数：`repeat("ha", n=3)`；这样比靠第几个位置更清楚。
5. `*args` 将额外 positional arguments 收成 tuple；`**kwargs` 将额外 keyword arguments 收成 dict。

**可变默认值陷阱：**默认表达式在函数定义时创建一次，不能写 `def add(x, values=[]): ...` 并不断 `append`。用 `None` 表示“调用者没有提供值”，再在函数内创建新 list：

```python
def add(x, values=None):
    if values is None:
        values = []
    values.append(x)
    return values
```

### 局部/全局名字、mutation 与副作用

- 函数体内赋值的名字默认是**局部**名字；函数结束后不能在外部使用它。函数可以读取外层名字，但若要在函数里重新绑定全局名字必须显式 `global name`（通常应避免）。
- 改变传入的可变对象与重新绑定 parameter 不同：

```python
def mutate(xs):
    xs.append(0)       # 改 caller 所见的同一个 list

def rebind(xs):
    xs = xs + [0]      # 只把局部 xs 绑定到新 list
```

- 会打印、写文件、改传入 list/dict 或改全局状态的函数有副作用。若副作用是函数契约的一部分，docstring 应说明；需要保留输入时先复制或构造新对象。
- DRY（Don't Repeat Yourself）不是把每一行都强行抽成函数，而是把真正重复、可命名、可复用的行为封装，令函数只做一个容易解释的工作。

### 文档、type hints 与异常

- docstring 紧跟在 `def` 后的三引号字符串；简短函数可用一行。较大函数至少交代：行为、参数、返回值、特殊情况/副作用和用法。课程推荐 NumPy/SciPy 风格的 `Parameters`、`Returns`、`Examples` 小节。
- `x: int` 和 `-> str` 是 type hint，帮助读者和 IDE；普通 Python 不会因 hint 自动拒绝其他类型。
- 预测错会抛**异常**，不是返回一个特殊正常值。读 traceback 的异常类型和信息。

```python
try:
    value = int(text)
except ValueError as exc:
    print(f"Not an integer: {exc}")
else:
    print(value)         # 仅在 try 成功时
finally:
    close_resource()     # 无论成功、失败或 return 都执行
```

- 只捕获你能处理的具体异常（如 `ValueError`、`KeyError`、`IndexError`、`TypeError`、`ZeroDivisionError`）；裸 `except:` 会掩盖 bug。
- `raise TypeError("...")` 可在函数边界主动给出清楚的错误。自定义异常 class 继承 `Exception`。

---

## 5. 面向对象（OOP）

### class、instance、attribute、method

- **class** 是创建某类对象的蓝图；**instance/object** 是该 class 创建出的具体对象。`isinstance(obj, Class)` 检查关系。
- **attribute** 是对象状态（如 `dog.name`）；**method** 是定义在 class 内的 function（如 `dog.teach_trick("roll")`）。调用 method 要有 `()`；没有 `()` 取得的是 method 对象本身。
- `__init__` 是实例初始化时自动运行的 special method；regular instance method 的第一个 parameter 是 `self`，调用 `obj.method(x)` 时 Python 自动传入该 obj。

```python
class Dog:
    species = "dog"                 # class attribute：所有实例默认共享

    def __init__(self, name):
        self.name = name              # instance attribute：每个实例自己的值
        self.tricks = []

    def teach(self, trick):
        self.tricks.append(trick)

    def description(self):
        return f"{self.name}: {self.tricks}"
```

- class attribute 写在 `__init__` 外；更改 `Dog.species` 会影响未覆盖它的各实例。`dog.species = "..."` 会在那个实例上建立/覆盖同名 instance attribute，通常不是想要的“改全班规则”。
- 每个实例的可变状态应在 `__init__` 用 `self.tricks = []` 创建；不要把会被改的 list 作为 class attribute，否则所有实例共享它。

### 三类 method

| 种类 | 写法/首参 | 何时用 |
|---|---|---|
| instance method | 无 decorator；`self` | 需要读/改某个实例状态 |
| class method | `@classmethod`；`cls` | 需要 class 本身；常作 alternative constructor |
| static method | `@staticmethod`；无自动 `self`/`cls` | 与 class 相关但不需实例或 class 状态的 utility |

```python
class Member:
    def __init__(self, first, last):
        self.first, self.last = first, last

    @classmethod
    def from_csv(cls, text):
        first, last = text.split(",")
        return cls(first, last)

    @staticmethod
    def is_quiz_week(week):
        return week in [3, 5]
```

`cls(...)` 而不是写死 `Member(...)`，使 alternative constructor 也可正确构造 subclass。

### 继承与 special methods

```python
class Student(Member):
    role = "student"

    def __init__(self, first, last, grade):
        super().__init__(first, last)   # 复用 parent 初始化
        self.grade = grade
```

- `class Student(Member):` 令 `Student` 继承 parent/superclass `Member`；它可新增或重写 attribute/method。查找时先找 subclass，再沿继承链找 parent。
- 重写 `__init__` 后，用 `super().__init__(...)` 初始化父类部分，避免复制父类已有逻辑。
- double-underscore **special (magic) methods**让内置语法有意义：`__len__` 支持 `len(obj)`，`__eq__` 定义 `==`，`__str__` 定义 `print(obj)` 的字符串。定义它们前先说明何种比较/长度对该 class 有合理含义。

---

## 6. NumPy：同质多维数组

```python
import numpy as np
```

`np.ndarray` 是矩形（每一维长度一致）、通常同 dtype 的 n 维数组。相较 Python list，它适合数值数据：连续同质存储和 C 实现使批量数值运算通常更快、更节省内存；更关键的使用方式是**向量化**。

### 属性与创建

| 表达式 | 返回/含义 |
|---|---|
| `np.array(data)` | 从 list/tuple 等创建 `ndarray`；混合类型可能被 coerced 为共同 dtype |
| `np.arange(start, stop, step)` | 等间隔 `ndarray`；`stop` 不含，和 `range` 一样 |
| `np.linspace(start, stop, num)` | `num` 个等距值；默认包含 `stop` |
| `np.full(shape, fill_value)` | 指定 shape、填满某值的 array |
| `np.zeros(shape)` | 全 0 array |
| `np.random.rand(d0, d1, ...)` | 给定维度、元素在 `[0, 1)` 的随机 float array |
| `a.dtype` | 元素 dtype |
| `a.shape` | 各轴长度组成的 tuple，如 `(2, 3)` |
| `a.size` / `a.ndim` | 总元素数 / 轴数 |

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
# a.shape == (2, 3), a.ndim == 2, a.size == 6
np.arange(0, 10, 2)       # array([0, 2, 4, 6, 8])
np.linspace(0, 1, 5)      # array([0.  , 0.25, 0.5 , 0.75, 1.  ])
np.full((2, 3), 4)        # 2 rows, 3 columns
```

### 向量化、数学函数和 axis

算术对 array 是 element-wise 的，并产生新 array：`a + 5`、`a * b`、`a ** 2`。普通 Python list 不支持 `my_list + 5`；不要为 ndarray 的逐元素算术手写循环。

| 操作 | 无 `axis` | `axis=0` | `axis=1`（对 2D array） |
|---|---|---|---|
| `np.sum(a)`、`np.mean(a)`、`np.min(a)`、`np.max(a)` | 对所有元素归约为一个 scalar | 沿 row 方向归约；每一列一个结果 | 沿 column 方向归约；每一行一个结果 |
| `np.log(a)` | 对每个元素算自然对数，shape 不变 | 不用 axis | 不用 axis |

`np.sum` 等既可写成 standalone function（推荐清楚一致地写 `np.sum(a)`），某些也有 array method。预测结果时先写 shape：例如 `(2, 3)` 上 `axis=0` 的 sum shape 是 `(3,)`，`axis=1` 是 `(2,)`。

### 数值/布尔索引与赋值

```python
a[1, 2]             # 2D：row 1、column 2 的 scalar
a[:, 0]             # 所有 rows 的第一列；shape 通常少一维
a[0, 1:3]           # row 0 的 columns 1 与 2
positive = a[a > 0] # 比较先产生同 shape 的 bool mask，再筛出 True 的值
```

- 多维索引以逗号分隔各轴：`a[row, column]`；`:` 表示该轴全取。数字 index 通常移除该轴，切片保留该轴。
- `a > 0` 是 bool array，不是一个总的 True/False；`a[a > 0]` 用它作 mask 筛选。
- mask 可用于原地替换：`a[a < 0] = np.nan`。**`a` 必须是可存 float 的 dtype**；整数 array 不能存 `np.nan`，应先转换，例如 `a = a.astype(float)`。这是改变 `a`；若 `b = a`，`b` 只是 alias，改 `b` 也会改 `a`。需要独立副本时用 `a.copy()`。
- `np.nan` 是特殊 float “not a number”；不要用 `== np.nan` 判断缺失值（NaN 不等于自身）。

### Broadcasting

NumPy 可在算术前把 size 为 1 的维度“扩展”来对齐 array；scalar 也会广播到每个元素。

```python
np.array([1, 2, 3]) + 10              # (3,) + scalar -> (3,)
np.ones((2, 3)) + np.array([1, 2, 3]) # (2, 3) + (3,) -> (2, 3)
```

从**最右侧维度**比较：两维 compatible 当且仅当长度相等，或其中一个长度是 1；缺少的前导维度可视为 1。其他组合会 `ValueError`，例如 shape `(3,)` 与 `(6,)`。先检查 `.shape`，不要把能运行的广播当成一定符合分析意图。

### 改 shape，不改数据值

| 操作 | 效果与陷阱 |
|---|---|
| `np.transpose(a)` | 调换 axes；2D 常把 rows/columns 对调，shape `(r, c)` 变 `(c, r)` |
| `np.reshape(a, new_shape)` | 用同一批元素给新 shape；元素总数必须相同；默认 row-major/C order |
| `a.flatten()` | 压为 1D 的**copy** |
| `np.ravel(a)` | 压为 1D；尽可能给 view，必要时才 copy |

`reshape((6, 2))` 不是任意裁剪/填充：原数组 `size` 必须为 12。若随后要修改扁平化结果而不影响原 array，`flatten()` 的 copy 语义更安全；若追求避免不必要 copy，要理解 `ravel()` 的 view 可能共享数据。

---

## 7. 快速读题/查错清单

1. **先标类型和 shape。** 是 scalar、list、tuple、dict、`ndarray` 还是 `None`？二维 array 的 shape 是什么？
2. **逐步执行状态变化。** 标出每次赋值、mutation、循环当前值和 `return`；不要把 `print` 当返回值。
3. **看操作是取值、复制还是原地修改。** `x = y`、`x[:]`、`.append()`、`a[mask] = ...` 的效果完全不同。
4. **对索引写出边界。** Python 是 0-based，slice stop 不含，`range(stop)` 也不含 stop；负 index 从末尾开始。
5. **对函数对照签名。** required/optional 参数是否都绑定？调用返回什么 type？是否副作用？
6. **对 NumPy 先写 shape，再算。** 特别是 `axis`、二维索引、mask 和 broadcasting。
7. **错误类型是线索。** `KeyError`（dict key）、`IndexError`（序列位置）、`TypeError`（操作/类型不匹配）、`ValueError`（值/shape 不合法）分别指向不同问题。

---

## 主要来源

- 本学期官方课程 README：学习目标、Lecture 1–8 主题和 Quiz 权重，`official/current/DSCI_511_py-prog_students/README.md`。
- 本学期官方 Lecture 1–4 notebooks：learning objectives、Python/函数/OOP/NumPy 的具体语义与例子，`official/current/DSCI_511_py-prog_students/lecture-notes/lecture1.ipynb` 至 `lecture4.ipynb`。
- 已发布的本学期练习：Worksheet 1（Python basics）、Worksheet 2（control/iterables/functions）、Lab 1（Python basics），各自 `official/current/.../worksheets/` 与 `labs/lab1/student/lab1.ipynb`。
- 当前官方 [MDS Quiz Guidelines](https://ubc-mds.github.io/resources_pages/quiz_guidelines/)：每次 quiz 50 分钟、经 PrairieLearn 交付，并说明 ORCA/PrairieTest 和 cheatsheet 的通用政策。
- 2026-09-13 查看的本学期 Canvas 与 PrairieLearn：Quiz 1 成绩项/无 Canvas quiz，及 Practice Quiz 1 与 cheatsheet 上传项的可见状态。
- `official/current/.../_quarto.yml`：课程站点目前列出 Lecture 1–5，Quiz logistics/practice chapters仍未启用。
