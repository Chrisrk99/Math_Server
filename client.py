from xmlrpc.client import ServerProxy
from concurrent.futures import ThreadPoolExecutor
import random
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def reset_counts(server_address):
    """Reset the operation counts on the server before starting new tests."""
    proxy = ServerProxy(server_address, allow_none=True)
    try:
        success = proxy.reset_operation_counts()
        if success:
            logging.info("Operation counts reset successfully.")
        else:
            logging.error("Failed to reset operation counts.")
    except Exception as e:
        logging.error(f"Failed to communicate with server to reset counts: {str(e)}")

def make_request(server_address, operation):
    """Make a single XML-RPC request to the server."""
    proxy = ServerProxy(server_address, allow_none=True)
    try:
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        z = random.randint(1, 100)
        if operation in ['magicAdd', 'magicSubtract']:
            result = proxy.__getattr__(operation)(x, y)
        else:
            result = proxy.__getattr__(operation)(x, y, z)
        logging.info(f"Executed {operation} with result: {result}")
    except Exception as e:
        logging.error(f"Error during request {operation}: {e.__class__.__name__} - {str(e)}")

def main():
    server_address = 'http://localhost:8000/'
    reset_counts(server_address)  # Reset counts before starting new tests
    operations = ['magicAdd', 'magicSubtract', 'magicFindMin', 'magicFindMax']
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, server_address, random.choice(operations)) for _ in range(100)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Exception in thread: {str(e)}")

    # Fetch the final operation counts after all requests are done
    proxy = ServerProxy(server_address, allow_none=True)
    try:
        operation_count = proxy.get_operation_count()
        logging.info(f"Final operation counts: {operation_count}")
    except Exception as e:
        logging.error(f"Failed to fetch operation counts: {str(e)}")

if __name__ == '__main__':
    main()
