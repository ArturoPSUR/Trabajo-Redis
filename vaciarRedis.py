import redis

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
r = redis.Redis(connection_pool=conexionRedis)

r.flushdb()
print("Base de datos de Redis eliminada (flushdb ejecutado con éxito).")

conexionRedis.close()