class Block:
    def __init__(self, block_id, position):
        self.id = block_id
        self.alive = True
        self.position = position
        self.position_in_frame = None
        self.length = 50