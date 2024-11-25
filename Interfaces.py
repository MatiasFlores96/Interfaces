import tkinter as tk
from tkinter import messagebox
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="videogame_store",
    user="postgres",
    password="123456"  # Use the same password you set earlier
)
cur = conn.cursor()

# Function to fetch inventory from the database
def fetch_inventory():
    cur.execute("SELECT * FROM inventory")
    rows = cur.fetchall()
    inventory = {}
    for row in rows:
        game, price, stock = row
        inventory[game] = {"price": price, "stock": stock}
    return inventory

# Function to fetch total revenue from the database
def fetch_total_revenue():
    cur.execute("SELECT revenue FROM total_revenue WHERE id = 1")
    revenue = cur.fetchone()[0]
    return revenue

# Initialize variables
inventory = fetch_inventory()
total_revenue = fetch_total_revenue()

# Function to handle purchases
def purchase(game):
    global total_revenue
    if inventory[game]["stock"] > 0:
        inventory[game]["stock"] -= 1
        total_revenue += inventory[game]["price"]

        # Update the database
        cur.execute("UPDATE inventory SET stock = %s WHERE game = %s", (inventory[game]["stock"], game))
        cur.execute("UPDATE total_revenue SET revenue = %s WHERE id = 1", (total_revenue,))
        conn.commit()

        update_display()
        messagebox.showinfo("Compra exitosa", f"Has comprado {game} por ${inventory[game]['price']}")
    else:
        messagebox.showwarning("Sin stock", f"{game} está agotado. Por favor, repón el inventario.")

# Function to restock inventory
def restock(game):
    inventory[game]["stock"] += 5

    # Update the database
    cur.execute("UPDATE inventory SET stock = %s WHERE game = %s", (inventory[game]["stock"], game))
    conn.commit()

    update_display()
    messagebox.showinfo("Inventario repuesto", f"Se han añadido 5 unidades de {game}.")

# Function to update the display
def update_display():
    for game, widgets in display_widgets.items():
        widgets["stock_label"].config(text=f"Stock: {inventory[game]['stock']}")
    revenue_label.config(text=f"Total recaudado: ${total_revenue}")

# Create the main window
root = tk.Tk()
root.title("Simulación - Tienda de Videojuegos")

# Set the size of the window
window_width = 900
window_height = 700

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)

# Set the geometry of the window
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
root.configure(bg="#2C3E50")

# Title label
title_label = tk.Label(root, text="Tienda de Videojuegos", font=("Helvetica", 20, "bold"), fg="white", bg="#2C3E50", pady=10)
title_label.pack()

# Widgets for each game
display_widgets = {}

for idx, (game, data) in enumerate(inventory.items()):
    frame = tk.Frame(root, bg="#34495E", pady=10, padx=10, relief="groove", borderwidth=2)
    frame.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(frame, text=game, font=("Helvetica", 16, "bold"), fg="white", bg="#34495E").pack(anchor="w")
    price_label = tk.Label(frame, text=f"Precio: ${data['price']}", font=("Helvetica", 14), fg="#E74C3C", bg="#34495E")
    price_label.pack(anchor="w")

    stock_label = tk.Label(frame, text=f"Stock: {data['stock']}", font=("Helvetica", 14), fg="#1ABC9C", bg="#34495E")
    stock_label.pack(anchor="w")

    btn_frame = tk.Frame(frame, bg="#34495E")
    btn_frame.pack(anchor="w")

    purchase_btn = tk.Button(btn_frame, text="Comprar", command=lambda g=game: purchase(g), bg="#E67E22", fg="white", font=("Helvetica", 12), padx=10, pady=5)
    purchase_btn.pack(side=tk.LEFT, padx=5)

    restock_btn = tk.Button(btn_frame, text="Reponer", command=lambda g=game: restock(g), bg="#3498DB", fg="white", font=("Helvetica", 12), padx=10, pady=5)
    restock_btn.pack(side=tk.LEFT, padx=5)

    # Save references for dynamic updates
    display_widgets[game] = {"price_label": price_label, "stock_label": stock_label}

# Label to display total revenue
revenue_label = tk.Label(root, text=f"Total recaudado: ${total_revenue}", font=("Helvetica", 16, "bold"), fg="white", bg="#2C3E50", pady=10)
revenue_label.pack()

# Run the application
update_display()
root.mainloop()

# Close the database connection when the GUI is closed
cur.close()
conn.close()
