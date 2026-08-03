# Low-Level Design (LLD) & Object-Oriented Design (OOD) Reference

This reference covers standard Object-Oriented Design patterns and solutions for core LLD components, complementing High-Level System Design.

---

## SOLID Principles Summary

- **S — Single Responsibility Principle (SRP)**: A class should have only one reason to change.
- **O — Open/Closed Principle (OCP)**: Software entities should be open for extension, but closed for modification.
- **L — Liskov Substitution Principle (LSP)**: Subtypes must be substitutable for their base types without altering correctness.
- **I — Interface Segregation Principle (ISP)**: Clients should not be forced to depend on interfaces they do not use.
- **D — Dependency Inversion Principle (DIP)**: High-level modules should not depend on low-level modules; both should depend on abstractions.

---

## Canonical OOD Worked Examples

### 1. Design a Least Recently Used (LRU) Cache

**Requirements**:
- `get(key)`: Get value of key if key exists in cache, otherwise return -1. Time complexity: O(1).
- `put(key, value)`: Update or insert key-value pair. If capacity exceeded, evict the least recently used item. Time complexity: O(1).

**Design**:
Hash Map + Doubly Linked List.
- Hash Map maps `key -> Node` for O(1) lookup.
- Doubly Linked List maintains access order: Most Recently Used (MRU) at head, Least Recently Used (LRU) at tail.

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict LRU from tail
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
```

---

### 2. Design a Parking Lot

**Requirements**:
- Support multiple levels, each level with multiple spots.
- Spot sizes: Motorcycle, Compact, Large.
- Vehicle types: Motorcycle (fits any spot), Car (compact or large), Bus (requires 5 contiguous large spots).
- Operations: `park_vehicle(vehicle)`, `unpark_vehicle(vehicle)`.

**Class Design**:
- `Vehicle` (Abstract) -> `Motorcycle`, `Car`, `Bus`
- `ParkingSpot` -> tracks size, row, spot_number, level, current_vehicle
- `Level` -> manages collection of `ParkingSpot`s
- `ParkingLot` (Singleton) -> manages collection of `Level`s

```python
from enum import Enum

class VehicleSize(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3

class Vehicle:
    def __init__(self, license_plate: str, spots_needed: int, size: VehicleSize):
        self.license_plate = license_plate
        self.spots_needed = spots_needed
        self.size = size
        self.parking_spots = []

    def can_fit_in_spot(self, spot):
        pass

class ParkingSpot:
    def __init__(self, level, row: int, spot_number: int, spot_size: VehicleSize):
        self.level = level
        self.row = row
        self.spot_number = spot_number
        self.spot_size = spot_size
        self.vehicle = None

    def is_available(self) -> bool:
        return self.vehicle is None

    def park(self, vehicle: Vehicle) -> bool:
        if not self.is_available() or not vehicle.can_fit_in_spot(self):
            return False
        self.vehicle = vehicle
        vehicle.parking_spots.append(self)
        return True

    def remove_vehicle(self):
        for spot in self.vehicle.parking_spots:
            spot.vehicle = None
        self.vehicle.parking_spots.clear()
```

---

### 3. Design a Hash Map (Chaining Technique)

**Requirements**:
- `put(key, value)`
- `get(key)`
- `remove(key)`
- Handle hash collisions via Separate Chaining (LinkedList per bucket).

```python
class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    def __init__(self, capacity=10007):
        self.capacity = capacity
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        idx = self._hash(key)
        head = self.buckets[idx]
        curr = head
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next
        new_node = HashNode(key, value)
        new_node.next = head
        self.buckets[idx] = new_node

    def get(self, key):
        idx = self._hash(key)
        curr = self.buckets[idx]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return -1

    def remove(self, key):
        idx = self._hash(key)
        curr = self.buckets[idx]
        prev = None
        while curr:
            if curr.key == key:
                if prev:
                    prev.next = curr.next
                else:
                    self.buckets[idx] = curr.next
                return
            prev = curr
            curr = curr.next
```

---

### 4. Design Patterns Cheatsheet

| Pattern | Type | Intent | Example in System Design |
|---|---|---|---|
| Singleton | Creational | Single instance globally | Connection pool, Logger, Config Manager |
| Factory Method | Creational | Interface for creating objects | Storage driver factory (S3, GCS, Local) |
| Strategy | Behavioral | Encapsulate interchangeable algorithms | Load balancing strategy (RR, LeastConn, Hash) |
| Observer | Behavioral | Event notification mechanism | Pub/Sub event bus, metrics collectors |
| Decorator | Structural | Attach responsibilities dynamically | Middleware (Auth, Rate Limit, Compression) |
| Circuit Breaker | Structural / Behavioral | Prevent cascading failures | Resilient HTTP/RPC clients |
