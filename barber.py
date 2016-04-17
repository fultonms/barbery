import threading, time, random

CUSTOMERS = 256
BARBERS = 4

ARRIVAL_WAIT = 0.05

def wait():
    time.sleep(ARRIVAL_WAIT * random.random())

class Barber(threading.Thread):
    condition = threading.Condition()
    customers = []
    should_stop = threading.Event()

    def run(self):
        while True:
            with self.condition:
                if not self.customers:
                    print "{} is sleeping.".format(self)
                    self.condition.wait()
                if self.should_stop.is_set():
                    return
                if not self.customers:
                    print "{} woke up, but has no customers.".format(self)
                    continue

                customer = self.customers.pop()
                print "{} is waking up to service {}.".format(self, customer)
            customer.snipSnip()


class Customer(threading.Thread):
    WAIT = 0.05
    serviced = None

    def wait(self):
        time.sleep(self.WAIT * random.random())

    def snipSnip(self):
        print "{} is getting a haircut cut.".format(self)
        self.wait()
        self.serviced.set()

    def run(self):
        self.serviced = threading.Event()

        with Barber.condition:
            Barber.customers.append(self)
            Barber.condition.notify(1)

        print "{} has fallen asleep while waiting.".format(self)
        self.serviced.wait()
        print "{} is leaving!".format(self)


def main():
    print "Opening Shop!"

    for b in range(BARBERS):
        Barber().start()

    customers = []

    for c in range(CUSTOMERS):
        wait()
        c = Customer()
        customers.append(c)
        c.start()
        print "{} has arrived.".format(c)

    for c in customers:
        c.join()

    print "\nNo more customers left!"

    Barber.should_stop.set()

    with Barber.condition:
        Barber.condition.notify_all()

    print "Closing shop!\n"

if __name__ == "__main__":
    main()
