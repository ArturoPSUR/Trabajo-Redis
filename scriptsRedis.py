import redis
import json

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
datos_json = [
    {"id": 1, "nombre": "Portátil Asus", "categoria": "Informática", "precio": 700},
    {"id": 2, "nombre": "Impresora HP", "categoria": "Informática", "precio": 150},
    {"id": 3, "nombre": "Silla Oficina", "categoria": "Mobiliario", "precio": 120},
]
baseDatosRedis.set('inventario_json', json.dumps(datos_json))

# 15 - Realizar un filtro por cada atributo de la estructura JSON anterior (0.5 puntos)
inventario = json.loads(baseDatosRedis.get('inventario_json'))

filtro_id = [item for item in inventario if item['id'] == 1]
filtro_nombre = [item for item in inventario if 'HP' in item['nombre']]
filtro_categoria = [item for item in inventario if item['categoria'] == 'Informática']
filtro_precio = [item for item in inventario if item['precio'] > 200]

print(f"15. Filtro ID=1: {filtro_id}")
print(f"15. Filtro Nombre='HP': {filtro_nombre}")
print(f"15. Filtro Categoria='Informática': {filtro_categoria}")
print(f"15. Filtro Precio > 200: {filtro_precio}")

# 16 - Crear una lista en Redis (0.25 puntos)
baseDatosRedis.rpush('tareas', 'revisar_inventario', 'comprar_papel', 'revisar_inventario', 'mantenimiento')
print(f"16. Elementos en lista 'tareas': {baseDatosRedis.lrange('tareas', 0, -1)}")

#----------------------------------

# 17 - Obtener elementos de una lista con un filtro en concreto (0.5 puntos)
todas_las_tareas = baseDatosRedis.lrange('tareas', 0, -1)
tareas_filtradas = [t for t in todas_las_tareas if 'revisar' in t]
print(f"17. Tareas filtradas con patrón 'revisar': {tareas_filtradas}")

# 18 - Crea datos con índices, definiendo un esquema de al menos tres campos (0.5 puntos)
# Mediante Hashes y Sets auxiliares (índices invertidos)
dispositivos = [
    {
        'id': 'disp:1',
        'marca': 'Dell',
        'tipo': 'Sobremesa',
        'aula': '101',
        'estado': 'Activo',
    },
    {
        'id': 'disp:2',
        'marca': 'HP',
        'tipo': 'Portátil',
        'aula': '101',
        'estado': 'Inactivo',
    },
    {
        'id': 'disp:3',
        'marca': 'Dell',
        'tipo': 'Portátil',
        'aula': '102',
        'estado': 'Activo',
    },
]

for d in dispositivos:
    # Guardar entidad en Hash
    baseDatosRedis.hset(d['id'], mapping=d)
    # Crear índices
    baseDatosRedis.sadd(f"idx:marca:{d['marca']}", d['id'])
    baseDatosRedis.sadd(f"idx:aula:{d['aula']}", d['id'])
    baseDatosRedis.sadd(f"idx:estado:{d['estado']}", d['id'])

print("18. Datos y sus índices creados correctamente.")

# 19 - Realiza una búsqueda con índices en base a un campo (0.5 puntos)
# Buscar todos los dispositivos de la marca 'Dell'
ids_dell = baseDatosRedis.smembers('idx:marca:Dell')
resultados_dell = [baseDatosRedis.hgetall(doc_id) for doc_id in ids_dell]
print(f"19. Búsqueda por índice (Marca = Dell): {resultados_dell}")

# 20 - Realiza un group by usando los índices (0.5 puntos)
# Agrupar los dispositivos por su 'aula'
aulas = ['101', '102']
group_by_aula = {}

for aula in aulas:
    ids_en_aula = baseDatosRedis.smembers(f"idx:aula:{aula}")
    group_by_aula[aula] = [
        baseDatosRedis.hgetall(doc_id) for doc_id in ids_en_aula
    ]

print(f"20. Group By por Campo 'aula': {group_by_aula}")

conexionRedis.close()