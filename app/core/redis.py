from redis.asyncio import Redis , ConnectionPool

def get_redis(host : str ,max_connections : int = 10,port :int =6379):
    try :
        pool = ConnectionPool(host=host, port=port, max_connections=max_connections)
        redis =  Redis(connection_pool=pool)
        if redis.ping():
            return redis
        raise ConnectionError("Failed to connect Redis")
    
    except Exception as e :
        print("Failed to connect Redis")
        raise e



