class Block:
    _BLOCK_LENGTH = 50

    def __init__(self, block_id, position):
        self.id = block_id
        self.length = Block._BLOCK_LENGTH
        self.position = position
        self.position_in_frame = None
        self.alive = True
