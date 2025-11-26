# Control del DOBOT Magician E6 mediante Sockets TCP/IP

Este repositorio contiene un script en Python diseñado para controlar el **DOBOT Magician E6** utilizando comunicación **TCP/IP por socket**.  
Permite enviar comandos al robot, mover sus ejes, controlar la herramienta (pinza/ventosa), consultar estados y realizar secuencias completas de pick & place.

Archivo principal: robotScript.py

Este script permite:

- Conectarse al controlador del robot mediante sockets.
- Enviar comandos nativos del DOBOT E6 (MovJ, MovL, PowerOn, ToolDO…).
- Activar / desactivar la herramienta del efector final.
- Obtener ángulos actuales de las articulaciones.
- Ejecutar secuencias de movimiento automatizadas.
- Implementar rutinas de recogida y colocación.

---

# Conexión con el robot

### `connect()`
Establece una conexión TCP/IP con el robot.

- **HOST:** `192.168.64.100`
- **PORT:** `29999`

Devuelve un objeto `socket` conectado al controlador.

### `sendData(client, message)`
Envía un comando al robot y recibe su respuesta.

- Convierte el mensaje a UTF-8.
- Envía la cadena completa.
- Recibe respuesta de hasta 1024 bytes.
- Retorna la respuesta decodificada.

---

# Funciones generales de control

### `clearError()`
Limpia errores activos del robot.

1. Envía `EmergencyStop(0)` para desactivar el paro.
2. Envía `ClearError()` para limpiar fallas.
3. Llama automáticamente a `enableRobot()`.

---

### `enableRobot()`
Activa el robot:

1. `PowerOn()` alimenta los motores.
2. `EnableRobot(0.2,0,0,80)` habilita el brazo con los parámetros de operación.

---

### `disableRobot()`
Deshabilita el robot sin apagarlo completamente.

---

### `useTool()`
Activa la herramienta en el canal digital 1:  
`ToolDO(1,1)` → cierra pinza/activa ventosa.

### `notUseTool()`
Desactiva la herramienta:  
`ToolDO(1,0)` → abre pinza/desactiva ventosa.

---

### `emergencyStop()`
Ejecuta un paro de emergencia inmediato con `EmergencyStop(1)`.

---

### `posicionHome()`
Envía al robot a una posición de referencia mediante:

MovJ(pose={250,-50,362,-178,0,100})


Movimiento rápido articular (joint move).

---

# Funciones de consulta

### `getPositions()`
Obtiene los ángulos de las juntas mediante `GetAngle()`.

La función:

- Extrae el bloque `{J1,J2,J3,J4,J5,J6}`.
- Convierte cada valor a `float`.
- Retorna una lista de 6 elementos.

Ejemplo:

[10.4, -30.2, 45.0, -90.0, 12.3, 0.0]


---

### `getToolStatus()`
Consulta el estado de la herramienta con `GetToolDO(1)`:

- `{1}` → herramienta activa (ON)
- `{0}` → herramienta inactiva (OFF)

Imprime el estado en consola.

---

# 🤖 Funciones de movimiento

Estas funciones utilizan dos poses:

- `coordenada1`: punto bajo (recoger/dejar).
- `coordenada2`: punto alto (trayectoria segura).

---

## `movimientoRecoger(coordenada1, coordenada2)`
Realiza la secuencia completa de **recoger** un objeto:

1. `MovJ` hacia el punto alto.
2. Reduce velocidad lineal con `VelL(20)`.
3. Desciende en línea recta (`MovL`) al punto bajo.
4. Activa la herramienta con `useTool()`.
5. Asciende nuevamente al punto alto.
6. Restaura velocidad (`VelL(100)`).

---

## `movimientoDejar(coordenada1, coordenada2)`
Realiza la secuencia de **dejar** un objeto:

1. `MovJ` al punto alto.
2. Baja la velocidad (`VelL(20)`).
3. Desciende con `MovL` al punto bajo.
4. Desactiva la herramienta (`notUseTool()`).
5. Sube al punto alto.
6. Restaura velocidad.

---

# `secuenciaMovimientos()`
Ejemplo completo que combina:

- Posición home.
- Movimiento de recogida.
- Movimiento de colocación.
- Repetición con posiciones invertidas.

Incluye pausas para garantizar estabilidad mecánica.

---

# Ejecución principal

El bloque `__main__` realiza:

1. `clearError()`
2. `disableRobot()`
3. `posicionHome()`
4. `secuenciaMovimientos()`
5. Imprime la lista de ángulos (`getPositions()`).
6. Imprime estado de herramienta (`getToolStatus()`).
7. Cierra la conexión.

---

# Ejemplo básico de uso

```python
from robotScript import connect, sendData, posicionHome

robot = connect()
sendData(robot, "PowerOn()")
posicionHome()
robot.close()
