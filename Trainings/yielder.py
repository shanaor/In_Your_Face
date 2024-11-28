import csv
import threading
from queue import Queue

# Create a CSV file with tokens
def create_csv(filename, tokens):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Token"])
        for token in tokens:
            writer.writerow([token])

# Generator function to yield tokens from a CSV file
def token_generator(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            yield row[0]

# Thread function to process tokens
def process_tokens(thread_name, queue):
    while not queue.empty():
        token = queue.get()
        print(f"{thread_name} processed token: {token}")
        queue.task_done()

# Function to create and run a thread for token processing
def create_thread(thread_name, queue):
    thread = threading.Thread(target=process_tokens, args=(thread_name, queue))
    thread.start()
    return thread

# Main function
def main():
    # CSV file and tokens
    csv_file = "tokens.csv"
    tokens = [f"Token{i}" for i in range(1, 21)]
    
    # Create the CSV file
    create_csv(csv_file, tokens)

    # Initialize the generator and a queue for thread-safe processing
    gen = token_generator(csv_file)
    token_queue = Queue()

    # Preload the queue with tokens from the generator
    for token in gen:
        token_queue.put(token)

    # Create and start threads separately
    thread1 = create_thread("Thread-1", token_queue)
    thread2 = create_thread("Thread-2", token_queue)

    # Wait for threads to complete
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()