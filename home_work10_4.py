import queue
import threading
from threading import Thread
import random
import time
from queue import Queue

class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        time.sleep(random.randint(3, 10))
class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = Queue()
    def guest_arrival(self, *guests):
        self.guests = guests
        def set_guest(guest):
            for y in self.tables:
                if y.guest is None:
                    y.guest = guest.name
                    return y
        for x in self.guests:
            if any(y.guest is None for y in self.tables):
                table_occupy = set_guest(x)
                print(f'{x.name} сел(-а) за стол номер {table_occupy.number}')
                x.start()
            if not x.is_alive() and all(y.guest != None for y in self.tables):
                self.queue.put(x)
                print(f'{x.name} в очереди')
    def discuss_guests(self):
        thread_alive = [x for x in self.guests if x.is_alive()]
        while thread_alive:
            for x in thread_alive:
                if not x.is_alive():
                    free_table = next(filter(lambda y: y.guest == x.name, self.tables), None)
                    print(f'{x.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер  свободен {free_table.number}')
                    thread_alive.remove(x)
                    free_table.guest = None
                    if not self.queue.empty():
                        queve_guest = self.queue.queue[0]
                        free_table.guest = queve_guest.name
                        thread_alive.append(queve_guest)
                        self.queue.get()
                        thguest = next(filter(lambda y: y.name == queve_guest.name, self.guests), None)
                        thguest.start()
                        print(f'{thguest.name} вышел(-ла) из очереди и сел(-а) за стол {free_table.number}')



# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
cafe.discuss_guests()


