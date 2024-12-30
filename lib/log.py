import os,sys
import inspect

def log(message):
    # Ottieni lo stack corrente
    stack = inspect.stack()
    # La funzione chiamante è nello stack al livello 1
    caller_frame = stack[1]
    caller_function = caller_frame.function
    
    # Se è dentro una classe, ottieni il nome della classe
    caller_class = None
    if 'self' in caller_frame.frame.f_locals:
        caller_class = type(caller_frame.frame.f_locals['self']).__name__
    
    if caller_class:
        print(f"[{caller_class}.{caller_function}] {message}")
    else:
        print(f"[{caller_function}] {message}")