# Consistent Hashing configuration
import hashlib


class ConsistentHashing:
    def init(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = dict()

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._get_key(f"{node}-{i}")
            self.ring[key] = node

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self._get_key(f"{node}-{i}")
            del self.ring[key]

    def get_node(self, key):
        if not self.ring:
            return None

        hashed_key = self._get_key(key)
        keys = sorted(self.ring.keys())
        for ring_key in keys:
            if hashed_key <= ring_key:
                return self.ring[ring_key]

        # If the key is greater than all keys in the ring, return the first node
        return self.ring[keys[0]]

    def _get_key(self, value):
        return int(hashlib.md5(value.encode()).hexdigest(), 16)

