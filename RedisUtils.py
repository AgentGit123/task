"""
    describe: redis操作类
    Author:   zyc
    Date:     2023-9-8
    Usage:

    redisUtils = RedisUtils(host, port, password, db, decode_responsese)

    # 从右边插入列表数据
    redisUtils.list_push('list_test', 'r', '张三', '李四', '王五')
    # 修改指定索引的元素
    redisUtils.list_set('list_test', 2, '赵云')
    # 查看列表
    redisUtils.list_get('list_test', 0, -1)
    #删除指定数据
    redisUtils.list_pop('list_test', 0,'','c')

    # 设置string字符串数据
    redisUtils.string_set('string_test', 'zyc')
    # 查看字符串数据
    redisUtils.string_get('string_test')
    # 删除字符串数据
    redisUtils.any_delete('string_test')

    # 添加Hash键值对
    redisUtils.hash_hset('hash_test', 'name', 'zyc')
    redisUtils.hash_hset('hash_test', 'age', '22')
    # 查看Hash中key对应的value
    redisUtils.hash_hget('hash_test', 'name')
    # 修改Hash中key对应的value
    redisUtils.hash_hset('hash_test', 'name', 'zyc123')
    # 删除Hash中的键值对
    redisUtils.hash_hdel('hash_test', 'age')

    # 添加Set元素
    redisUtils.set_sadd('set_test', 'zyc', '22', 'fjnu')
    # 查看Set所有元素
    redisUtils.set_smembers('set_test')
    # 删除Set中元素
    redisUtils.set_srem('set_test', '22')

    # host == 连接的redis服务器的ip地址
    # port == redis的端口号,默认为6379
    # password == 进入redis数据库的密码
    # db == 选择对哪个数据库进行操作
    # decode_reponses == redis取出的结果是否为字符串类型,通常设置为True
"""

import redis

# RedisUtils 操作工具类
class RedisUtils:

    def __init__(self, host, port , password, db, decode_responses):
        self.__conn = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=decode_responses
        )

    '''
        list相关操作方法
    '''
    # 创建或者增加列表数据的操作 rpush, lpush
    def list_push(self, key, push_var, *value):
        if push_var == 'r':
            self.__conn.rpush(key, *value)
        elif push_var == 'l':
            self.__conn.lpush(key, *value)

    # 删除列表数据的操作 lpop, rpop, lrem指定删除 num=0 代表删除全部
    def list_pop(self, key, num, value, pop_var):
        if pop_var == 'r':
            # 从右边删除
            self.__conn.rpop(key)
        elif pop_var == 'l':
            # 从左边删除
            self.__conn.lpop(key)
        elif pop_var == 'c':
            # 指定删除元素
            self.__conn.lrem(key, num, value)

    # 修改所在索引的元素：lset key index value
    def list_set(self, key, index, value):
        self.__conn.lset(key, index, value)

    # 查看列表元素所在的索引：lrange
    def list_get(self, key, start_index, end_index):
        print(self.__conn.lrange(key, start_index, end_index))

    '''
        string相关操作方法
    '''
    # 创建或者修改字符串数据的操作 set
    def string_set(self, key, value):
        self.__conn.set(key, value)

    # 查询字符串数据的操作 get
    def string_get(self, key):
        print(self.__conn.get(key))

    '''
        Hash相关操作方法
    '''
    # 哈希中添加或修改一个键值对 hset
    def hash_hset(self, name, key, value):
        self.__conn.hset(name, key ,value)

    # 哈希中删除键值对 hdel
    def hash_hdel(self, name, *keys):
        self.__conn.hdel(name, *keys)

    # 获取Hash中指定key的值 hget
    def hash_hget(self, name, key):
        print(self.__conn.hget(name, key))

    '''
        Set集合相关操作方法
    '''
    #集合中添加一个元素 sadd
    def set_sadd(self, name, *values):
        self.__conn.sadd(name, *values)

    #集合中删除一个或多个元素 srem
    def set_srem(self, name, *values):
        self.__conn.srem(name, *values)

    #查询集合中的所有元素 smembers
    def set_smembers(self, name):
        print(self.__conn.smembers(name))

    '''
        其它常用操作方法
    '''
    #删除redis中任意数据类型 delete
    def any_delete(self, *names):
        self.__conn.delete(*names)