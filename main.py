import yaml
from queue_1 import Queue
from queue_network import QueueNetwork

def read_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = read_config('config.yml')
    queues = []

    for queue_config in config['queue_configurations']:
        queue = Queue(
            id=queue_config['id'],
            service_interval_range=queue_config['service_interval_range'],
            servers=queue_config['servers'],
            arrival_interval_range=queue_config['arrival_interval_range'],
            capacity=queue_config.get('capacity')  # Usa get para tratar casos onde 'capacity' não é fornecido
        )
        for route in queue_config.get('routes', []):
            queue.add_destination(route['destination'], route['probability'])
        queues.append(queue)

    network = QueueNetwork(queues)
    num_events = int(config['events_number'])
    start_time = float(config['start_time'])

    network.simulate(num_events, start_time)

    events_file_path = config['logs_file']
    network.save_events_to_file(events_file_path)
    print(f"\nEventos salvos em: {events_file_path}")

    network.print_statistics()

if __name__ == "__main__":
    main()