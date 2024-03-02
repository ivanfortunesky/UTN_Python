import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror


# Función para conectar a l db
def conectar():    
    con = sqlite3.connect("estacionamiento.db")
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
    patente_local  = patente.get()
    nombre_local  = nombre.get()
    telefono_local  = telefono.get()
 
        
    
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
    patente_local  = patente.get()
    nombre_local  = nombre.get()
    telefono_local  = telefono.get()
    
    # Validar que todos los campos estén llenos
    if cochera_local == "" or patente_local == "" or nombre_local == "" or telefono_local == "":
        showerror("Error", "Por favor, complete todos los campos.")
        return
    
    # Validar que el teléfono contenga solo dígitos
    if not telefono_local.isdigit():
        showerror("Error", "El teléfono debe contener solo números.")
        return
    
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
    for row in cursor.fetchall():
        tree.insert("", "end", values=(row[1], row[2], row[3], row[4]))
    con.close()


##################################################
# Función para updatear las campos cuando selecciono un item
def actualizar(evento):
    selection = tree.selection()
    if selection: 
        cochera_seleccionada = tree.item(selection[0], "values")[0]  
        cochera.set(cochera_seleccionada)  # hago solo la cochera para ahorrarme pasos al modificar
    patente.set("")
    nombre.set("")
    telefono.set("")

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
