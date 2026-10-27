import redis
import json
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0,decode_responses=True)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

# 1 - Crear registros clave-valor(0.25 puntos)
baseDatosRedis.set('libro_1','Matematicas')
baseDatosRedis.set('ordenador_1','001')
baseDatosRedis.set('libro_2','Lengua')
baseDatosRedis.set('ordenador_2','002')
baseDatosRedis.set('libro_3','Historia')
baseDatosRedis.set('ordenador_3','003')
baseDatosRedis.set('libro_4','Fisica')
baseDatosRedis.set('ordenador_4','004')

# 2 - Obtener y mostrar el número de claves registradas (0.25 puntos)
claves= baseDatosRedis.keys()
print("2. numero claves:",len(claves))

# 3 - Obtener y mostrar un registro en base a una clave (0.25 puntos)
valor_libro= baseDatosRedis.get('libro_1')
print("3. valor:",valor_libro)

# 4 - Actualizar el valor de una clave y mostrar el nuevo valor(0.25 puntos)
baseDatosRedis.set('libro_1', 'Ingles')
valor_libro= baseDatosRedis.get('libro_1')
print("4. nuevo valor:",valor_libro)

# 5 - Eliminar una clave-valor y mostrar la clave y el valor eliminado(0.25 puntos)
clave_eliminada = 'ordenador_4'
valor_eliminado = baseDatosRedis.get(clave_eliminada)
baseDatosRedis.delete(clave_eliminada)
print(f"5. Clave eliminada: {clave_eliminada}, Valor eliminado: {valor_eliminado}")

# 6 - Obtener y mostrar todas las claves guardadas (0.25 puntos)
todas_las_claves = baseDatosRedis.keys('*')
print(f"6. Todas las claves: {todas_las_claves}")

# 7 - Obtener y mostrar todos los valores guardados(0.25 puntos)
todos_los_valores = [baseDatosRedis.get(clave) for clave in todas_las_claves]
print(f"7. Todos los valores: {todos_los_valores}")

# 8 - Obtener y mostrar varios registros con una clave con un patrón en común usando * (0.5 puntos)
claves_asterisco = baseDatosRedis.keys('libro_*')
print(f"8. Claves 'libro_*': {claves_asterisco}")

# 9 - Obtener y mostrar varios registros con una clave con un patrón en común usando [] (0.5 puntos)
claves_corchetes = baseDatosRedis.keys('libro_[1-2]')
print(f"9. Claves 'libro_[1-2]': {claves_corchetes}")

# 10 - Obtener y mostrar varios registros con una clave con un patrón en común usando ? (0.5 puntos)
claves_interrogacion = baseDatosRedis.keys('ordenador_?')
print(f"10. Claves 'ordenador_?': {claves_interrogacion}")

# 11 - Obtener y mostrar varios registros y filtrarlos por un valor en concreto (0.5 puntos)
registros_filtrados = {k: baseDatosRedis.get(k) for k in baseDatosRedis.keys() if baseDatosRedis.get(k) == 'Lengua'}
print(f"11. Registros filtrados 'Lengua': {registros_filtrados}")

# 12 - Actualizar una serie de registros en base a un filtro (por ejemplo aumentar su valor en 1)(0.5 puntos)
for k in baseDatosRedis.keys('ordenador_*'):
    val_actual = int(baseDatosRedis.get(k))
    baseDatosRedis.set(k, str(val_actual + 1).zfill(3))
print("12. Valores de ordenadores incrementados:",{k: baseDatosRedis.get(k) for k in baseDatosRedis.keys('ordenador_*')},)

# 13 - Eliminar una serie de registros en base a un filtro (0.5 puntos)
for k in baseDatosRedis.keys('ordenador_*'):
    baseDatosRedis.delete(k)
print(f"13. Claves tras eliminar 'ordenador_*': {baseDatosRedis.keys()}")

# 14 - Crear una estructura en JSON de array de los datos que vayáis a almacenar (0.5 puntos)
baseDatosRedis.json().set("productos_array", "$", [])
baseDatosRedis.json().arrappend("productos_array", "$", {"id": 1, "nombre": "Portatil Asus", "categoria": "Informatica", "precio": 700})
baseDatosRedis.json().arrappend("productos_array", "$", {"id": 2, "nombre": "Impresora HP", "categoria": "Informatica", "precio": 150})
baseDatosRedis.json().arrappend("productos_array", "$", {"id": 3, "nombre": "Silla Oficina", "categoria": "Mobiliario", "precio": 120})

# 15 - Realizar un filtro por cada atributo de la estructura JSON anterior (0.5 puntos)
res_id = baseDatosRedis.json().get("productos_array", "$[?(@.id==1)]")
res_nombre = baseDatosRedis.json().get("productos_array", "$[?(@.nombre=='Impresora HP')]")
res_cat = baseDatosRedis.json().get("productos_array", "$[?(@.categoria=='Informatica')]")
res_precio = baseDatosRedis.json().get("productos_array", "$[?(@.precio>200)]")

print(f"15. Filtro JSON ID=1: {res_id}")
print(f"15. Filtro JSON Nombre='Impresora HP': {res_nombre}")
print(f"15. Filtro JSON Categoria='Informatica': {res_cat}")
print(f"15. Filtro JSON Precio>200: {res_precio}")

# 16 - Crear una lista en Redis (0.25 puntos)
baseDatosRedis.rpush('tareas', 'revisar_inventario', 'comprar_papel', 'revisar_inventario', 'mantenimiento')
print(f"16. Elementos en lista 'tareas': {baseDatosRedis.lrange('tareas', 0, -1)}")

# 17 - Obtener elementos de una lista con un filtro en concreto (0.5 puntos)
todas_las_tareas = baseDatosRedis.lrange('tareas', 0, -1)
tareas_filtradas = [t for t in todas_las_tareas if 'revisar' in t]
print(f"17. Tareas filtradas con patrón 'revisar': {tareas_filtradas}")

# 18 - Crea datos con índices, definiendo un esquema de al menos tres campos (0.5 puntos)
esquema = (
    TextField("$.nombre", as_name="nombre"),
    TagField("$.ciudad", as_name="ciudad"),
    NumericField("$.edad", as_name="edad")
)

# Creación del índice.
try:
    baseDatosRedis.ft("indice:usuarios").create_index(
        esquema,
        definition=IndexDefinition(prefix=["usuarios:"], index_type=IndexType.JSON)
    )
except Exception:
    pass

# Inserción usuarios formato JSON
u1 = {"nombre": "Jorge Baron", "email": "jorge.baron@example.com", "edad": 38, "ciudad": "Spain"}
u2 = {"nombre": "Elena Gomez", "email": "elena.gomez@example.com", "edad": 29, "ciudad": "Mexico"}
u3 = {"nombre": "Pepe Garcia", "email": "pepe.garcia@example.com", "edad": 33, "ciudad": "Spain"}
baseDatosRedis.json().set("usuarios:1", Path.root_path(), u1)
baseDatosRedis.json().set("usuarios:2", Path.root_path(), u2)
baseDatosRedis.json().set("usuarios:3", Path.root_path(), u3)

# 19 - Realiza una búsqueda con índices en base a un campo (0.5 puntos)
resultados = baseDatosRedis.ft("indice:usuarios").search(Query("@ciudad:{Spain} @edad:[30 40]"))
print(f"19. Resultados búsqueda por índice: {resultados.docs}")

# 20 - Realiza un group by usando los índices (0.5 puntos)
groupby = aggregations.AggregateRequest("*").group_by('@ciudad', reducers.count().alias('count'))
resultado_group = baseDatosRedis.ft("indice:usuarios").aggregate(groupby).rows
print(f"20. Group By por ciudad: {resultado_group}")

conexionRedis.close()