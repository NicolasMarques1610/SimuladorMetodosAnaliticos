import numpy as np

class QueueNetwork:
    def __init__(self, queues):
        self.queues = {queue.id: queue for queue in queues}  # Use a dictionary to access queues by ID

    def simulate(self, num_events, start_time):
        time = start_time
        initial_queue = self.queues[1]
        initial_queue.process_arrival(time)
        for _ in range(num_events-1):
            time += np.random.exponential(1)  # Increment time by an exponential distribution

            # Simulate the process for each queue
            for queue in self.queues.values():
                # Process arrivals based on each queue's arrival interval
                if np.random.random() < np.random.uniform(*queue.arrival_interval_range):
                    queue.process_arrival(time)
                queue.start_service(time)
                queue.process_departures(time, self.queues)
        self.total_time = time - start_time

    def save_events_to_file(self, filename):
        with open(filename, "w") as file:
            for queue in self.queues.values():
                for event in queue.events:
                    file.write(event + "\n")
                queue.events = []  # Clear events after writing

    def print_statistics(self):
        for queue in self.queues.values():
            stats = queue.statistics()
            print(f"\nEstatísticas da Fila {queue.id}:")
            print(f"Percentual de Perda: {stats[0]:.2f}%")
            print(f"Percentual de Completude: {stats[1]:.2f}%")
            print(f"Total de Clientes: {stats[2]}")
            print(f"Tempo Médio de Serviço: {stats[3]:.2f}")
        
        print(f"\nTempo Total da Simulação: {self.total_time:.2f} segundos")
