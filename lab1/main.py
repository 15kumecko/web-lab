from creational.singleton import Singleton
from structural.adapter import Adaptee, Adapter
from behavioral.observer import Subject, Observer

def main():
    s1 = Singleton()
    s2 = Singleton()
    print(f"Singleton test (same instance): {s1 is s2}")

    adaptee = Adaptee()
    adapter = Adapter(adaptee)
    print(f"Adapter test: {adapter.request()}")

    subject = Subject()
    observer1 = Observer()
    subject.attach(observer1)
    subject.notify("System update")

if __name__ == "__main__":
    main()
