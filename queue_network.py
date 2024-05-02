import numpy as np

class QueueNetwork:
    def __init__(self, queues):
        self.queues = {queue.id: queue for queue in queues}
        self.total_time = 0

    def simulate(self, num_events, start_time):
        time = start_time
        for _ in range(num_events):
            time += np.random.exponential(1)
            for queue in self.queues.values():
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
                queue.events = [] 

    def print_statistics(self):
        print("Detalhes da Simulação:")
        for queue in self.queues.values():
            stats = queue.statistics()
            print(f"\nEstatísticas da Fila {queue.id}:")
            print(f"Tempo Total de Espera: {stats['total_wait_time']:.2f} segundos")
            print(f"Tempo Total de Serviço: {stats['total_service_time']:.2f} segundos")
            print(f"Número de Perdas: {stats['lost']}")
            print("Probabilidades de Roteamento:")
            for dest, prob in stats['probabilities']:
                print(f"  Para fila {dest}: {prob * 100:.2f}%")
        print(f"\nTempo Global da Simulação: {self.total_time:.2f} segundos")
        print(f"Total de Perdas em Todas as Filas: {sum(queue.lost for queue in self.queues.values())}")
