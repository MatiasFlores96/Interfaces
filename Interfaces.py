import tkinter as tk
from tkinter import messagebox

# Variables iniciales
inventory = {
    "The Legend of Zelda: Breath of the Wild": {"price": 70, "stock": 10},
    "Elden Ring": {"price": 60, "stock": 8},
    "Stardew Valley": {"price": 20, "stock": 15},
}
total_revenue = 0

# Función para manejar compras
def purchase(game):
    global total_revenue
    if inventory[game]["stock"] > 0:
        inventory[game]["stock"] -= 1
        total_revenue += inventory[game]["price"]
        update_display()
        messagebox.showinfo("Compra exitosa", f"Has comprado {game} por ${inventory[game]['price']}")
    else:
        messagebox.showwarning("Sin stock", f"{game} está agotado. Por favor, repón el inventario.")

# Función para reponer inventario
def restock(game):
    inventory[game]["stock"] += 5
    update_display()
    messagebox.showinfo("Inventario repuesto", f"Se han añadido 5 unidades de {game}.")

# Función para actualizar la visualización
def update_display():
    for game, widgets in display_widgets.items():
        widgets["stock_label"].config(text=f"Stock: {inventory[game]['stock']}")
    revenue_label.config(text=f"Total recaudado: ${total_revenue}")

# Crear ventana principal
root = tk.Tk()
root.title("Simulación - Tienda de Videojuegos")

# Widgets para cada videojuego
display_widgets = {}

for idx, (game, data) in enumerate(inventory.items()):
    frame = tk.Frame(root, pady=10)
    frame.pack(fill=tk.X)

    tk.Label(frame, text=game, font=("Arial", 14)).pack(anchor="w")
    price_label = tk.Label(frame, text=f"Precio: ${data['price']}", font=("Arial", 12))
    price_label.pack(anchor="w")

    stock_label = tk.Label(frame, text=f"Stock: {data['stock']}", font=("Arial", 12))
    stock_label.pack(anchor="w")

    btn_frame = tk.Frame(frame)
    btn_frame.pack(anchor="w")

    purchase_btn = tk.Button(btn_frame, text="Comprar", command=lambda g=game: purchase(g))
    purchase_btn.pack(side=tk.LEFT, padx=5)

    restock_btn = tk.Button(btn_frame, text="Reponer", command=lambda g=game: restock(g))
    restock_btn.pack(side=tk.LEFT, padx=5)

    # Guardar referencias para actualizar dinámicamente
    display_widgets[game] = {"price_label": price_label, "stock_label": stock_label}

# Etiqueta para mostrar el total recaudado
revenue_label = tk.Label(root, text=f"Total recaudado: ${total_revenue}", font=("Arial", 14), pady=10)
revenue_label.pack()

# Ejecutar la aplicación
update_display()
root.mainloop()
