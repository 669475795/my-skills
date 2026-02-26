# 阿里巴巴 Java 开发手册 - 核心规范

## 命名规约

### 基本规则
- 代码中的命名严禁使用拼音与英文混合，更不允许直接使用中文
- 类名使用 UpperCamelCase 风格
- 方法名、参数名、成员变量、局部变量使用 lowerCamelCase 风格
- 常量命名全部大写，单词间用下划线隔开
- 包名统一使用小写，点分隔符之间有且仅有一个自然语义的英语单词

### POJO 类
- 布尔类型变量不要加 is 前缀，否则部分框架解析会引起序列化错误
- 包装类型 Boolean 属性不能定义为 isXxx，否则 RPC 框架可能无法识别

### Service/DAO 层
- 获取单个对象：`getXxx()`
- 获取多个对象：`listXxx()`
- 获取统计值：`countXxx()`
- 插入方法：`save/insert`（推荐 save）
- 删除方法：`remove/delete`（推荐 remove）
- 修改方法：`update()`

### 集合相关
- 不要在 foreach 循环里进行元素的 remove/add 操作

## 常量定义

### 魔法值
- 不允许任何魔法值（即未经定义的常量）直接出现在代码中
```java
// 反例
if (key.equals("Id"))

// 正例
String KEY_ID = "Id";
if (KEY_ID.equals(key))
```

### Long 类型
- Long 类型赋值必须使用大写 L，不能使用小写 l
```java
Long value = 100L; // 正确
```

## 代码格式

### 大括号
- 左大括号前不换行，后换行
- 左大括号后换行
- 右大括号前换行
- 右大括号后还有 else 等代码则不换行

### 缩进
- 采用 4 个空格缩进，禁止使用 tab 字符

### 单行长度
- 单行字符数限制不超过 120 个

### 换行
- 运算符与下文一起换行
- 方法调用的点符号与下文一起换行

## OOP 规约

### equals 方法
- 对于 Object 的 equals 方法，容易抛空指针异常，应使用常量或确定有值的对象来调用 equals
```java
// 推荐
"test".equals(object);

// 不推荐
object.equals("test");
```

### 包装类型比较
- 所有整型包装类对象之间值的比较，全部使用 equals 方法比较
- 不能用 == 比较，因为缓存范围 -128 到 127 之外的对象比较会出错

### POJO 类
- POJO 类必须写 toString 方法
- 使用 IDE 的中工具自动生成，或使用 lombok
- 如果继承了另一个 POJO 类，注意在前面加一下 super.toString()

### hashCode 和 equals
- 重写 equals 必须重写 hashCode
- Set 存储的对象、Map 的键对象必须重写这两个方法

### final 关键字
- 类内方法只能被本类的其他方法或构造方法调用，可以加 final
- 不允许被继承的类必须使用 final 关键字

## 集合处理

### 判空
- 判断所有集合是否为空，使用 isEmpty() 而不是 size() == 0

### subList
- subList 返回的是原列表的一个视图，对它的修改会影响原列表

### toArray
- 使用集合转数组的方法，必须使用集合的 toArray(T[] array)
```java
// 正例
String[] array = list.toArray(new String[0]);
```

### Arrays.asList
- Arrays.asList() 返回的是 Arrays 的内部类，不能使用修改集合相关的方法
```java
// 反例
List<String> list = Arrays.asList("a", "b");
list.add("c"); // 抛出 UnsupportedOperationException
```

### 泛型通配符
- 频繁往外读取内容的，适合用上界 Extends
- 经常往里插入的，适合用下界 Super

## 并发处理

### SimpleDateFormat
- SimpleDateFormat 是线程不安全的类，使用 DateTimeFormatter 代替
```java
// JDK 8+
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
```

### 线程池
- 线程池不允许使用 Executors 去创建，而是通过 ThreadPoolExecutor 的方式
- 避免资源耗尽风险

### 并发集合
- 使用 ConcurrentHashMap 代替 Hashtable
- 使用 CopyOnWriteArrayList 代替 Vector

### volatile
- 对于 64 位系统，不需要对 long 和 double 使用 volatile
- volatile 解决多线程内存不可见问题，但不解决原子性

### synchronized
- 对于多个资源、数据库表、对象同时加锁时，需要保持一致的加锁顺序，否则可能造成死锁

## 控制语句

### if-else
- 超过 3 层的 if-else 的逻辑判断代码可以使用卫语句、策略模式、状态模式等来实现

### switch
- switch 语句中，每个 case 要么通过 break/return 等来终止，要么注释说明程序将继续执行到哪一个 case 为止

### 循环
- 循环体内，字符串的连接方式，使用 StringBuilder 的 append 方法进行扩展
- 不要在 foreach 循环里进行元素的 remove/add 操作

## 注释规约

### 类注释
- 所有的类都必须添加创建者和创建日期

### 方法注释
- 方法内部单行注释，在被注释语句上方另起一行，使用 // 注释
- 方法内部多行注释使用 /* */ 注释，注意与代码对齐

### TODO/FIXME
- 待办事宜（TODO）标记
- 错误标记（FIXME）

### 代码修改
- 代码修改的同时，注释也要进行相应的修改

## 异常处理

### 异常分类
- 运行时异常：RuntimeException 及其子类
- 受检异常：Exception 及其子类，但不包括 RuntimeException

### 异常捕获
- 异常不要用来做流程控制，条件控制
- catch 时请分清稳定代码和非稳定代码，稳定代码指的是无论如何不会出错的代码

### 异常处理
- 有 try 块放到了事务代码中，catch 异常后，如果需要回滚事务，一定要手动回滚
- 不要在 finally 块中使用 return

### 自定义异常
- 定义时区分 unchecked / checked 异常
- 方法的返回值可以为 null，不强制返回空集合或空对象，但必须添加注释充分说明什么情况下会返回 null

## MySQL 数据库

### 表设计
- 表达是与否概念的字段，必须使用 is_xxx 的方式命名，数据类型是 unsigned tinyint（1 表示是，0 表示否）
- 表名、字段名必须使用小写字母或数字，禁止出现数字开头，禁止两个下划线中间只出现数字
- 主键索引名为 pk_字段名；唯一索引名为 uk_字段名；普通索引名则为 idx_字段名

### 字段类型
- 小数类型为 decimal，禁止使用 float 和 double
- 如果存储的字符串长度几乎相等，使用 char 定长字符串类型
- varchar 是可变长字符串，不预先分配存储空间，长度不要超过 5000

### SQL 语句
- 不要使用 count(列名) 或 count(常量) 来替代 count(*)
- 不要使用外键与级联，一切外键概念必须在应用层解决
- 禁止使用存储过程，存储过程难以调试和扩展，更没有移植性

### 索引
- 业务上具有唯一特性的字段，即使是多个字段的组合，也必须建成唯一索引
- 超过三个表禁止 join
- 在 varchar 字段上建立索引时，必须指定索引长度

## 安全规约

### SQL 注入
- 用户输入的 SQL 参数严格使用参数绑定或者 METADATA 字段值限定
- 禁止字符串拼接 SQL 访问数据库

### XSS 攻击
- 在使用平台资源时，譬如短信、邮件、电话、下单、支付，必须实现正确的防重放的机制

### HTTPS
- 敏感数据传输必须使用 HTTPS
- 用户输入的 SQL 参数严格使用参数绑定

### 权限控制
- 表单、AJAX 提交必须执行 CSRF 安全验证
- 用户敏感数据禁止直接展示，必须对展示数据进行脱敏

## 日志规约

### 日志级别
- ERROR：错误信息，影响到程序正常运行、当前请求正常运行的异常情况
- WARN：警告信息，不应该出现但是不影响程序、当前请求正常运行的异常情况
- INFO：一般性消息，强调应用程序的运行过程
- DEBUG：调试信息，最详细的信息，开发时使用
- TRACE：追踪信息，比 DEBUG 更详细

### 日志规范
- 应用中不可直接使用日志系统（Log4j、Logback）中的 API，应使用日志门面 SLF4J
- 日志文件推荐至少保存 15 天
- 异常信息应该包括两类信息：案发现场信息和异常堆栈信息

### 性能
- 输出 Exceptions 的全部 Trace 信息
- 谨慎地记录日志，避免大量输出无效日志，信息埋没
