1.Integridad (Módulo 5075): una tabla comparativa con el hash original, el hash limpio, nº de filas antes y después, y filas eliminadas por cada causa. Añade una frase sobre por qué cambia el hash.
SHA-256 original : 317f5047ddc0407b36fe4b8af54b919e5a2f815555c5c1b0c176cff4e0df0181
Coincide con referencia: False

Filas iniciales: 300
id_envio             0
id_vehiculo          0
timestamp_lectura    0
origen               0
destino              1
peso_kg              1
temp_celsius         1
latitud              0
longitud             0
estado_envio         0
dtype: int64

Duplicados eliminados: 2
Filas con nulos eliminadas: 3
Pesos no positivos eliminados: 1
Temperaturas fuera de rango eliminadas: 1
Estados no catalogados eliminados: 1

Filas finales: 292
SHA-256 limpio   : d629f756a673c146bfa2842ab7d3345cbfbb202717284a2034937f94e6a5b514

2.Despliegue y HDFS (Módulo 5074): cómo verificaste el contenedor, los puertos mapeados (9870 y 8088), los volúmenes y cada comando HDFS con su propósito.
La imagen apache/hadoop:3.4.0 incluye únicamente el JRE, por lo que la herramienta jps (propia del JDK) no está disponible (bash: jps: command not found). La verificación se realizó con ps -ef, que lista los mismos procesos Java. Se confirman los cuatro daemons activos: NameNode (PID 149), DataNode (PID 266), ResourceManager (PID 382) y NodeManager (PID 473).

3.Análisis crítico (2-3 párrafos): “¿Por qué un fichero en HDFS no se corrompe ni se pierde aunque falle un DataNode?”
La principal razón por la que no se pierden datos es por el factor de replicacion ya que guarda 3 copias de cada bloque en diferentes DataNodes, además de la concienciacion de racks ya que hdfs no distribuye replicas de manera aleatoria sino una local, otra remoto y otra en otro nodo del mismo rack. El monitoreo constante permite detectar al instante la perdida de un datanode, permitiendo suplirla con una de las replicaas y mandando a clonar esos bloques para cumplir conel factor de replicación. En caso de corrupcion se detecta rapidamente con checksums por bloque, que descarta la corrupcion e igual que cuando hay una perdida de bloque utiliza una replica y manda a replicarla.

4.Evidencias gráficas: las cuatro imágenes incrustadas (evidencias/*).