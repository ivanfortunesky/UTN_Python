import sqlite3
import re
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror


# Función para conectar a l db
def conectar():   
    con = sqlite3.connect("estacionamiento.db") #lo crea una carpeta antes que el .py
    return con

# Función para crear la tabla si no existe
def crear_tabla():
    con = conectar()
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS estacionamiento (
                      id INTEGER PRIMARY KEY,
                      cochera INTEGER,
                      patente TEXT,
                      nombre TEXT,
                      telefono TEXT)''')
    con.commit()
    con.close()
########################################################
########################################################
    
#Función para modificar un registro de una cochera, por ejemplo cambirle la patente
    
########################################################
########################################################
    
def modificar():
    selection = tree.selection()
    if not selection:
        showerror("Error", "seleccione el registro a Modificar")
        return
    #cochera.set(tree.item(selection[0], "values")[0])

    cochera_local = cochera.get()
    patente_local  = validar_patente(patente.get())
    nombre_local  = validar_nombre(nombre.get())
    telefono_local  = validar_telefono(telefono.get())
 
        
    
    # Validar que todos los campos estén llenos
    if patente_local == "" or nombre_local == "" or telefono_local == "":
        showerror("Error", "Por favor, complete todos los campos.")
        return
    
    # Validar que el teléfono contenga solo dígitos
    if not telefono_local.isdigit():
        showerror("Error", "El teléfono debe contener solo números.")
        return
    
    # Conectar a la base de datos
    con = conectar()
    cursor = con.cursor()

    # updatear la base con los nuevos valores para ese registro

    cursor.execute('''UPDATE estacionamiento 
                      SET patente = ?, nombre = ?, telefono = ?
                      WHERE cochera = ?''',
                   (patente_local, nombre_local, telefono_local, cochera_local))
    con.commit()
    con.close()
    # Refrescar la tabla mostrada en treeview
    #showinfo("Información", "Se modificó el registro de esa cochera")
    consultar()



########################################################
########################################################

# Función para insertar un nuevo registro
def insertar_registro():
    
    
    cochera_local = cochera.get()
    patente_local  = validar_patente(patente.get())
    #Validar con REGEX (nombre, telefono y patente)
    nombre_local  = validar_nombre(nombre.get())
    telefono_local  = validar_telefono(telefono.get())
    
    # Validar que todos los campos estén llenos
    if cochera_local == "" or patente_local == "" or nombre_local == "" or telefono_local == "":
        showerror("Error", "Por favor, complete todos los campos.")
        return   
    
    # Validar que el teléfono contenga solo dígitos
    """if not telefono_local.isdigit():
        showerror("Error", "El teléfono debe contener solo números.")
        return
    """
    # Conectar a la base de datos
    con = conectar()
    cursor = con.cursor()
    
    # Verificar si la cochera está ocupada
    cursor.execute('''SELECT * FROM estacionamiento WHERE cochera = ?''', (cochera_local,))
    if cursor.fetchone():
        showerror("Error", f"La cochera {cochera_local} ya está ocupada.")
        return
    
    # Insertar el registro
    cursor.execute('''INSERT INTO estacionamiento (cochera, patente, nombre, telefono) VALUES (?, ?, ?, ?)''', (cochera_local, patente_local, nombre_local, telefono_local))
    con.commit()
    con.close()
    
    #showinfo("Información", "Registro insertado correctamente.")
    consultar()



# Función para consultar registros
def consultar():
    # Limpiar el Treeview antes de agregar nuevos datos
    for row in tree.get_children():
        tree.delete(row)
    
    con = conectar()
    cursor = con.cursor()
    cursor.execute('''SELECT * FROM estacionamiento''') # traigo de la base estacionamiento TODO
    filas = cursor.fetchall()
    con.close()
    filas_ordenadas = sorted(filas, key=lambda x: x[1])
    for fila in filas_ordenadas:
        tree.insert("", "end", values=(fila[1], fila[2], fila[3], fila[4]))

    """for row in cursor.fetchall():
        tree.insert("", "end", values=(row[1], row[2], row[3], row[4]))
    con.close()
    """

##################################################
# Función para updatear las campos cuando selecciono un item
def actualizar(evento):
    selection = tree.selection()
    if selection: 
        cochera_seleccionada = tree.item(selection[0], "values")[0]  
        cochera.set(cochera_seleccionada)  # hago  la cochera para ahorrarme pasos al modificar
    if selection: 
        patente_seleccionada = tree.item(selection[0], "values")[1]  
        patente.set(patente_seleccionada)  # hago  la patente para ahorrarme clicks al modificar
    if selection: 
        nombre_seleccionada = tree.item(selection[0], "values")[2]  
        nombre.set(nombre_seleccionada)  # hago  el nombre para ahorrarme tipeo al modificar
    if selection: 
        telefono_seleccionada = tree.item(selection[0], "values")[3]  
        telefono.set(telefono_seleccionada)  # hago  el nombre para ahorrarme tipeo al modificar
   
    
##################################################
    
# Función para borrar una reserva
def borrar():
    selection = tree.selection()
    if not selection:
        showerror("Error", "seleccione un registro para borrar.")
        return
    
    con = conectar()
    cursor = con.cursor()
    for item in selection:
        cursor.execute('''DELETE FROM estacionamiento WHERE cochera = ?''', (tree.item(item, "values")[0],))
    con.commit()
    con.close()
    
    #showinfo("Información", "Se borró el registro de esa cochera")
    consultar()

# Crear tabla si no existe
crear_tabla()


##################################################
#Función validar con Regex (Nombre solo alfanumerico y telefono solo dígitos sín espacios)

def validar_nombre(expresion_a_validar):
        nombre_regex = re.compile(r"^[A-Za-záéíóúñ]{2,}([\s][A-Za-záéíóúñ]{2,})+$", re.I)
               
        if nombre_regex.match(expresion_a_validar):
            return expresion_a_validar.title()
        else: 
            showerror("Error", "Completar Nombre y Apellido, solo alfanumerico.")
            return "<ERR formato Nom>"
        
def validar_telefono(expresion_a_validar):
        
        telefono_regex = re.compile(r"[0-9]{8,}$")
        
        if telefono_regex.match(expresion_a_validar):
            return expresion_a_validar
        else: 
            showerror("Error", "Completar telefono completo, solo números.")
            return "<ERR formato Tel>"
def validar_patente(expresion_a_validar):
        return expresion_a_validar.upper()
        

        
#expresion_a_validar == nombre_regex | telefono_regex:
##################################################   


# Configuración de la ventana principal
root = Tk()
root.title("Estacionamiento")

# Variables para almacenar los datos de entrada
cochera = StringVar()
patente = StringVar()
nombre = StringVar()
telefono = StringVar()

# Etiquetas y entradas
Label(root, text="Cochera").grid(row=1, column=0, sticky=W)
Entry(root, textvariable=cochera).grid(row=1, column=1)
Label(root, text="Patente").grid(row=2, column=0, sticky=W)
Entry(root, textvariable=patente).grid(row=2, column=1)
Label(root, text="Nombre").grid(row=3, column=0, sticky=W)
Entry(root, textvariable=nombre).grid(row=3, column=1)
Label(root, text="Teléfono").grid(row=4, column=0, sticky=W)
Entry(root, textvariable=telefono).grid(row=4, column=1)

# Botones #Tpdps el fila 5 y columnas consecutivas
Button(root, text="Ingresar Auto", command=insertar_registro).grid(row=5, column=0)
Button(root, text="Consultar", command=consultar).grid(row=5, column=1)
Button(root, text="Borrar", command=borrar).grid(row=5, column=2)
Button(root, text="Modificar", command=modificar).grid(row=5, column=3)

# TREEVIEW
tree = ttk.Treeview(root, columns=("Cochera", "Patente", "Nombre", "Teléfono"), show="headings")
tree.heading("Cochera", text="Cochera")
tree.heading("Patente", text="Patente")
tree.heading("Nombre", text="Nombre")
tree.heading("Teléfono", text="Teléfono")
tree.grid(row=7, column=0, columnspan=4)

tree.bind("<<TreeviewSelect>>", actualizar)

root.mainloop()
