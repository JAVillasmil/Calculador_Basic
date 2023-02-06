import sqlite3
from tkinter import *
from tkinter import ttk

class Producto:
    """ Clase Producto sin herencia, este contiene atributo Nombre:Txt, Precio:Float, Categoria:Txt, Stock:Int id:Autoincrement
    Condicionales..
        Nombre no admite valores repetidos, No discrimina Mayusculas y minisculas.
        Precio solo admite valores numericos
        Categoria. No tiene condicionales
        Stock, solo admite valores numericos enteros

        En caso de interrupcion de condiciones, muestar mensaje razon en pantalla principal.

    Pantalla editar contiene la misma condicones.

    Condicionales..
        Nombre no admite valores repetidos, No discrimina Mayusculas y minisculas.
        Precio solo admite valores numericos
        Categoria. No tiene condicionales
        Stock, solo admite valores numericos enteros

        En caso de interrupcion por condiciones, vuelve a la pantalla principal, y muestra el error en ella.
    """

    #Comunicado base de datos ruta relativa
    db ="database/productos.db"
    """
    id: Integer/NN/PK/AI/U
    nombre: TEXT/NN/ / / U
    precio: REAL/NN/ / / 
    categoria: TEXT/NN/ / / 
    stock: INTEGER/NN/ / / 
    """

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App gestor de productos")
        self.ventana.resizable(1,1) #0,0 si no se quiere que el usuario mofidque
        self.ventana.wm_iconbitmap("recursos/icon.ico")

        #configuracon de interfaz grafica
        #creacion del contenedor frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto",font=('Calibri', 14, 'bold'), pady=5)
        frame.grid(row = 0, column = 0, columnspan = 20, pady = 10)
        # pady margen superior

        #casillas de entrada
        #label de nombre
        self.etiqueta_nombre = Label(frame, text="Nombre(*) ",font=('Calibri', 11, 'bold'))
        self.etiqueta_nombre.grid(row = 1, column =0)
        #entry nombre
        self.nombre = Entry(frame, width=40)
        self.nombre.focus() #solo puede estar en un cajon
        self.nombre.grid(row=1,column=1,sticky=E+W)

        # label de precio
        self.etiqueta_precio = Label(frame, text="Precio(*) ",font=('Calibri', 11, 'bold'))
        self.etiqueta_precio.grid(row = 2, column = 0)
        # entry precio
        self.precio = Entry(frame, width=40)
        self.precio.grid(row=2,column=1,sticky=E+W)

        # label de categoria
        self.etiqueta_categoria = Label(frame, text="Categoria(*) ",font=('Calibri', 11, 'bold'))
        self.etiqueta_categoria.grid(row=3, column=0)
        # entry categoria
        self.categoria =Entry(frame, width=40)
        self.categoria.grid(row=3, column=1, sticky=E+W)

        # label de stock
        self.etiqueta_stock = Label(frame, text="Stock(*) ",font=('Calibri', 11, 'bold'))
        self.etiqueta_stock.grid(row=4, column=0)
        # entry stock
        self.stock = Entry(frame, width=40)
        self.stock.grid(row=4, column=1, sticky=E+W)


        #boton añadir producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command= self.add_producto,style="my.TButton") #command no requiere que los metodos no requieran ()
        self.boton_aniadir.grid(row=6, columnspan= 4, sticky = W + E, pady=10) #styky mantiene los margenes sobre el

        # mensaje de error
        self.mensaje = Label(text="", fg="red",font=('Calibri', 11, 'bold'))
        self.mensaje.grid(row=4, column=3, columnspan=16, sticky=W+E)


        #tabla productos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',11)) # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea', {'sticky':'nswe'})]) # Eliminamos los bordes

        #estructura de la tabla
        self.tabla = ttk.Treeview(frame,height=20,columns=('#1','#2','#3',),style="mystyle.Treeview")
        self.tabla.grid(row=10,column=0,columnspan=4)
        self.tabla.heading("#0",text="Nombre",anchor=CENTER)
        self.tabla.heading("#1",text= "Precio",anchor=CENTER)
        self.tabla.heading("#2",text="Categoria", anchor=CENTER)
        self.tabla.heading("#3",text="Stock", anchor=CENTER)

        #botones de eliminar y editar
        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri",14,"bold"))

        boton_eliminar = ttk.Button(text="ELIMINAR", style="my.TButton", command= self.del_producto)
        boton_eliminar.grid(row=4, column=0, columnspan=1, sticky= W + E)
        boton_editar = ttk.Button(text="EDITAR", style="my.TButton", command= self.edit_producto)
        boton_editar.grid(row=4, column=19, columnspan=1, sticky= W + E)

        self.get_productos()


    #logica del programa
    def db_consulta(self, consulta, parametros = ()):#excute recibe un str y una tupla, importante de definir
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado


    #metodos propios
    def get_productos(self):
        registro_tabla = self.tabla.get_children() #borro y se vuelve a obtener los registros "actualizamosl info"
        #print(registro_tabla)
        for fila in registro_tabla:
            self.tabla.delete(fila)
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registro = self.db_consulta(query)
        for fila in registro:
            self.tabla.insert("", 0,text= fila[1] ,values= fila[2:]) # debe ir "" para que no herede de otra tabla/indice de intro de datos/ / /
            #print(fila)

    def validacion_nombre(self):#encargado de comprobar texto de nombre
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):#encargado de comprobar texto de precio
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def precio_num(self):
        precio_numerico = self.precio.get()
        try:
            stock_numerico = float(precio_numerico)
        except(ValueError):
            return False
        return True

    def validacion_categoria(self):  # encargado de comprobar texto de precio
        categoria_introducido_por_usuario = self.categoria.get()
        return len(categoria_introducido_por_usuario) != 0

    def validacion_stock(self):  # encargado de comprobar texto de precio
        stock_introducido_por_usuario = self.stock.get()
        return len(stock_introducido_por_usuario) != 0

    def stock_num(self):
        stock_numerico = self.stock.get()
        try:
            stock_numerico = int(stock_numerico)
        except(ValueError):
            return False
        return True

    def add_producto(self):
        if self.precio_num() == False:
            self.mensaje["text"] = ("Precio debe ser un elemento númerico")
        if self.stock_num() == False:
            self.mensaje["text"] = ("Stock debe ser un elemento númerico entero")
        if self.validacion_precio() and self.validacion_nombre() and self.validacion_categoria() and self.validacion_stock() \
                and  self.precio_num() and self.stock_num():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?) " #NULL debido a que es una columm autoicrement
            parametros =(self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get()) #debe ser en formato tupla
            try:
                self.db_consulta(query, parametros)
                self.mensaje["text"] = ("Datos guardados de forma correcta")
                #para debug
                #print(self.nombre.get())
                #print(self.precio.get())
                #print(self.categoria.get())
                #print(self.stock.get())
            except(sqlite3.IntegrityError):
                self.mensaje["text"] = ("Nombre colocado ya existe, Introduzca otro")
        if self.validacion_nombre() == False or self.validacion_precio() == False or self.validacion_categoria() == False or self.validacion_stock() == False:
            self.mensaje["text"] = ("Los campos marcados con * son obligatorios")
        self.get_productos()

    def del_producto(self):
        print((self.tabla.item(self.tabla.selection())))
        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query,(nombre,))
        self.get_productos()
        self.mensaje["text"] = ("Elemento eliminado con éxito")

    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]
        old_categoria = self.tabla.item(self.tabla.selection())['values'][1]
        old_stock = self.tabla.item(self.tabla.selection())['values'][2]




        #Nueva Ventana al activar EDITAR __________________________
        self.ventana_editar = Toplevel()
        self.ventana_editar.title = "Editar Producto"
        self.ventana_editar.resizable(0,0)
        self.ventana_editar.wm_iconbitmap("recursos/icon.ico")

        titulo = Label(self.ventana_editar, text="Editar Producto", font=("Calibri", 16 , "bold"))
        titulo.grid(row=0,column=0,columnspan=20,pady=5)

        #label nombre antiguo
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto",font=('Calibri', 13, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=10, pady=20)

        # Boton Actualizar Producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style='my.TButton', command=lambda:
                                        (self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                  self.input_nombre_antiguo.get(),
                                                                  self.input_precio_nuevo.get(),
                                                                  self.input_precio_antiguo.get(),
                                                                  self.input_categoria_nueva.get(),
                                                                  self.input_categoria_antigua.get(),
                                                                  self.input_stock_nuevo.get(),
                                                                  self.input_stock_antiguo.get())))

        self.boton_actualizar.grid(row=18, columnspan=10, sticky=W + E)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ")  #
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)  # Posicionamiento a traves
        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep,textvariable=StringVar(self.ventana_editar, value=nombre),
                                          state='readonly',font=('Calibri', 10, 'bold'))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ")
        self.etiqueta_precio_antiguo.grid(row=4, column=0)  # Posicionamiento a traves
        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep,textvariable=StringVar(self.ventana_editar,value=old_precio),
                                          state='readonly',font=('Calibri', 10, 'bold'))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoria antigua
        self.etiqueta_categoria_antigua = Label(frame_ep, text="Categoria antigua: ")
        self.etiqueta_categoria_antigua.grid(row=6, column=0)  # Posicionamiento a traves
        # Entry Categoria antigua (texto que no se podra modificar)
        self.input_categoria_antigua  = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                          state='readonly',font=('Calibri', 10, 'bold'))
        self.input_categoria_antigua .grid(row=6, column=1)

        # Label Categoria Nueva
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoria nueva: ")
        self.etiqueta_categoria_nueva.grid(row=7, column=0)
        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_categoria_nueva = Entry(frame_ep)
        self.input_categoria_nueva.grid(row=7, column=1)

        # Label stock antiguo
        self.etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo: ")
        self.etiqueta_stock_antiguo.grid(row=8, column=0)  # Posicionamiento a traves
        # Entry stock antiguo (texto que no se podra modificar)
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock),
                                          state='readonly',font=('Calibri', 10, 'bold'))
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ")
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        # Entry stock nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep)
        self.input_stock_nuevo.grid(row=9, column=1)

        # Boton Actualizar Producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto",
                                           command=lambda:self.actualizar_productos(
                                                             self.input_nombre_nuevo.get(),
                                                             self.input_nombre_antiguo.get(),
                                                             self.input_precio_nuevo.get(),
                                                             self.input_precio_antiguo.get(),
                                                             self.input_categoria_nueva.get(),
                                                             self.input_categoria_antigua.get(),
                                                             self.input_stock_nuevo.get(),
                                                             self.input_stock_antiguo.get()))

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio,
                             nueva_categoria, antigua_categoria, nuevo_stock, antiguo_stock):


        #condicionales para entrada datos a editar
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ? , categoria = ?, stock = ?' \
                'WHERE nombre = ? AND precio = ? AND categoria = ? AND stock = ?'

        #condiconales para precio y stock numericos
        condiciona_nuevo_precio = True
        condiciona_nuevo_stock = True
        condiciones_cumplicasd = True

        #interrupcion precio no numerico
        try:
            if nuevo_precio != "":
                nuevo_precio = float(nuevo_precio)
        except(ValueError):
            self.ventana_editar.destroy()
            self.mensaje["text"] = ("Editado interrumpido. precio este debe ser númerico")
            print("int precio")
            condiciona_nuevo_precio = False
        #interucpion stock no entero
        try:
            if nuevo_stock != "":
                nuevo_stock = int(nuevo_stock)
        except(ValueError):
            self.ventana_editar.destroy()
            self.mensaje["text"] = ("Editado interrumpido. stock debe ser número entero ")
            print("int stock")
            condiciona_nuevo_stock = False

        #condiconal para editar nombre
        nombre_1 = antiguo_nombre
        nombre_2 = antiguo_nombre
        if nuevo_nombre != "":
            nombre_1 = nuevo_nombre
            nombre_2 = antiguo_nombre

        #condiconal para editar precio
        precio_1 = antiguo_precio
        precio_2 = antiguo_precio
        if nuevo_precio != "":
            precio_1 = nuevo_precio
            precio_2 = antiguo_precio

        #condiconal para editar categoria
        categoria_1 = antigua_categoria
        categoria_2 = antigua_categoria
        if nueva_categoria != "":
            categoria_1 = nueva_categoria
            categoria_2 = antigua_categoria

        #condiconal para editar stock
        stock_1 = antiguo_stock
        stock_2 = antiguo_stock
        if nuevo_stock != "":
            stock_1 = nuevo_stock
            stock_2 = antiguo_stock

        parametros = (nombre_1, precio_1, categoria_1, stock_1, nombre_2, precio_2, categoria_2, stock_2)

        if (nuevo_nombre != "" or  nuevo_precio != "" or  nueva_categoria != "" or  nuevo_stock != "") \
                and (condiciona_nuevo_precio and condiciona_nuevo_stock):
            producto_modificado = True
           # print("COND OR")

        if nuevo_nombre == "" and  nuevo_precio == "" and  nueva_categoria == "" and  nuevo_stock == "" \
                and condiciona_nuevo_precio and condiciona_nuevo_stock :
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto "{}" no ha sido actualizado'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            #rint("COND AND")

        if producto_modificado == True:
            # interrupcion nombre duplicado
            try:
                self.db_consulta(query, parametros)
            except(sqlite3.IntegrityError):
                self.ventana_editar.destroy()
                condiciones_cumplicasd = False
                self.mensaje["text"] = ("Editado interrumpido. Nombre colocado ya existe")


        if condiciones_cumplicasd == True and producto_modificado == True:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado con éxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
           # print("PRODUCTO MODIFCADO")