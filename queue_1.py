import numpy as np
import random

class Queue:
    def __init__(self, id, service_interval_range, servers, arrival_interval_range, capacity=None):
        self.id = id
        self.service_interval_range = service_interval_range
        self.arrival_interval_range = arrival_interval_range
        self.servers = servers
        self.capacity = capacity if capacity is not None else float('inf') 
        self.queue = []
        self.in_service = []
        self.completed = 0
        self.lost = 0
        self.total_service_time = 0
        self.total_customers_arrived = 0
        self.customer_id = 0
        self.events = []
        self.destinations = []

    def add_destination(self, destination_id, probability):
        self.destinations.append((destination_id, probability))

    def process_arrival(self, time):
        if len(self.queue) + len(self.in_service) < self.capacity:
            self.queue.append((self.customer_id, time))
            self.customer_id += 1
            self.events.append(f"[Tempo {time:.2f}]: Cliente {self.customer_id} chegou à Fila {self.id}")
        else:
            self.lost += 1
            self.events.append(f"[Tempo {time:.2f}]: Cliente {self.customer_id} perdido na Fila {self.id}")

    def start_service(self, current_time):
        while len(self.in_service) < self.servers and self.queue:
            customer_id, arrival_time = self.queue.pop(0)
            service_time = np.random.uniform(*self.service_interval_range)
            departure_time = current_time + service_time
            self.in_service.append((customer_id, departure_time))
            self.total_service_time += service_time
            self.events.append(f"[Tempo {current_time:.2f}]: Cliente {customer_id} iniciou o serviço na Fila {self.id}")

    def process_departures(self, current_time, queues_dict):
        for customer_id, departure_time in list(self.in_service):
            if departure_time <= current_time:
                self.in_service.remove((customer_id, departure_time))
                self.completed += 1
                self.events.append(f"[Tempo {current_time:.2f}]: Cliente {customer_id} completou o serviço na Fila {self.id}")
                self.route_customer(current_time, queues_dict)

    def route_customer(self, current_time, queues_dict):
        random_prob = random.random()
        cumulative_probability = 0.0
        for destination_id, probability in self.destinations:
            cumulative_probability += probability
            if random_prob < cumulative_probability:
                if destination_id == -1:  # Caso o destino seja -1, o cliente sai do sistema
                    self.events.append(f"[Tempo {current_time:.2f}]: Cliente saiu do sistema a partir da Fila {self.id}")
                    return
                else:  # Processa a chegada na próxima fila
                    queues_dict[destination_id].process_arrival(current_time)
                    return

    def generate_service_time(self):
        return np.random.uniform(*self.service_interval_range)

    def statistics(self):
        total_customers = self.completed + self.lost
        percent_lost = (self.lost / total_customers * 100) if total_customers else 0
        percent_completed = (self.completed / total_customers * 100) if total_customers else 0
        average_service_time = (self.total_service_time / self.completed) if self.completed else 0
        return (percent_lost, percent_completed, total_customers, average_service_time)