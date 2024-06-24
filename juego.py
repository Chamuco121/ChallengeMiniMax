import pygame
import numpy as np
import random

# Dimensiones del tablero
TAMAÑO_TABLERO = 8
TAMAÑO_CELDA = 60
ANCHO_VENTANA = TAMAÑO_TABLERO * TAMAÑO_CELDA
ALTO_VENTANA = TAMAÑO_TABLERO * TAMAÑO_CELDA

# Colores
COLOR_FONDO = ('royalblue')
COLOR_LINEA = (0, 0, 0)

# Inicializamos el tablero
tablero = np.zeros((TAMAÑO_TABLERO, TAMAÑO_TABLERO))

# Posiciones iniciales
gato_pos = (0, 0)
raton_pos = (4, 4)

# Definir las posiciones iniciales en el tablero
tablero[gato_pos] = 1  # 1 representa al Gato
tablero[raton_pos] = 2  # 2 representa al Raton

# Para evitar pos_movimientos repetidos
movimientos_previos = set()

# Generar destino para el ratón
def generar_destino(raton_pos, min_distancia):
# Generar una posición aleatoria para el destino del ratón que esté a una distancia mínima de la posición actual del ratón.
    while True:
# Genera una posición aleatoria dentro del tablero
        destino = (random.randint(0, TAMAÑO_TABLERO - 1), random.randint(0, TAMAÑO_TABLERO - 1))
# Calcula la distancia de Manhattan entre la posición actual del raton y el destino generado:
# Calcula y suma la diferencia absoluta entre las coordenadas del destino y la posición actual del ratón. 
        distancia = np.sum(np.abs(np.array(destino) - np.array(raton_pos)))
# Verifica si la distancia calculada es mayor o igual a la distancia mínima especificada       
        if distancia >= min_distancia:
# La función devuelve la posición generada como destino válido.           
            return destino

# La posición actual del ratón y una distancia mínima de 4.
destino = generar_destino(raton_pos, 4)

# La posición actual y nueva del jugador en el tablero, representada como una tupla   
def mover_jugador(tablero, posicion_actual, nueva_posicion):
#Verifica que la fila/columna de la nueva posición esté dentro de los límites del tablero    
    if (0 <= nueva_posicion[0] < TAMAÑO_TABLERO) and (0 <= nueva_posicion[1] < TAMAÑO_TABLERO):
# Guarda el valor del jugador en la posición actual       
        jugador = tablero[posicion_actual]
# Vacía la posición actual del jugador en el tablero, estableciendo su valor a 0       
        tablero[posicion_actual] = 0
# Mueve el jugador a la nueva posición en el tablero, asignando el valor guardado en personaje a la nueva posición.        
        tablero[nueva_posicion] = jugador
# Indica que el movimiento fue exitoso y el personaje está ahora en la nueva posición.
        return nueva_posicion
    else:
# Devuelve la posición actual del personaje. Esto indica que el movimiento no se realizó porque la nueva posición no era válida.

        return posicion_actual

def evaluar(tablero):
# Se utiliza para encontrar todas las posiciones en la matriz 
# La función np.argwhere devuelve un array con las coordenadas de todas las celdas que contienen el valor 1 (gato)    
    gato_pos = np.argwhere(tablero == 1)
# La función np.argwhere devuelve un array con las coordenadas de todas las celdas que contienen el valor 2 (raton)
    raton_pos = np.argwhere(tablero == 2)
# Verifica si alguna de las posiciones no existe en el tablero    
    if gato_pos.size == 0 or raton_pos.size == 0:
# Si alguna de las posiciones no existe, devuelve 0. Juego ha terminado
        return 0

# Toma la primera posición del gato encontrada.
    gato_pos = gato_pos[0]
# Toma la primera posición del ratón encontrada.
    raton_pos = raton_pos[0]
# Suma diferencias absolutas y Calcula la distancia entre el gato y el raton
    distancia = np.sum(np.abs(gato_pos - raton_pos)) 
# El gato quiere minimizar la distancia del raton    
    return -distancia  

# Si alguna posicion no existe =0. Si ambas existen devuelve negativo de la distancia entre ellos 
# Un puntaje mas bajo es favorable para el gato
 
def minimax(tablero, profundidad, maximizando, movimientos_previos):
# Comprueba que se ha alcanzado la profundidad maxima de recursion o el juego ha terminado 
# Limita la cantidad de recursiones y tiempo de calculo    
    if profundidad == 0 or juego_terminado(tablero): 
# Si se cumple, se evalua y devuelve el puntaje del estado actual del juego
        return evaluar(tablero)

# Comprueba si el jugador actual es el ratón, que busca maximizar su puntaje.    
    if maximizando:
# Inicializa el mejor puntaje con un valor muy bajo (-infinito) porque el ratón busca maximizar el puntaje
        mejor_valor = -np.inf
# Genera todos los pos_movimientos posibles para el ratón desde el estado actual del tablero
        pos_movimientos = generar_movimientos(tablero, 1, movimientos_previos)
#  Itera sobre todos los posibles pos_movimientos del ratón
        for movimiento in pos_movimientos:
# Llama recursivamente a minimax para evaluar el nuevo estado del tablero después de realizar el movimiento. La profundidad se reduce en 1, y el siguiente jugador es el gato (por eso False)
            valor = minimax(movimiento, profundidad - 1, False, movimientos_previos)
# Actualiza el mejor puntaje con el mayor valor entre el puntaje actual y el puntaje del nuevo estado del tablero
            mejor_valor = max(mejor_valor, valor)
# Devuelve el mejor puntaje encontrado para el ratón.
        return mejor_valor
    else:
# Inicializa el mejor puntaje con un valor muy alto (infinito) porque el gato busca minimizar el puntaje
        mejor_valor = np.inf
# Genera todos los pos_movimientos posibles para el gato desde el estado actual del tablero
        pos_movimientos = generar_movimientos(tablero, 2, movimientos_previos)
# Itera sobre todos los posibles pos_movimientos del gato
        for movimiento in pos_movimientos:
# Llama recursivamente a minimax para evaluar el nuevo estado del tablero después de realizar el movimiento. La profundidad se reduce en 1, y el siguiente jugador es el ratón (por eso True)
            valor = minimax(movimiento, profundidad - 1, True, movimientos_previos)
# Actualiza el mejor puntaje con el menor valor entre el puntaje actual y el puntaje del nuevo estado del tablero
            mejor_valor = min(mejor_valor, valor)
# Devuelve el mejor puntaje encontrado para el gato
        return mejor_valor

def generar_movimientos(tablero, jugador, movimientos_previos):
# Inicializa una lista vacía para almacenar los pos_movimientos posibles
    pos_movimientos = []
# Encuentra la posición actual del jugador en el tablero. np.argwhere devuelve las coordenadas donde el jugador se encuentra en la matriz.
    posicion_actual = np.argwhere(tablero == jugador)
# Comprueba si el personaje no se encuentra en el tablero. Esto puede suceder si el personaje ha sido removido
    if posicion_actual.size == 0:
# Si el personaje no está en el tablero, retorna la lista vacía de pos_movimientos posibles
        return pos_movimientos

    posicion_actual = posicion_actual[0]
# Selecciona la primera (y única) posición del personaje
    posibles_movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
# Define las direcciones de movimiento posibles (derecha, izquierda, abajo, arriba) como tuplas de coordenadas   
    for movimiento in posibles_movimientos:
# Itera sobre cada dirección de movimiento
        nueva_posicion = (posicion_actual[0] + movimiento[0], posicion_actual[1] + movimiento[1])
# Calcula la nueva posición del personaje sumando posibles movimiento a la posición actual
        if (0 <= nueva_posicion[0] < TAMAÑO_TABLERO) and (0 <= nueva_posicion[1] < TAMAÑO_TABLERO):
# Crea una copia de la matriz del tablero para no modificar el estado actual del juego
            nuevo_tablero = tablero.copy()
# Vacia la celda de la posición actual del personaje en la copia del tablero
            nuevo_tablero[posicion_actual[0], posicion_actual[1]] = 0
# Coloca al personaje en la nueva posición en la copia del tablero
            nuevo_tablero[nueva_posicion[0], nueva_posicion[1]] = jugador
#Comprueba si la nueva matriz del tablero no está en el historial de pos_movimientos (para evitar pos_movimientos repetidos)           
            if tuple(map(tuple, nuevo_tablero)) not in movimientos_previos:
#Si la nueva matriz del tablero no está en el historial de pos_movimientos, la agrega a la lista de pos_movimientos posibles                
                pos_movimientos.append(nuevo_tablero)
#Devuelve la lista de todas las posibles matrices de estados del tablero después de mover al personaje en cada dirección válida
    return pos_movimientos

def generar_movimientos_raton(tablero, raton_pos, movimientos_previos):
# Inicializa una lista vacía para almacenar los pos_movimientos posibles del ratón
    pos_movimientos = []
# Define las direcciones de movimiento posibles (derecha, izquierda, abajo, arriba) como tuplas de coordenadas
    posibles_movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
# Itera sobre cada dirección de movimiento   
    for movimiento in posibles_movimientos:
# Calcula la nueva posición del ratón sumando la dirección de movimiento a la posición actual
        nueva_posicion = (raton_pos[0] + movimiento[0], raton_pos[1] + movimiento[1])
# Comprueba si la nueva posición está dentro de los límites del tablero
        if (0 <= nueva_posicion[0] < TAMAÑO_TABLERO) and (0 <= nueva_posicion[1] < TAMAÑO_TABLERO):
# Crea una copia de la matriz del tablero para no modificar el estado actual del juego
            nuevo_tablero = tablero.copy()
# Vacía la celda de la posición actual del ratón en la copia del tablero
            nuevo_tablero[raton_pos[0], raton_pos[1]] = 0
# Coloca al ratón en la nueva posición en la copia del tablero
            nuevo_tablero[nueva_posicion[0], nueva_posicion[1]] = 2
# Comprueba si la nueva matriz del tablero no está en el historial de pos_movimientos (para evitar pos_movimientos repetidos)
            if tuple(map(tuple, nuevo_tablero)) not in movimientos_previos:
# Si la nueva matriz del tablero no está en el historial de pos_movimientos, la agrega a la lista de pos_movimientos posibles junto con la nueva posición
                pos_movimientos.append((nuevo_tablero, nueva_posicion))
# Ordenar pos_movimientos por la distancia al destino
    pos_movimientos.sort(key=lambda x: np.sum(np.abs(np.array(x[1]) - np.array(destino))))
# Devuelve la lista de todos los pos_movimientos válidos posibles del ratón, ordenados por la distancia al destino
    return pos_movimientos

def juego_terminado(tablero):
# Para encontrar las coordenadas de la celda donde está ubicado el gato. Esto devuelve un array con las coordenadas
    gato_pos = np.argwhere(tablero == 1)
# Para encontrar las coordenadas de la celda donde está ubicado el raton. Esto devuelve un array con las coordenadas.
    raton_pos = np.argwhere(tablero == 2)
# Verifica si el array de posiciones del gato o el array de posiciones del ratón están vacíos (lo que significa que no se encontraron en el tablero)
    if gato_pos.size == 0 or raton_pos.size == 0:
# Si el gato o el raton no están en el tablero, retorna True, indicando que el juego ha terminado
        return True
# Asigna las coordenadas del gato (primer y único elemento del array)
    gato_pos = gato_pos[0]
# Asigna las coordenadas del ratón (primer y único elemento del array)
    raton_pos = raton_pos[0]
# Utiliza np.array_equal para verificar si las coordenadas del gato y del ratón son iguales
    if np.array_equal(gato_pos, raton_pos):
# Si las coordenadas son iguales, significa que el gato ha atrapado al ratón, y la función retorna True, indicando que el juego ha terminado
        return True
# Utiliza np.array_equal para verificar si las coordenadas del ratón son iguales a las coordenadas del destino del ratón
    if np.array_equal(raton_pos, destino):
# Si las coordenadas son iguales, significa que el ratón ha alcanzado su destino y ha escapado, y la función retorna True, indicando que el juego ha terminado
        return True
# Si ninguna de las condiciones anteriores se cumple, retorna False, indicando que el juego no ha terminado y continúa
    return False

def dibujar_destino(pantalla, imagen_destino, destino):
# Se crea un objeto Rect de Pygame que define un rectángulo en la pantalla donde se dibujará la imagen del destino
# Calcula la coordenada X Y del rectángulo multiplicando la columna del destino por el tamaño de una celda del tablero
# Define el ancho y el alto del rectángulo
    destino_rect = pygame.Rect(destino[1] * TAMAÑO_CELDA, destino[0] * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA)
# Utiliza el método blit de Pygame para dibujar la imagen_destino en la pantalla
    pantalla.blit(imagen_destino, destino_rect.topleft)

# Se encarga de configurar y ejecutar el juego
def jugar():
# Declara que posicion_gato y posicion_raton son variables globales
    global gato_pos, raton_pos
# Indica que el gato tiene el primer turno
    turno_gato = True
# Establece la profundidad de búsqueda para el algoritmo Minimax
    profundidad = 3

# Inicializa todos los módulos de Pygame
    pygame.init()
# Crea la ventana del juego con dimensiones especificadas
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
# Establece el título de la ventana del juego
    pygame.display.set_caption("Juego del Gato y el Raton")
# Crea un objeto Clock para controlar la velocidad del juego
    reloj = pygame.time.Clock()

# Cargar imágenes GIF y redimensionarlas
    imagen_gato = pygame.image.load('static/cat.png')
    imagen_raton = pygame.image.load('static/mouse.png')
    imagen_destino = pygame.image.load('static/destino.png')
    imagen_gato = pygame.transform.scale(imagen_gato, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    imagen_raton = pygame.transform.scale(imagen_raton, (TAMAÑO_CELDA, TAMAÑO_CELDA))
    imagen_destino = pygame.transform.scale(imagen_destino, (TAMAÑO_CELDA, TAMAÑO_CELDA))

# Variable que controla si el juego está en ejecución
    corriendo = True
# Bucle principal que continúa mientras el juego esté en ejecución y no haya terminado
    while corriendo and not juego_terminado(tablero):
# Procesa eventos de Pygame. Si se cierra la ventana del juego, se detiene el bucle
        for evento in pygame.event.get():
# Verificar si el evento actual es un evento de cierre de ventana
            if evento.type == pygame.QUIT:
# Detener el bucle principal del juego, indicando que el juego debe terminar
                corriendo = False

# Rellena la pantalla con el color de fondo
        pantalla.fill(COLOR_FONDO)

# Itera sobre cada celda del tablero
        for x in range(TAMAÑO_TABLERO):
            for y in range(TAMAÑO_TABLERO):
# Crea un rectángulo para la celda
                rect = pygame.Rect(y * TAMAÑO_CELDA, x * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA)
# Dibuja el borde de la celda   
                pygame.draw.rect(pantalla, COLOR_LINEA, rect, 1)
# Dibuja el gato si está en la celda actual
                if tablero[x, y] == 1:
                    pantalla.blit(imagen_gato, rect.topleft)
# Dibuja el ratón si está en la celda actual
                elif tablero[x, y] == 2:
                    pantalla.blit(imagen_raton, rect.topleft)
        
# Dibuja el destino del ratón
        dibujar_destino(pantalla, imagen_destino, destino)
# Actualiza la pantalla para reflejar los cambios
        pygame.display.flip()
# Si es el turno del gato, busca el mejor movimiento posible usando Minimax
        if turno_gato:
# Inicializa el mejor puntaje
            mejor_valor = -np.inf
# Comienza sin un movimiento asignado, indicando que aún no se ha evaluado ningún movimiento
            mejor_movimiento = None
# Genera posibles pos_movimientos del gato
            pos_movimientos = generar_movimientos(tablero, 1, movimientos_previos)
# Iterar sobre todos los movimientos posibles para evaluarlos
            for movimiento in pos_movimientos:
# Evaluar el puntaje de cada movimiento posible utilizando el algoritmo Minimax para decidir cuál es el mejor movimiento
                valor = minimax(movimiento, profundidad, False, movimientos_previos)
# Verificar si el puntaje del movimiento actual es mejor que el mejor puntaje encontrado hasta ahora
                if valor > mejor_valor:
# Actualizar mejor_valor con el puntaje del movimiento actual porque es mejor que el puntaje anterior
                    mejor_valor = valor
# Actualizar mejor_movimiento con el movimiento actual porque tiene el mejor puntaje encontrado hasta el momento
                    mejor_movimiento = movimiento
# Verificar si se ha encontrado un mejor movimiento           
            if mejor_movimiento is not None:
# Añadir el mejor movimiento a los movimientos previos para evitar movimientos repetidos en el futuro
                movimientos_previos.add(tuple(map(tuple, mejor_movimiento)))
# Actualizar el tablero con la nueva disposición resultante del mejor movimiento
                tablero[:] = mejor_movimiento
# Actualizar la posición del gato según el nuevo estado del tablero
                gato_pos = np.argwhere(tablero == 1)[0]
        else:
# Si es el turno del ratón, busca el mejor movimiento posible usando Minimax
# Comienza con el valor más alto posible para garantizar que cualquier valor encontrado durante la evaluación de movimientos será menor
            mejor_valor = np.inf
# Comienza sin un movimiento asignado, indicando que aún no se ha evaluado ningún movimiento
            mejor_movimiento = None
# Genera posibles movimientos del ratón
            pos_movimientos = generar_movimientos_raton(tablero, raton_pos, movimientos_previos)
# Evalúa cada movimiento usando Minimax
            for movimiento, nueva_posicion in pos_movimientos:
# Evaluar el puntaje de cada movimiento posible utilizando el algoritmo Minimax para decidir cuál es el mejor movimiento
                valor = minimax(movimiento, profundidad, True, movimientos_previos)
# Verificar si el puntaje del movimiento actual es mejor que el mejor puntaje encontrado hasta ahora
                if valor < mejor_valor:
# Actualizar mejor_valor con el puntaje del movimiento actual porque es mejor que el puntaje anterior
                    mejor_valor = valor
# Actualizar mejor_movimiento con el movimiento actual porque tiene el mejor puntaje encontrado hasta el momento
                    mejor_movimiento = movimiento
# Verificar si se ha encontrado un mejor movimiento           
            if mejor_movimiento is not None:
# Añadir el mejor movimiento a los movimientos previos para evitar movimientos repetidos en el futuro
                movimientos_previos.add(tuple(map(tuple, mejor_movimiento)))
# Actualizar el tablero con la nueva disposición resultante del mejor movimiento
                tablero[:] = mejor_movimiento
# Actualizar la posición del gato según el nuevo estado del tablero
                raton_pos = np.argwhere(tablero == 2)[0]
# Cambia de turno
        turno_gato = not turno_gato
# Controla la velocidad del juego a 2 FPS
        reloj.tick(2)  

# Rellena la pantalla con el color de fondo
    pantalla.fill(COLOR_FONDO)
# Verifica si las posiciones de los jugadores son válidas
    if gato_pos.size == 0 or raton_pos.size == 0:
        mensaje = "Error en la posición de los jugadores."
    else:
# Determina si el ratón ha alcanzado su destino
        if np.array_equal(raton_pos, destino):
            mensaje = "El Raton ha alcanzado su destino y ha escapado!"
# Determina si el gato ha atrapado al ratón
        else:
            mensaje = "El Gato ha atrapado al Raton!"
#  Crea una fuente para el texto del mensaje
    fuente = pygame.font.Font(None, 74)
# Renderiza el mensaje en una superficie de texto
    texto = fuente.render(mensaje, True, (0, 128, 0))
# Dibuja el texto en la pantalla
    pantalla.blit(texto, (20, ALTO_VENTANA // 2 - 37))
# Actualiza la pantalla para mostrar el mensaje final
    pygame.display.flip()

# Bucle que espera hasta que se cierre la ventana del juego
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
# Cierra Pygame y sale del juego
                pygame.quit()
                return

# Verifica si el script se está ejecutando como programa principal
if __name__ == "__main__":
    jugar()
