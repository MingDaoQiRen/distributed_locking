import redis
import logging
from math import ceil

__all__ = ["RedisConn"]


class RedisConn:
    local_host = "localhost"
    default_port = 6379
    default_db = 0

    lock_value = "parsing_lock"
    lock_key_format = "id:{}"

    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
            pool = self.create_local_pool()
        else:
            pool = self.create_pool(*args, decode_responses=True, **kwargs)
        self.conn = redis.Redis(connection_pool=pool)

    @staticmethod
    def create_local_pool() -> redis.ConnectionPool:
        """
        create_local_pool will create a local redis connection pool
        """
        pool = redis.ConnectionPool(
            host=RedisConn.local_host,
            port=RedisConn.default_port,
            db=RedisConn.default_db,
            decode_responses=True
        )
        return pool

    @staticmethod
    def create_pool(*args, **kwargs) -> redis.ConnectionPool:
        """
        create_pool will create a redis connection pool
        """
        pool = redis.ConnectionPool(*args, **kwargs)
        return pool

    def acquire_lock(self, lock_key) -> bool:
        """
        acquire_lock will acquire a lock. If the value of the key has not been
        set, set a lock and return True,else return False
        """
        lock_key_f = self.format_key(lock_key)
        try:
            res = self.conn.setnx(lock_key_f, RedisConn.lock_value)
            print(res)
            return res
        except Exception as ex:
            logging.error(ex, extra={"lock_key": lock_key})

    def acquire_lock_with_timeout(self, lock_key, lock_timeout=60) -> bool:
        """
        acquire_lock_with_timeout will acquire a lock. If the value of the key
        has not been set(maybe it's deleted by sever at expire time), set a
        lock and return True,else return False
        """
        # 未启用
        lock_key_f = self.format_key(lock_key)
        lock_timeout = int(ceil(lock_timeout))
        try:
            res = self.conn.setnx(lock_key_f, RedisConn.lock_value)
            if res:
                self.conn.expire(lock_key_f, lock_timeout)
            return res
        except Exception as ex:
            logging.error(ex, extra={"lock_key": lock_key})

    def release_lock(self, lock_key):
        """
        release_lock will delete the lock_key
        """
        lock_key_f = self.format_key(lock_key)
        pipe = self.conn.pipeline(True)
        # TODO:以后可能会加带timeout的锁,到时候的release不能使用死循环
        while True:
            try:
                pipe.watch(lock_key_f)
                if pipe.get(lock_key_f) == RedisConn.lock_value:
                    pipe.multi()
                    pipe.delete(lock_key_f)
                    pipe.execute()
                pipe.unwatch()
                return
            except redis.exceptions.WatchError:
                pass
            except Exception as ex:
                logging.error(ex, extra={"lock_key": lock_key})

    def release_lock_if_set_timeout(self):
        ...
        # 暂未启用

    @staticmethod
    def format_key(key) -> str:
        """
        format_key will format the lock_key
        """
        return RedisConn.lock_key_format.format(key)


if __name__ == '__main__':
    conn = RedisConn()
    conn.acquire_lock(10086)
    conn.release_lock(10086)
