#Daniel domenech moreno - ddm19 - 54207039H
import sys, pygame
import tkinter
import bisect
from casilla import *
from Nodo import *
from mapa import *
from pygame.locals import *


MARGEN=5
MARGEN_INFERIOR=60
TAM=13
NEGRO=(0,0,0)
BLANCO=(255, 255,255)
VERDE=(0, 255,0)
ROJO=(255, 0, 0)
AZUL=(0, 0, 255)
AMARILLO=(255, 255, 0)

#------- ESTADÍSTICAS ----------
NODOEXPLORADO = 0
NODOCAMINO = 0
# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0:
        res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
# Devuelve las casillas vecinas (si existen en el mapa) a la casilla pasada
def vecinos(mapi,node,camino):
    global NODOEXPLORADO
    veins = []
    for x in range(-1,2):     # Recorro las 9 Direcciones (incluyendo la misma casilla)
        for y in range(-1,2):
            if not (x == 0 and y == 0):
                cx = node.GetX()+x
                cy = node.GetY()+y
                if cx > 0 and cx < mapi.getAlto()-1 and cy > 0 and cy < mapi.getAncho()-1:
                    if mapi.getCelda(cx,cy) == 0:
                        veins.append(Casilla(cx,cy))
                        if(camino[cx][cy] != '/'):
                            NODOEXPLORADO += 1
                        camino[cx][cy] = '/' #pintar vecinos azul
                        
                    
    return(veins)

def construyecamino(nodo,camino):
    global NODOCAMINO
    if nodo.GetPadre() == None:   # Es el inicio
        camino[nodo.GetX()][nodo.GetY()] = 'y'
    else:
        camino[nodo.GetX()][nodo.GetY()] = 'y'
        construyecamino(nodo.GetPadre(),camino)
        NODOCAMINO += 1

def InsOrden(lista,elemento):     #Inserto en la lista un elemento ordenado   
    lista.append(elemento)
    lista.sort(reverse=False, key=Nodo.Getf)
    
def aEstrella(mapi, origen, destino, camino):
    global NODOCAMINO
    global NODOEXPLORADO
    NODOEXPLORADO = NODOCAMINO = 0
    
    listaint = []
    listafront = []
    coste = -1
    orig = Nodo(origen.getFila(),origen.getCol(),None,0)
    listafront.append(orig) #inicializo lista frontera con el origen (el cerdo)
    
    while len(listafront) != 0: #Mientras la lista frontera no esté vacía
        n = listafront[0]
        if n.GetX() == destino.getFila() and n.GetY() == destino.getCol():  # Es meta
            construyecamino(n,camino)
            coste = n.Getg()
            break
        else:
            listaint.append(listafront.pop(0))
            hijos = vecinos(mapi,n,camino)
            for hijo in hijos:
                m = Nodo(hijo.getFila(),hijo.getCol(),n,Nodo.CalculaCoste(hijo,Casilla(n.GetX(),n.GetY()))) #Creo un nodo m con la casilla hijo
                m.g = n.g + m.coste
                m.SetFDDiag(destino) # Cambiar por SetF() para h = 0 (Recorrido en Anchura), SetFMan(destino) para Manhattan, SetFEucl(destino) para distancia euclídea o SetFDDiag(destino) para distancia diagonal

                existeint = False
                existefront = False
                for l in listaint:   # Compruebo que no existe en lista interior
                    if l.GetX() == m.GetX() and l.GetY() == m.GetY():
                        existeint = True
                for l in listafront: # Compruebo que no existe en lista frontera, si existe me guardo el índice para compararlo y modificarlo
                    if l.GetX() == m.GetX() and l.GetY() == m.GetY():
                        existefront = True
                        index = listafront.index(l)
                if not existeint:  # Si el hijo NO está en lista interior:
                    if not existefront:     # m no está en lista frontera
                        bisect.insort(listafront,m)
                        #InsOrden(listafront,m)       #Inserto en orden el elemento f >
                    elif m.Getg() < listafront[index].Getg():   # Si la nueva g de m es menor a la almacenada (nuevo camino + barato) cambio el padre y recalculo F
                        listafront[index].SetPadre(n)
                        listafront[index].SetCoste(Nodo.CalculaCoste(Casilla(n.GetX(),n.GetY()),Casilla(m.GetX(),m.GetY()))) #Recalculo Coste 
                        listafront[index].g = n.g + listafront[index].coste
                        listafront[index].SetFDDiag(destino) # Cambiar por SetF() para h = 0 (Recorrido en Anchura), SetFMan(destino) para Manhattan, SetFEucl(destino) para distancia euclídea o SetFDDiag(destino) para distancia diagonal
    print(NODOEXPLORADO)
    print(NODOCAMINO)
    return coste        
        
#PDevuelve si se ha pulsado el botón. Posición del botón: 20, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10]
def pulsaBoton(mapi, posicion):
    res=False
    
    if posicion[0] > 20 and posicion[0] < 70 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True
    
    return res
    
    
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

        
# función principal
def main():
    root= tkinter.Tk() #para eliminar la ventana de Tkinter
    root.withdraw() #se cierra
    file=tkinter.filedialog.askopenfilename() #abre el explorador de archivos    
    
    pygame.init()
    destino=Casilla(-1,-1)
    
    reloj=pygame.time.Clock()    
    
    if not file:     #si no se elige un fichero coge el mapa por defecto   
        file='mapa.txt'
    
    mapi=Mapa(file)
    origen=mapi.getOrigen()    
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton=pygame.image.load("boton.png").convert()
    boton=pygame.transform.scale(boton,[50, 30])
    
    personaje=pygame.image.load("pig.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])   
    
    coste=-1
    running= True
    primeraVez=True
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False               
                
            if event.type==pygame.MOUSEBUTTONDOWN:                
                #obtener posición y calcular coordenadas matriciales
                pos=pygame.mouse.get_pos()                
                colDestino=pos[0]//(TAM+MARGEN)
                filDestino=pos[1]//(TAM+MARGEN)
                casi=Casilla(filDestino, colDestino)
                if pulsaBoton(mapi, pos): #reinicializar                    
                    origen=mapi.getOrigen()
                    destino=Casilla(-1,-1)                    
                    camino=inic(mapi)
                    coste=-1
                    primeraVez=True
                elif esMapa(mapi, pos):
                    if bueno(mapi, casi):
                        if not primeraVez: #la primera vez el origen está en el mapa
                            origen=destino                            
                        else:                          
                            mapi.setCelda(int(origen.getFila()), int(origen.getCol()), 0) #se marca como libre la celda origen
                        destino=casi                        
                        camino=inic(mapi)
                        # llamar al A*
                        coste=aEstrella(mapi, origen, destino, camino)
                        if coste==-1:
                            tkinter.messagebox.showwarning(title='Error', message='No existe un camino entre origen y destino')                     
                        else:
                            primeraVez=False  # hay un camino y el destino será el origen para el próximo movimiento
                    else: # se ha hecho click en una celda roja                
                        tkinter.messagebox.showwarning(title='Error', message='Esa casilla no es valida')
                
          
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):
                if mapi.getCelda(fil, col)==2 and not primeraVez: #para que no quede negro el origen inicial
                    pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                    
                if mapi.getCelda(fil,col)==0:
                    if camino[fil][col]=='.':
                        pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    elif camino[fil][col]=='/':
                        pygame.draw.rect(screen, AZUL, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    else:
                        pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, ROJO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])    
        #pinta destino
        pygame.draw.rect(screen, VERDE, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN, TAM, TAM], 0)
        #pinta boton
        screen.blit(boton, [20, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste
        if coste!=-1:            
            fuente= pygame.font.Font(None, 30)
            texto= fuente.render("Coste "+str(coste), True, AMARILLO)            
            screen.blit(texto, [anchoVentana-120, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])            
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)        
       
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
