import threading
import time

# Function that causes a delay using a large FOR loop
def delayed_loop():
    print("Start of delayed loop")
    for _ in range(10**8):  # A large loop causing delay
        pass
    print("End of delayed loop")

# Function that prints messages to the terminal
def print_messages():
    for i in range(10):
        print(f"Message {i+1} from the print thread")
        time.sleep(0.5)  # Small delay to make prints readable

# Create threads
thread1 = threading.Thread(target=delayed_loop)
thread2 = threading.Thread(target=print_messages)

# Start threads
thread1.start()
thread2.start()

# Wait for threads to finish
thread1.join()
thread2.join()

print("All threads completed.")
