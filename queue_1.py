import numpy as np
import random

class Queue:
    def __init__(self, id, service_interval_range, servers, arrival_interval_range, capacity=None):
        self.id = id
        self.service_interval_range = service_interval_range
        self.servers = servers
        self.capacity = capacity if capacity is not None else float('inf')
        self.arrival_interval_range = arrival_interval_range
        self.queue = []
        self.in_service = []
        self.completed = 0
        self.lost = 0
        self.total_service_time = 0
        self.total_wait_time = 0
        self.customer_id = 0
        self.events = []
        self.destinations = []
        self.state_times = {}
        self.last_event_time = 0
        self.max_tracked_customers = 4  

    def add_destination(self, destination_id, probability):
        self.destinations.append((destination_id, probability))

    def process_arrival(self, time, external=True):
        self.update_state_times(time)
        if len(self.queue) < self.capacity:
            if len(self.queue) in self.state_times:
                self.state_times[len(self.queue)] += time - self.last_event_time
        self.last_event_time = time

        if self.arrival_interval_range and external:
            if np.random.random() < np.random.uniform(*self.arrival_interval_range):
                self._add_customer(time)
        else:
            self._add_customer(time)

    def _add_customer(self, time):
        self.customer_id += 1
        if len(self.queue) + len(self.in_service) < self.capacity:
            self.queue.append((self.customer_id, time, time))
            self.events.append(f"[Tempo {time:.2f}]: Cliente {self.customer_id} chegou à Fila {self.id}")
        else:
            self.lost += 1
            self.events.append(f"[Tempo {time:.2f}]: Cliente {self.customer_id} perdido na Fila {self.id}")

    def start_service(self, current_time):
        self.update_state_times(current_time)
        if len(self.queue) < self.capacity:
            if len(self.queue) in self.state_times:
                self.state_times[len(self.queue)] += current_time - self.last_event_time
        self.last_event_time = current_time

        while len(self.in_service) < self.servers and self.queue:
            customer_id, arrival_time, entered_queue_time = self.queue.pop(0)
            wait_time = current_time - entered_queue_time
            self.total_wait_time += wait_time  
            service_time = np.random.uniform(*self.service_interval_range)
            departure_time = current_time + service_time
            self.total_service_time += service_time 
            self.in_service.append((customer_id, departure_time))
            self.events.append(f"[Tempo {current_time:.2f}]: Cliente {customer_id} iniciou o serviço na Fila {self.id}")

    def update_state_times(self, current_time):
        current_state = len(self.queue) + len(self.in_service)
        if self.id == 1: 
            if current_state > self.max_tracked_customers:
                return
        if current_state not in self.state_times:
            self.state_times[current_state] = 0
        elapsed_time = current_time - self.last_event_time
        self.state_times[current_state] += elapsed_time
        self.last_event_time = current_time

    def process_departures(self, current_time, queues_dict):
        self.update_state_times(current_time)
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
                if destination_id == -1:
                    self.events.append(f"[Tempo {current_time:.2f}]: Cliente saiu do sistema a partir da Fila {self.id}")
                    return
                else: 
                    queues_dict[destination_id].process_arrival(current_time)
                    return

    def generate_service_time(self):
        return np.random.uniform(*self.service_interval_range)

    def statistics(self, total_simulation_time):
        total_time = sum(self.state_times.values())
        probabilities = {state: (time / total_time) * 100 if total_time else 0 for state, time in self.state_times.items()}
        return {
            "lost": self.lost,
            "total_wait_time": self.total_wait_time,
            "total_service_time": self.total_service_time,
            "probabilities": probabilities,
            "state_times": self.state_times
        }