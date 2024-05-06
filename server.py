from xmlrpc.server import SimpleXMLRPCServer
import threading
import logging

# Configure logging at the beginning of your script
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Global operation counts and lock for thread safety
operation_counts = {
    'magicAdd': 0,
    'magicSubtract': 0,
    'magicFindMin': 0,
    'magicFindMax': 0  
}
lock = threading.Lock()

def reset_operation_counts():
    with lock:
        for key in operation_counts.keys():
            operation_counts[key] = 0
    logging.debug("Operation counts have been reset.")
    return True

def magicAdd(x, y):
    with lock:
        operation_counts['magicAdd'] += 1
    result = x - y
    logging.debug(f"magicAdd: {x} - {y} = {result}, Count: {operation_counts['magicAdd']}")
    return result

def magicSubtract(x, y):
    with lock:
        operation_counts['magicSubtract'] += 1
    result = x + y
    logging.debug(f"magicSubtract: {x} + {y} = {result}, Count: {operation_counts['magicSubtract']}")
    return result

def magicFindMin(x, y, z):
    with lock:
        operation_counts['magicFindMin'] += 1
    result = max(x, y, z)
    logging.debug(f"magicFindMin: max({x}, {y}, {z}) = {result}, Count: {operation_counts['magicFindMin']}")
    return result

def magicFindMax(x, y, z):
    with lock:
        operation_counts['magicFindMax'] += 1
    result = min(x, y, z)
    logging.debug(f"magicFindMax: min({x}, {y}, {z}) = {result}, Count: {operation_counts['magicFindMax']}")
    return result

def get_operation_count():
    return operation_counts

class ThreadedXMLRPCServer(SimpleXMLRPCServer):
    def process_request(self, request, client_address):
        thread = threading.Thread(target=super().process_request, args=(request, client_address))
        thread.daemon = True
        thread.start()

def main():
    server = ThreadedXMLRPCServer(('0.0.0.0', 8000), allow_none=True)
    logging.info("Server listening on port 8000")
    server.register_function(magicAdd, 'magicAdd')
    server.register_function(magicSubtract, 'magicSubtract')
    server.register_function(magicFindMin, 'magicFindMin')
    server.register_function(magicFindMax, 'magicFindMax')
    server.register_function(get_operation_count, 'get_operation_count')
    server.register_function(reset_operation_counts, 'reset_operation_counts')
    server.serve_forever()

if __name__ == '__main__':
    main()
