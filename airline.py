import tkinter as tk
from tkinter import messagebox, ttk

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, city):
        if city not in self.nodes:
            self.nodes[city] = []

    def add_edge(self, source, destination, cost, flight_name):
        self.nodes[source].append({"destination": destination, "cost": cost, "flight_name": flight_name})
        self.nodes[destination].append({"destination": source, "cost": cost, "flight_name": flight_name})

    def dijkstra(self, start, end):
        distances = {city: float('inf') for city in self.nodes}
        previous = {city: None for city in self.nodes}
        flight_details = {city: None for city in self.nodes}
        distances[start] = 0
        queue = set(self.nodes)

        while queue:
            min_city = min(queue, key=lambda city: distances[city])
            queue.remove(min_city)

            if min_city == end:
                break

            for neighbor in self.nodes[min_city]:
                new_distance = distances[min_city] + neighbor['cost']
                if new_distance < distances[neighbor['destination']]:
                    distances[neighbor['destination']] = new_distance
                    previous[neighbor['destination']] = min_city
                    flight_details[neighbor['destination']] = {
                        "flight_name": neighbor['flight_name'],
                        "cost": neighbor['cost']
                    }

        path = []
        flights_used = []
        current = end
        while current:
            path.insert(0, current)
            if flight_details[current]:
                flights_used.insert(0, flight_details[current])
            current = previous[current]

        return {"path": path, "cost": distances[end], "flights_used": flights_used}

# GUI Setup
def find_flights():
    source = source_var.get()
    destination = destination_var.get()

    if source == destination:
        messagebox.showwarning("Invalid Selection", "Source and Destination cannot be the same.")
        return

    result = airline.dijkstra(source, destination)
    if not result["path"] or result["cost"] == float('inf'):
        result_label.config(text="No available flights")
        return

    output = "All Available Flights:\n"
    for flight in result["flights_used"]:
        is_cheapest = flight["cost"] == result["cost"]
        output += f"{'CHEAPEST: ' if is_cheapest else ''}Flight: {flight['flight_name']} | Cost: ${flight['cost']}\n"

    result_label.config(text=output)

# Cities and Routes
cities = ["Mumbai", "Goa", "Delhi", "Bangalore", "Chennai"]
airline = Graph()
for city in cities:
    airline.add_node(city)

airline.add_edge("Mumbai", "Goa", 300, "Flight A")
airline.add_edge("Mumbai", "Goa", 250, "Flight B")
airline.add_edge("Mumbai", "Delhi", 400, "Flight C")
airline.add_edge("Delhi", "Bangalore", 350, "Flight D")
airline.add_edge("Bangalore", "Chennai", 200, "Flight E")

# Tkinter Window
root = tk.Tk()
root.title("Airline Reservation System")
root.geometry("400x400")
root.configure(bg="#f4f4f4")

container = tk.Frame(root, bg="white", bd=2, relief="groove", padx=20, pady=20)
container.pack(pady=40)

tk.Label(container, text="Airline Reservation System", font=("Arial", 16), bg="white").pack(pady=10)

tk.Label(container, text="Select Source:", bg="white").pack()
source_var = tk.StringVar()
source_menu = ttk.Combobox(container, textvariable=source_var, values=cities, state="readonly")
source_menu.pack()

tk.Label(container, text="Select Destination:", bg="white").pack()
destination_var = tk.StringVar()
destination_menu = ttk.Combobox(container, textvariable=destination_var, values=cities, state="readonly")
destination_menu.pack()

find_btn = tk.Button(container, text="Find Flights", command=find_flights, bg="#007bff", fg="white")
find_btn.pack(pady=10)

result_label = tk.Label(container, text="", bg="white", justify="left", wraplength=350)
result_label.pack(pady=10)

root.mainloop()
