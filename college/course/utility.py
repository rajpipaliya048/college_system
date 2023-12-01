import time
import random



def generate_unique_order_id():
    timestamp = int(time.time() * 1000)
    random_number = random.randint(1000, 9999)
    order_id = f"{timestamp}{random_number}"
    return order_id