import numpy as np

class QueueNetwork:
    def __init__(self, queues):
        self.queues = {queue.id: queue for queue in queues}
        self.total_time = 0

    def simulate(self, num_events, start_time):
        time = start_time
        for _ in range(num_events):
            time += np.random.exponential(0.3934)
            if 'arrival_interval_range' in self.queues[1].__dict__:
                self.queues[1].process_arrival(time, external=True)
            for queue in self.queues.values():
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
        total_simulation_time = self.total_time  
        print("=" * 57)
        print("======================    REPORT   ======================")
        print("=" * 57)
        
        for queue in self.queues.values():
            stats = queue.statistics(total_simulation_time)  
            print("*" * 57)
            print(f"Queue: Q{queue.id} (G/G/{queue.servers}/{'' if queue.capacity == float('inf') else queue.capacity})")
            print(f"Arrival: {'N/A' if not queue.arrival_interval_range else f'{queue.arrival_interval_range[0]} ... {queue.arrival_interval_range[1]}'}")
            print(f"Service: {queue.service_interval_range[0]} ... {queue.service_interval_range[1]}")
            print("*" * 57)
            print("   State               Time               Probability")
            for state, time in stats['state_times'].items():
                prob = stats['probabilities'][state]
                print(f"      {state}           {time:10,.4f}                {prob:.2f}%")
            print("\nNumber of losses:", stats['lost'])
            print("*" * 57)

        print("=" * 57)
        print(f"Simulation average time: {total_simulation_time:.4f}")
        print("=" * 57)