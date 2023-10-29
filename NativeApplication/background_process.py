import threading, functools
def background(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        speak_thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        speak_thread.start()
    return wrapper
