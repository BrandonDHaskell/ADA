import threading

class SharedVariable:
    """
    SharedVariable is a thread-safe class used for sharing data between different
    threads in the ADA project. This is particularly used for sharing state changes
    detected by hardware monitoring interfaces like ContinuousMonitoringInterface.

    Thread Safety:
    - Access to the variable is controlled via a threading.Lock to prevent
      concurrent access issues in a multi-threaded environment.

    Usage:
    - Set the value using shared_variable.set(value)
    - Read the value using value = shared_variable.get()
    - Reset the value to None using shared_variable.reset()

    Example:
    shared_variable = SharedVariable()
    shared_variable.set('new_state')
    state = shared_variable.get()
    shared_variable.reset()

    Integration:
    - SharedVariable instances should be passed to components (like hardware
      monitors) that need to communicate state changes back to the main thread.

    Note:
    - Care should be taken to avoid deadlocks by ensuring that the locks are
      properly released after use.
    - Be aware of the potential for stale data if the variable is not regularly
      checked and reset in the main thread.
    """

    def __init__(self):
        self.value = None
        self.lock = threading.Lock()

    def set(self, value):
        with self.lock:
            self.value = value

    def get(self):
        with self.lock:
            return self.value

    def reset(self):
        with self.lock:
            self.value = None
