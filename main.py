from models import Producto
from tkinter import Tk

if __name__ =="__main__":
    root = Tk() #instancia de ventana principal
    app = Producto(root)
    root.mainloop() #mantener la ventana abierta

