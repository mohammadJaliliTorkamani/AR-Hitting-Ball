class Block:
    def __init__(self, block_id, position):
        self._id = block_id
        self.alive = True
        self.position = position
