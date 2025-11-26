import socket
import time

#CONEXIÓN AL ROBOT POR TCP-IP
def connect ():
    HOST = '192.168.64.100'
    PORT = 29999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s
def sendData(client, message):
    client.sendall(message.encode('utf-8'))
    data = client.recv(1024)
    return data.decode('utf-8')

robot = connect()

#FUNCIONES PREFABRICADAS
def clearError():
    sendData(robot, 'EmergencyStop(0)')
    sendData(robot, 'ClearError()')
    enableRobot()
def enableRobot():
    sendData(robot, 'PowerOn()')
    sendData(robot, 'EnableRobot(0.2,0,0,80)')
def disableRobot():sendData(robot, 'DisableRobot()')
def useTool():sendData(robot, 'ToolDO(1,1)') #Falta checar el sensor para cuando agarra algo
def notUseTool():sendData(robot, 'ToolDO(1,0)')
# def posicionDefault(): sendData(robot, 'MovJ(pose={225.80,-49,258.62,-180, 0, -90})') # NO OPERATIVA
def emergencyStop(): sendData(robot, 'EmergencyStop(1)')
def posicionHome(): sendData(robot, 'MovJ(pose={250,-50,362,-178, 0, 100})')
def getPositions():
    angles = sendData(robot, 'GetAngle()')
    inicio = angles.index('{')
    fin = angles.index('}') + 1
    res = angles[inicio:fin]
    return [float(x) for x in res.strip("{}").split(",")]
def getToolStatus():
    res = (sendData(robot, 'GetToolDO(1)')).split(',')[1]
    if res == '{1}': print("ON")
    elif res == '{0}': print("OFF")

# Funciones de Movimiento: Los parámetros que reciben son prácticamente la misma ubicación
# solo que la coordenada2 está en un punto más alto para hacer un efecto de descenso
def movimientoRecoger(coordenada1, coordenada2):
    sendData(robot, f"MovJ(pose={coordenada2})")
    sendData(robot, 'VelL(20)')
    time.sleep(2)
    sendData(robot, f"MovL(pose={coordenada1})")
    useTool()
    time.sleep(3)
    sendData(robot, f"MovL(pose={coordenada2})")
    time.sleep(3)
    sendData(robot, 'VelL(100)')

# Similar al anterior, solo que aquí la coordenada1 está más arriba

def movimientoDejar(coordenada1, coordenada2):
    sendData(robot, f"MovJ(pose={coordenada1})")
    time.sleep(2)
    sendData(robot, 'VelL(20)')
    sendData(robot, f"MovL(pose={coordenada2})")
    notUseTool()
    time.sleep(3)
    sendData(robot, f"MovL(pose={coordenada1})")
    sendData(robot, 'VelL(100)')

# Función de ejemplo para probar movimientos y agarre

def secuenciaMovimientos():
    #mov1
    posicionHome()
    time.sleep(2)
    movimientoRecoger('{244.5275,225.6371,97,-177.5596,0,90}', '{244.5275,225.6371,170,-177.5596,0,147.4555}')
    time.sleep(1)
    movimientoDejar('{297.1595, 223.6479, 170, -179.0744, 0, 127.3484}','{297.1595, 223.6479, 97.8921, -179.0744, 0, 90}')
    posicionHome()
    time.sleep(10)
    #mov2
    movimientoRecoger('{297.1595, 223.6479, 96.8921, -179.0744, 0, 90}', '{297.1595, 223.6479, 160, -179.0744, 0, 127.3484}')
    time.sleep(1)
    movimientoDejar('{244.5275,225.6371,160,-177.5596,0,147.4555}', '{244.5275,225.6371,97,-177.5596,0,90}')
    posicionHome()
# Método donde se llaman las funciones
if __name__ == '__main__':
    #notUseTool()
    clearError()
    #enableRobot()
    disableRobot()
    posicionHome()
    secuenciaMovimientos()
    ## Esta parte muestra los ángulos en los que se encuentran los joints en el formato: {J1,J2,J3,J4,J5,J6}
    positionsList = getPositions()
    print(positionsList)
    ##
    getToolStatus()
    robot.close()
