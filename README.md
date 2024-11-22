# Interfaces
# Video Game Store Simulation 🎮

This project is an interactive simulation of a video game store developed in Python using the **Tkinter** library for the graphical user interface. It allows users to buy fictional video games, manage inventory, and observe real-time updates of total revenue and available stock.

---

## Features

- Three video games available for purchase:
  - **The Legend of Zelda: Breath of the Wild** - Price: $70
  - **Elden Ring** - Price: $60
  - **Stardew Valley** - Price: $20
- Dynamic inventory management:
  - Users can buy video games.
  - Inventory updates automatically.
  - Option to restock inventory when items are sold out.
- Real-time display of total revenue.

---

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/your_username/video-game-store.git
cd video-game-store
```

### 2. Set Up PostgreSQL with Docker

1. **Install Docker**  
   If Docker is not installed on your system, download and install it from [Docker's official website](https://www.docker.com/).

2. **Pull the PostgreSQL Docker Image**

   ```bash
   docker pull postgres
   ```

3. **Run the PostgreSQL Container on a Non-Default Port (5433)**

   ```bash
   docker run --name videogame_store_db -e POSTGRES_PASSWORD=yourpassword -p 5433:5432 -d postgres
   ```

  - Replace `yourpassword` with a secure password.
  - This command maps port **5433** on your host to port **5432** inside the container.

4. **Set Up the Database**

   Access the PostgreSQL container to create the required database and tables:

   ```bash
   docker exec -it videogame_store_db psql -U postgres
   ```

   Then run the following SQL commands:

   ```sql
   -- Create the database
   CREATE DATABASE videogame_store;
   ```
   ```sql
   \c videogame_store;
   ```
   ```sql
   -- Create the inventory table
   CREATE TABLE inventory (
       game VARCHAR(100) PRIMARY KEY,
       price INTEGER,
       stock INTEGER
   );
   ```
   ```sql
   -- Create the total revenue table
   CREATE TABLE total_revenue (
       id SERIAL PRIMARY KEY,
       revenue INTEGER
   );
   ```
   ```sql
   -- Initialize total revenue
   INSERT INTO total_revenue (revenue) VALUES (0);
   ```
   ```sql
   -- Insert initial inventory data
   INSERT INTO inventory (game, price, stock) VALUES
   ('The Legend of Zelda: Breath of the Wild', 70, 10),
   ('Elden Ring', 60, 8),
   ('Stardew Valley', 20, 15);
   ```

   Exit the container:

   ```bash
   \q
   ```

### 3. Install Python Dependencies

Ensure you have Python 3.8+ installed, then install the required library:

```bash
pip install psycopg2-binary tk
```

### 4. Run the Application

Execute the script:

```bash
python video_game_store.py
```

The graphical user interface will launch, allowing you to interact with the video game store simulation.

---

## Usage

- **Buy Video Games:** Click "Comprar" to purchase a game. The stock and total revenue update automatically.
- **Restock Inventory:** Click "Reponer" to add more stock for a specific game.
- The interface displays real-time updates for game prices, stock levels, and total revenue.

---

## Notes

- The database is persisted in the Docker container. If the container is removed, the data will be lost unless configured with a volume for persistent storage.
- Ensure Docker is running and the PostgreSQL container is active before starting the application.

