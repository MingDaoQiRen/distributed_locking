# distributed_locking

## 使用redis构建分布式锁
参考:https://redislabs.com/ebook/part-2-core-concepts/chapter-6-application-components-in-redis/6-2-distributed-locking)

## 项目运行相关

项目提供了 `virtualenv` 相关的配置支持，具体配置可以参考 `Makefile`

1. 新建 `virtualenv` 环境，并启用
   ```bash
   make env
   source venv/bin/activate
   ```
   
2. 安装依赖
   ```bash
   make deps
   ```

3. 使用
    ```python
    from distributed_locking.redis_lock.lock import RedisConn

    conn = RedisConn()
    conn.acquire_lock(10086)
    # do something
    conn.release_lock(10086)
    ```