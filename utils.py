from sys import stdout as terminal
from time import sleep
from itertools import cycle
from threading import Thread
from rich.console import Console

console = Console()

class LoadingAnimation:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.done = False
        self.thread = None

    def animate(self):
        for c in cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            terminal.write(f'\r{self.prefix}{c}')
            terminal.flush()
            sleep(0.1)
        terminal.write('\r' + ' ' * 50 + '\r') 
        terminal.flush()

    def start(self):
        self.done = False
        self.thread = Thread(target=self.animate)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.done = True
        if self.thread:
            self.thread.join()
