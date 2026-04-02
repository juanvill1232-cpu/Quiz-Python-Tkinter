#Proyecto Final: Juego de Quiz con Tkinter
#Alumno: Juan Jesús Villena Delgado
#Materia: Fundamentos de programación
#Fecha de entrega: 12 de Enero del 2026
#Librerias
import tkinter as tk #Librería que permite crear interfaces gráficas
from tkinter import messagebox #Addon de la libería Tkinter para crear cuadros de información
import tkinter.font as tkfont #Addon de tkinter para personalizar la fuente de los textos
import random #Librería que permite mezclar el orden de las preguntas en cada intento/nivel
import json # Librería para manejar archivos JSON (guardar datos)
import os # Librería para verificar si el archivo existe

 #Funciones
def main(): #Función principal que contiene toda la lógica del juego
    #Configuración de la Ventana Principal
    ventana = tk.Tk() #Variable que declara la ventana vía Tkinter 
    ventana.title("Juego de Quiz") #Título con el que se muestra la ventana
    ventana.geometry("600x500") #Dimensiones de la ventana del programa
    ventana.resizable(False, False) #Condición que evita que la ventana se pueda redimensionar
    
    #Fuentes personalizadas
    fuente_titulo = tkfont.Font (family = "Minecraft", size = 20, weight = "bold") #Fuente para el titulo
    fuente_pregunta = tkfont.Font (family = "Minecraft", size = 14) #Fuente para las preguntas
    fuente_boton = tkfont.Font (family = "Minecraft", size = 12) #Fuentes para el botón
    fuente_texto = tkfont.Font (family = "Minecraft", size =13) #Fuentes para el texto

    # Frames (Contenedores de las vistas/pantallas)
    frame_menu = tk.Frame(ventana, bg = "#2c9c1d")#Ventana que muestra el  menu 
    frame_registro = tk.Frame (ventana, bg = "#bbdefb") #Ventana que muestra la pantalla de registro
    frame_info = tk.Frame(ventana, bg = "#ffffff") #Ventana que muestra información (usuarios/créditos)
    frame_nivel_1 = tk.Frame(ventana, bg = "#e3f2fd") #Ventana que contiene el nivel 1
    frame_nivel_2 = tk.Frame(ventana, bg = "#e8f5e9") #Ventana que contiene el nivel 2
    frame_nivel_3 = tk.Frame(ventana, bg = "#fff3e0") #Ventana que contiene el nivel 3

    #Muestra el frame de registro al ejecutar el programa
    frame_registro.pack(fill="both", expand=True) #Función que expande la ventana del menú al inicio de la ejcución del programa
    
    #Variables
    intentos_nivel_1 = 0 #Variable que controla los intentos del nivel 1
    intentos_nivel_2 = 0 #Variable que controla los intentos del nivel 2
    intentos_nivel_3 = 0 #Variable que controla los intentos del nivel 3
    max_intentos = 3 #Variable que permite/bloquear los intentos de los niveles (universal para todos)
    indice = 0 #Posicion original de las preguntas de los niveles (preguntas, opciones, respuestas. Aplica para los 3 niveles)
    puntaje = 0 #Puntaje con el que se inicia cada nivel
    usuarios = {} #Diccionario para almacenar el progreso del usuario
    usuario_actual = tk.StringVar()#Variable que almacena el nombre del usuario actual
    archivo_usuarios = "usuarios.json" # Nombre del archivo donde se guardarán los datos

    # --- FUNCIONES DE PERSISTENCIA (GUARDAR/CARGAR) ---
    def cargar_usuarios():
        """Carga los usuarios desde el archivo JSON si existe."""
        if os.path.exists(archivo_usuarios):
            try:
                with open(archivo_usuarios, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    usuarios.update(datos) # Actualiza el diccionario con los datos del archivo
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def guardar_usuarios_archivo():
        """Guarda el diccionario de usuarios en el archivo JSON."""
        try:
            with open(archivo_usuarios, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")

    # Cargar datos al iniciar la aplicación
    cargar_usuarios()
    
    #Ventana de registro
    tk.Label (frame_registro, #Etiqueta de texto que indica al usuario que ingrese su nombre
           text = "Ingresa tu nombre",
           font = fuente_titulo,
           bg = "#bbdefb").pack(pady = 30)
    
    nombre_entrada = tk.Entry(frame_registro, #Campo de entrada para el nombre del usuario
                              font = fuente_texto,
                              justify = "center")
    
    nombre_entrada.pack(pady = 10) #Posición del campo de entrada en el eje Y
    
 
    #FUNCION DE GUARDAR USUARIO
    def guardar_usuario (): #Función que guarda el nombre del usuario y valida que no esté vacío o repetido
        try: 
            nombre = nombre_entrada.get().strip()
            if nombre == "":
                #Lanza un error si el nombre está vacío
                raise ValueError("Nombre vacio")
            
            # MODIFICACIÓN: Si el usuario ya existe, permitimos el ingreso (Login)
            if nombre in usuarios:
                usuario_actual.set(nombre)
                messagebox.showinfo("Bienvenido de nuevo", f"Hola {nombre}, tus puntajes han sido cargados.")
                mostrar_menu()
                return

            usuarios [nombre] = {"nivel_1" : 0, #Variable que inicializa el progreso del usuario en cada nivel
                                 "nivel_2" : 0,
                                 "nivel_3" : 0}
            usuario_actual.set(nombre) #Establece el nombre del usuario actual
            guardar_usuarios_archivo() # Guardamos el nuevo usuario en el archivo
            
            messagebox.showinfo("Correcto", f"Bienvenido {nombre}")
            mostrar_menu() #Función que pasa al menú principal
              
        except  ValueError as e: 
            #Captura errores controlados ()nombre vacío o duplicado)
            messagebox.showwarning("Error", str(e))
        except Exception as e:
            #Captura cualquier error inesperado
            messagebox.showerror("Error", f"Ocurrió un error innesperado: {e}")
    
    #Botón para registrar y entrar al juego        
    tk.Button(frame_registro, text = "Entrar",
              font = fuente_boton,
              width = 20,
              command = guardar_usuario).pack(pady = 15)
        
    #FUNCIONES DE NAVEGACIÓN  Y VISTAS DE INTERFAZ
    def mostrar_menu(): #Función que muestra el menu al ejecutar el programa
        nonlocal intentos_nivel_1, intentos_nivel_2, intentos_nivel_3
        #Reinicia los intentos de cada nivel al volver al menú
        intentos_nivel_1 = 0
        intentos_nivel_2 = 0
        intentos_nivel_3 = 0
        #Ocultan todos los frames excepto el del menú
        frame_info.pack_forget() #Variable que oculta el frame de la información 
        frame_nivel_1.pack_forget() #Variable que oculta el frame del nivel 1
        frame_nivel_2.pack_forget() #Variable que oculta el frame del nivel 2
        frame_nivel_3.pack_forget() #Variable que oculta el frame del nivel 3
        frame_registro.pack_forget() #Variable que oculta el frame del registro
        frame_menu.pack(fill="both", expand=True) #Variable que expande el frame del menu

    def mostrar_instrucciones(): #Función que muestra la vista de instrucciones
        frame_menu.pack_forget()
        frame_info.pack(fill="both", expand=True)
        label_info.config(
            text="INSTRUCCIONES\n\n"
                 "1. Responde las preguntas.\n"
                 "2. Cada respuesta correcta suma 1 punto.\n"
                 "3. Necesitas 8 aciertos para avanzar.\n"
                 "4. Máximo 3 intentos por nivel."
                 
        )

    def mostrar_creditos(): #Función que muestra la vista de créditos y puntajes
        frame_menu.pack_forget()
        frame_info.pack(fill="both", expand=True)
        
        texto = "Créditos\n\n"
        texto += "Alumno: Juan Jesús Villena Delgado\n"
        texto += "Juego de Quiz en Python\n\n"
        
        #Muestra los puntajes de los usuarios registrados
        for nombre, datos in usuarios.items():
            texto += (f"{nombre}\n"
                      f"Nivel 1: {datos['nivel_1']}/10\n"
                      f" Nivel 2: {datos['nivel_2']}/10\n"
                      f"Nivel 3: {datos['nivel_3']}/10\n")
        label_info.config(text = texto) #Actualiza la etiqueta con la información

    def cerrar_sesion(): #Función para regresar al registro y cambiar de usuario
        frame_menu.pack_forget()
        nombre_entrada.delete(0, tk.END) #Limpia el campo de entrada
        usuario_actual.set("")
        frame_registro.pack(fill="both", expand=True)

    def eliminar_usuario(): #Función para eliminar el usuario actual y sus datos
        nombre = usuario_actual.get()
        # Pregunta de confirmación antes de borrar
        if messagebox.askyesno("Eliminar Usuario", f"¿Estás seguro de que deseas eliminar a '{nombre}'?\nSe perderá todo el progreso y no se puede deshacer."):
            if nombre in usuarios:
                del usuarios[nombre] # Elimina del diccionario
                guardar_usuarios_archivo() # Actualiza el archivo JSON
                messagebox.showinfo("Eliminado", f"El usuario {nombre} ha sido eliminado.")
                cerrar_sesion() # Cierra sesión automáticamente

    #Lógica del juego y niveles
    # Nivel 1
    preguntas = [ #Lista de preguntas que se usan en el nivel 1
        "¿Qué función se usa para mostrar texto en pantalla?",
        "¿Cuál es el tipo de dato de 5?",
        "¿Cómo se escribe un comentario en Python?",
        "¿Qué función se usa para pedir datos al usuario?",
        "¿Cuál operador se usa para sumar?",
        "¿Qué tipo de dato es 'Hola'?",
        "¿Cuál es un nombre válido de variable?",
        "¿Qué palabra define una función?",
        "¿Cuál valor representa verdadero?",
        "¿Extensión de archivos Python?"
    ]

    opciones = [ #Lista de opciones para cada pregunta del nivel 1
        ["print()", "show()", "echo()", "write()"],
        ["int", "str", "float", "bool"],
        ["//comentario", "#comentario", "/comentario/", "<!comentario>"],
        ["input()", "read()", "scan()", "get()"],
        ["+", "-", "*", "/"],
        ["int", "char", "str", "bool"],
        ["1variable", "variable_1", "variable-1", "variable 1"],
        ["function", "def", "fun", "define"],
        ["True", "False", "0", "None"],
        [".py", ".python", ".pt", ".txt"]
    ]

    respuestas = [0,0,1,0,0,2,1,1,0,0] #Lista de respuestas correctas para el nivel 1

    #Nivel 2
    preguntas_nivel_2 = ["¿Qué estructura se usa para manejar excepciones?", #Lista de preguntas que se usan para el nivel 2
                         "¿Cúal ciclo se usa cuando no se sabe cuántas veces se repetirá?",
                         "¿Qué palabra detiene un ciclo?",
                         "¿Cómo se agrega un elemento a una lista?", 
                         "¿Para qué sirve una lista en Python?",
                         "¿Qué tipo de dato es [1,2,3]?",
                         "¿Qué símbolo o función sirve para unir texto con variables numericas?",
                        "¿Cuál operador se usa para comparar igualdad?", 
                        "¿Para qué se usa un ciclo en Python?",
                        "¿Qué significa elif?"]
    
    opciones_nivel_2 = [ #Lista de opciones para cada pregunta del nivel 2
    ["try-except", "if-else", "for", "while"],
    ["for", "if", "while", "def"],
    ["stop", "exit", "break", "end"],
    [".add()", ".append()", ".insert()", ".push()"],
    ["Guardar un dato", "Guardar varios datos", "Mostrar texto", "Crear funciones"],  
    ["tuple", "list", "dict", "set"],
    ["string", "f", "++", ".append"],
    ["=", "==", "!=", "<>"],
    ["Repetir instrucciones", "Comparar datos", "Crear listas", "Salir del programa"], 
    ["Otro if", "Error", "Fin del programa", "Un ciclo"]]

    respuestas_nivel_2 = [0,2,2,1,1,1,1,1,0,0] #Lista de respuestas correctas para el nivel 2
    
    #Nivel 3
    preguntas_nivel_3 = ["¿Qué hace range (5)?", #Lista de preguntas que se usan para el nivel 3
                         "¿Qué ciclo se usa para recorrer una lista?",
                         "¿Qué palabra devuelve un valor en una funcion?",
                         "¿Cómo se declara una lista vacía?",
                        "¿Qué estructura se usa para seleccionar entre varias opciones?",
                        "¿Que hace break?",
                        "¿Cúal No es un tipo de dato?",
                        "¿Qué simbolo se usa para indexar listas?",
                        "¿Que hace return?",
                        "¿Cúal es un valor falso?"]
    
    opciones_nivel_3 = [["Cuenta del 1 al 5", "Cuenta del 0 al 4", #Lista de opciones para cada pregunta del nivel 3
                         "Cuenta en intervalo infinito", "Marca error"],
                          ["while", "for", "else", "loop"],
                          ["end", "return", "stop", "exit"],
                          ["{}", "()", "[]", "<>"],
                          ["match case", "option", "try", "catch"],
                          ["Repite", "Sale del ciclo", "Termina programa", "Nada"],
                          ["int", "str", "float", "loop"],
                          ["()", "{}", "[]", "<>"],
                          ["Imprime", "Devuelve valor", "Cierra programa", "Repite"],
                          ["True", "1", "False", "!0"]]
    
    respuestas_nivel_3 = [1,2,1,2,1,1,3,2,1,2] #Lista de respuestas correctas para el nivel 3
                         

    indice = 0 #Posición inicial de las preguntas
    puntaje = 0 #Puntaje iinicial con el que comienza cada nivel
    orden = list(range(10)) #Lista que contiene el orden de las preguntas y posibles respuestas
    random.shuffle(orden) #Mezcla el orden de las preguntas/opciones para cada intento/nivel

    label_pregunta = tk.Label( #Etiqueta que muestra las preguntas en el nivel 1
        frame_nivel_1,
        text="",
        font= fuente_pregunta,
        wraplength=500
    )
    label_pregunta.pack(pady=20)

    botones = [] #Lista que contiene los botones para las opciones del nivel 1

    #Nivel 1
    def iniciar_nivel_1(): #Función que inicia el nivel 1
        nonlocal indice, puntaje, orden, intentos_nivel_1
        if intentos_nivel_1>= max_intentos: #Valida si se han agotado los intentos
            messagebox.showerror("Game Over", "Ya no hay mas intentos")
            mostrar_menu()
            return
        intentos_nivel_1 += 1 #Reincio y aumento de intentos
        indice = 0
        puntaje = 0
        orden = list(range(10))
        random.shuffle(orden) #Vuelve a mezclar el orden de las preguntas/opciones en caso de reintento
        
        #Transición de vistas
        frame_menu.pack_forget()
        frame_nivel_1.pack(fill="both", expand=True)
        mostrar_pregunta()

    def mostrar_pregunta():
        idx = orden[indice] #Obtiene el índice de la pregunta actual segun el orden aleatorio
        label_pregunta.config(text=preguntas[idx]) #Muestra la pregunta
        for i in range(4): #Configura el texto y la función de cada botón 
            botones[i].config(
                text=opciones[idx][i],
                command=lambda i=i: validar(i) #Usa lambda para pasar el índice de la opción a la funciuón validar
            )

    def validar(opcion): #Función que valida la respuesta seleccionada
        nonlocal indice, puntaje
        idx = orden[indice] #Indice de la pregunta original
        if opcion == respuestas[idx]: #Verifica si la opción seleccionada es correcta
            puntaje += 1

        indice += 1 #Avanza a la siguiente pregunta
        if indice <10: #Comprueba si hay más preguntas
            mostrar_pregunta() #Muestra la siguiente pregunta
        else: #Se considera que el nivel ha terminado
            usuarios[usuario_actual.get()]["nivel_1"] = puntaje #Guarda el puntaje del nivel 1
            guardar_usuarios_archivo() # Guardamos el progreso en el archivo
            if puntaje >= 8: #Requisito para avanzar de nivel (8 o más aciertos)
                messagebox.showinfo("Nivel Superado" ,f"Puntaje {puntaje}/10\n Avanzas al siguiente nivel!")
                iniciar_nivel_2() #Inicia el nivel 2
            else: #Repite el nivel si no se alcanza el puntaje mínimo
                messagebox.showinfo("Puntaje insuficiente para avanzar de nivel", 
                                f"Puntaje obtenido: {puntaje}/10 \n Intentos {intentos_nivel_1}/{max_intentos}")
                iniciar_nivel_1() #Vuelve a iniciar el nivel 1

    #Crea los botones para las opciones del nivel 1
    for i in range(4): #Ciclo que crea los 4 botones sin necesidad de declarar los 4 por separado
        btn = tk.Button(frame_nivel_1, width=30, font = fuente_boton) #Variable del botón y su ubicación
        btn.pack(pady=5) #Posición del boton en el eje Y
        botones.append(btn) #Variable que agrega los botones al} la lista botones_2

    #Logica del nivel 2
    #label y botones del nivel 2
    label_pregunta_2 = tk.Label (frame_nivel_2, font = fuente_pregunta, wraplength = 500)
    label_pregunta_2.pack(pady = 20)
    
    botones_2 =[] #Lista que contiene los botones para el nivel 2
    for a in range (4): #Ciclo que crea los 4 botones sin necesidad de declarar los 4 por separado
        btn = tk.Button (frame_nivel_2, width= 30, font = fuente_boton) #Variable del botón y su ubicación
        btn.pack (pady = 5) #Posición del boton en el eje Y
        botones_2.append(btn) #Variable que agrega los botones al} la lista botones_2

    def iniciar_nivel_2(): #Función que inicia el nivel 2
        nonlocal indice, puntaje, intentos_nivel_2 
        if intentos_nivel_2 >= max_intentos: #Valiidacion de intentos
            messagebox.showerror ("Game Over", "Ya no hay mas intentos")
            mostrar_menu ()
            return
        
        intentos_nivel_2 += 1 #Reinicio y aumento de intentos
        indice = 0
        puntaje = 0
        orden  = list(range(10))
        random.shuffle(orden)
        
        #Transición de vistas
        frame_nivel_1.pack_forget()
        frame_nivel_2.pack (fill="both", expand=True)
        mostrar_pregunta_2() 
    
    def mostrar_pregunta_2(): #Función que muestra las preguntas del nivel 2
        idx = orden [indice]    
        label_pregunta_2.config (text=preguntas_nivel_2[idx])
        for i in range(4): #Configura los botones de opciones para el nivel 2
            botones_2[i].config(text = opciones_nivel_2[idx][i],
            command = lambda i=i: validar_2(i))

    def validar_2(opcion):
        nonlocal indice, puntaje, intentos_nivel_2
        idx = orden [indice]
        
        if opcion == respuestas_nivel_2[idx]: #Verifica respuesta y actualiza puntaje
            puntaje += 1
           
        indice += 1
            
        if indice <10: #Comprueba si hay más preguntas
            mostrar_pregunta_2()
        else: #Se considera que el nivel ha terminado
            usuarios[usuario_actual.get()]["nivel_2"] = puntaje #Guarda el puntaje del nivel 2
            guardar_usuarios_archivo() # Guardamos el progreso en el archivo
            if puntaje >= 8: # Requisito para avanzar de nivel (8 o más aciertos)
                messagebox.showinfo ("Nivel 2 superado!", f"Felicidades!\n Puntaje {puntaje}/10")
                iniciar_nivel_3 () #Inicia el nivel 3
            else: #Repite el nivel si no se alcanza el puntaje mínimo
                messagebox.showerror("Nivel 2", 
                                     f"Puntaje {puntaje}/10 \n Intento {intentos_nivel_2}/{max_intentos}")
                iniciar_nivel_2()
                return
        
    #Logica del nivel 3
    #label y botones del nivel 3
    label_pregunta_3 = tk.Label (frame_nivel_3, font = fuente_pregunta, wraplength = 500)
    label_pregunta_3.pack(pady = 20)
    
    botones_3 = [] #Lista que contiene los botones para el nivel 3
    for i in range (4): #Ciclo que crea los 4 botones sin necesidad de declarar los 4 por separado
        btn = tk.Button(frame_nivel_3, width = 30, font = fuente_boton) #Variable del botón y su ubicación
        btn.pack(pady = 5) #Posición del boton en el eje Y
        botones_3.append(btn) #Variable que agrega los botones a la lista botones_3
        
    def iniciar_nivel_3 (): #Función que inicia el nivel 3
        nonlocal indice, puntaje, intentos_nivel_3
        if intentos_nivel_3 >= max_intentos:#Valiidacion de intentos
            messagebox.showerror ("Game Over", "Ya no te quedan intentos")
            mostrar_menu ()
            return
    
        intentos_nivel_3 += 1 #Reinicio y aumento de intentos
        indice = 0
        puntaje = 0
        orden = list(range(10))
        random.shuffle(orden)
    
        #Transición de vistas
        frame_nivel_2.pack_forget()
        frame_nivel_3.pack (fill = "both", expand = True)
        mostrar_pregunta_3 ()
    
    def mostrar_pregunta_3 (): #Función que muestra las preguntas del nivel 3
        idx = orden [indice]
        label_pregunta_3.config(text = preguntas_nivel_3[idx])#Muestra la pregunta
        for i in range (4): #Configura los botones de opciones para el nivel 3
            botones_3[i].config( text = opciones_nivel_3[idx][i],
                                command = lambda i=i: validar_3(i))
    
    def validar_3(opcion):
        nonlocal indice, puntaje
        idx = orden[indice]
        
        if opcion == respuestas_nivel_3[idx]: #Verifica respuesta y actualiza puntaje
            puntaje += 1
            
        indice += 1
        
        if indice <10: #Comprueba si hay más preguntas
            mostrar_pregunta_3()
        else: #Se considera que el nivel ha terminado
            usuarios[usuario_actual.get()]["nivel_3"] = puntaje #Guarda el puntaje del nivel 3
            guardar_usuarios_archivo() # Guardamos el progreso en el archivo
            if puntaje>= 8: #Requisito para completar el juego (8 o más aciertos)
                messagebox.showinfo("Felicidades!", 
                                    f"Terminaste el juego \n Puntaje final: {puntaje}/10")
                mostrar_menu() #Vuelve al menú principal
            else: #Repite el nivel si no se alcanza el puntaje mínimo
                messagebox.showwarning("Nivel 3", f"Puntaje {puntaje}/10 \n Intento {intentos_nivel_3}/{max_intentos}")
                iniciar_nivel_3()
        

    #Menu
    tk.Label(
        frame_menu,
        text="MENU PRINCIPAL",
        font= fuente_titulo,
        bg = ("#2c9c1d")
    ).pack(pady=30)

    #Botones del menú principal
    tk.Button(frame_menu, text="Instrucciones", width=25,  font = fuente_boton, command=mostrar_instrucciones).pack(pady=10)
    tk.Button(frame_menu, text="Comenzar juego", width=25, font = fuente_boton,command=iniciar_nivel_1).pack(pady=10)
    tk.Button(frame_menu, text="Créditos", width=25,  font = fuente_boton, command=mostrar_creditos).pack(pady=10)
    tk.Button(frame_menu, text="Cerrar Sesión", width=25, font = fuente_boton, command=cerrar_sesion).pack(pady=10)
    tk.Button(frame_menu, text="Eliminar Usuario", width=25, font = fuente_boton, command=eliminar_usuario).pack(pady=10)
    tk.Button(frame_menu, text="Salir", width=25, font = fuente_boton, command=ventana.quit).pack(pady=10)

    #Info 
    label_info = tk.Label(frame_info, text="", font= fuente_texto, justify="left")
    label_info.pack(pady=40)

    tk.Button(frame_info, text="Volver al menú", width=20, font = fuente_boton, command=mostrar_menu).pack()

    #Punto de entrada de la ventana
    ventana.mainloop()

#Punto de entrada principal
if __name__== "__main__":
    main()