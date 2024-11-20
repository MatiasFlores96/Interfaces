import tkinter as tk
from tkinter import messagebox
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="videogame_store",
    user="postgres",
    password="yourpassword"  # Use the same password you set earlier
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

# Widgets for each game
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

    # Save references for dynamic updates
    display_widgets[game] = {"price_label": price_label, "stock_label": stock_label}

# Label to display total revenue
revenue_label = tk.Label(root, text=f"Total recaudado: ${total_revenue}", font=("Arial", 14), pady=10)
revenue_label.pack()

# Run the application
update_display()
root.mainloop()

# Close the database connection when the GUI is closed
cur.close()
conn.close()
