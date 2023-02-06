from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import importlib

loader_webcam=importlib.import_module('.webcam',package='services')


# Paso 7------------- Crearemos una funcion que se encargara de registrar el usuario ---------------------
path = "imagenes"

def crear_fichero_imagenes():
    folder_name = 'imagenes'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    folder_name1 = 'imagenes_LOG'
    if not os.path.exists(folder_name1):
            os.makedirs(folder_name1)
    #img = cv2.imread('image.jpg')
    #cv2.imwrite(os.path.join(folder_name, 'image.jpg'), img)



# PASO 3------ -----Crearemos una funcion para asignar al boton registro --------------------------------
def registro():
    global usuario
    global contra  # Globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(pantalla)  # Esta pantalla es de un nivel superior a la principal
    pantalla1.title("Registro")
    pantalla1.geometry("300x250")  # Asignamos el tamaño de la ventana

    # --------- Empezaremos a crear las entradas ----------------------------------------

    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text="Registro facial: debe de asignar un usuario:").pack()
    # Label(pantalla1, text = "").pack()  #Dejamos un poco de espacio
    Label(pantalla1, text="Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text="").pack()  # Dejamos un poco de espacio
    Label(pantalla1, text="Usuario * ").pack()  # Mostramos en la pantalla 1 el usuario
    usuario_entrada = Entry(pantalla1,
                            textvariable=usuario)  # Creamos un text variable para que el usuario ingrese la info
    usuario_entrada.pack()
    

    # ------------ Vamos a crear el boton para hacer el registro facial --------------------
    Label(pantalla1, text="").pack()
    Button(pantalla1, text="Registro Facial", width=15, height=1, command=registro_facial).pack()


# PASO 3.2----------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------

def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()

    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)

    lista_archivos = os.listdir(path)  # Vamos a importar la lista de archivos con la libreria os
    if log_usuario in lista_archivos:  # Comparamos los archivos con el que nos interesa
        archivo2 = open(log_usuario, "r")  # Abrimos el archivo en modo lectura
        verificacion = archivo2.read().splitlines()  # leera las lineas dentro del archivo ignorando el resto
        if log_contra in verificacion:
            print("Inicio de sesión exitoso")
            Label(pantalla2, text="Inicio de Sesion Exitoso", fg="green", font=("Calibri", 11)).pack()
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text="Contraseña Incorrecta", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()


# PASO 4--------------------------- Funcion para almacenar el registro facial --------------------------------------
def registro_facial():
     # Vamos a capturar el rostro
     cap = cv2.VideoCapture(1)  # Elegimos la camara con la que vamos a hacer la deteccion
     while (True):
        ret, frame = cap.read()  # Leemos el video
        cv2.imshow('Registro Facial', frame)  # Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el vídeoº
             break
     usuario_img = usuario.get()
     #Cambiar a directorio donde se guardara la imagen
     directorio_ppal=os.getcwd()
     os.chdir(path)
     cv2.imwrite(usuario_img + ".jpg", frame)  # Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
     os.chdir(directorio_ppal)
     print(os.getcwd())
     cap.release()  # Cerramos
     cv2.destroyAllWindows()
     usuario_entrada.delete(0, END)  # Limpiamos los text variables
     contra_entrada.delete(0, END)
     Label(pantalla1, text="Registro Facial Exitoso", fg="green", font=("Calibri", 11)).pack()

     
def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2

    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("300x250")  # Creamos la ventana
    Label(pantalla2, text="Login facial: debe de ingresar un usuario:").pack()
    Label(pantalla2, text="").pack()  # Dejamos un poco de espacio

    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()

    # ---------------------------------- Ingresamos los datos --------------------------
    Label(pantalla2, text="Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable=verificacion_usuario)
    usuario_entrada2.pack()

    # ------------ Vamos a crear el boton para hacer el login facial --------------------
    Label(pantalla2, text="").pack()
    Button(pantalla2, text="Inicio de Sesion Facial", width=20, height=1, command=login_facial).pack()

# PASO 6-----------Funcion para el Login Facial --------------------------------------------------------
def login_facial():
    # ------------------------------Vamos a capturar el rostro-----------------------------------------------------
    cap = cv2.VideoCapture(0)  # Elegimos la camara con la que vamos a hacer la deteccion
    while (True):
        ret, frame = cap.read()  # Leemos el video
        cv2.imshow('Login Facial', frame)  # Mostramos el video en pantalla
        if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el video
            break
    usuario_login = verificacion_usuario.get()  # Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
    directorio = os.getcwd()
    os.chdir("imagenes_LOG")
    cv2.imwrite(usuario_login + "LOG.jpg",
                frame)  # Guardamos la ultima captura del video como imagen y asignamos el nombre del usuario
    os.chdir(directorio)
    cap.release()  # Cerramos
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)  # Limpiamos los text variables
    contra_entrada2.delete(0, END)

    # ----------------- Funcion para guardar el rostro --------------------------

    def log_rostro(img, lista_resultados):
        directorio_ppal=os.getcwd()
        os.chdir("imagenes_LOG")
        data = pyplot.imread(img)
        os.chdir(directorio_ppal)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen 150x200
            cv2.imwrite(usuario_login + "LOG.jpg", cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    # -------------------------- Detectamos el rostro-------------------------------------------------------

    os.chdir("imagenes_LOG")
    img = usuario_login + "LOG.jpg"
    pixeles = pyplot.imread(img)
    os.chdir(directorio)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img, caras)

    # -------------------------- Funcion para comparar los rostros --------------------------------------------
    def orb_sim(img1, img2):
        orb = cv2.ORB_create()  # Creamos el objeto de comparacion

        kpa, descr_a = orb.detectAndCompute(img1, None)  # Creamos descriptor 1 y extraemos puntos claves
        kpb, descr_b = orb.detectAndCompute(img2, None)  # Creamos descriptor 2 y extraemos puntos claves

        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Creamos comparador de fuerza

        matches = comp.match(descr_a, descr_b)  # Aplicamos el comparador a los descriptores

        regiones_similares = [i for i in matches if
                              i.distance < 70]  # Extraemos las regiones similares en base a los puntos claves
        if len(matches) == 0:
            return 0
        return len(regiones_similares) / len(matches)  # Exportamos el porcentaje de similitud

    # ---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------

    im_archivos = os.listdir(path)  # Vamos a importar la lista de archivos con la libreria os
    if usuario_login + ".jpg" in im_archivos:  # Comparamos los archivos con el que nos interesa
        # os.chdir(path)
        directorio_ppal = os.getcwd()
        os.chdir(path)
        ## Ejecutar función
        rostro_reg = cv2.imread(usuario_login + ".jpg", 0)  # Importamos el rostro del registro
        os.chdir(directorio_ppal)
        os.chdir("imagenes_LOG")
        rostro_log = cv2.imread(usuario_login + "LOG.jpg", 0)  # Importamos el rostro del inicio de sesion
        os.chdir(directorio_ppal)
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.94:
            Label(pantalla2, text="Inicio de Sesión Exitoso", fg="green", font=("Calibri", 11)).pack()
            print("Bienvenido al sistema usuario: ", usuario_login)
            print("Compatibilidad con la foto del registro: ", similitud)
        else:
            print("Rostro incorrecto, Certifique su usuario")
            print("Compatibilidad con la foto del registro: ", similitud)
            Label(pantalla2, text="Incompatibilidad de rostros", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()

# PASO 2--------------- Funcion de nuestra pantalla principal ------------------------------------------------

def pantalla_principal():
    crear_fichero_imagenes()
    global pantalla  # Globalizamos la variable para usarla en otras funciones
    pantalla = Tk()
    pantalla.geometry("300x250")  # Asignamos el tamaño de la ventana
    pantalla.title("FacialRecognitionF5")  # Asignamos el titulo de la pantalla
    Label(text="Login Inteligente", bg="gray", width="300", height="2",
          font=("Verdana", 13)).pack()  # Asignamos caracteristicas de la ventana

    # ------------------------- Vamos a Crear los Botones ------------------------------------------------------

    Label(text="").pack()  # Creamos el espacio entre el titulo y el primer boton
    Button(text="Iniciar Sesion", height="2", width="30", command=login).pack()
    Label(text="").pack()  # Creamos el espacio entre el primer boton y el segundo boton
    Button(text="Registro", height="2", width="30", command=registro).pack()
    Label(text="").pack()  # Creamos el espacio entre el primer boton y el segundo boton
    Button(text="Iniciar detección facial", height="2", width="30", command=loader_webcam.iniciar_webcam).pack()
    pantalla.mainloop()