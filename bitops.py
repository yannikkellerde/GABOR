from functools import reduce

class bit_reverser():
    def __init__(self):
        self.chunk_size = 9
        self.chunks = 4
        self.chunk_bits = (1 << self.chunk_size)-1
        self.lookup_table = {}
        for i in range(1 << self.chunk_size):
            self.lookup_table[i] = self.slow_reverse(i)

    def slow_reverse(self, num):
        count = self.chunk_size-1
        reverse_num = num
        num >>= 1
        while num:
            reverse_num <<= 1
            reverse_num |= num & 1
            num >>= 1
            count-=1
        reverse_num <<= count
        reverse_num &= (1 << self.chunk_size)-1
        return reverse_num

    def reverse(self, num):
        return (self.lookup_table[num&self.chunk_bits]<<27 |
                self.lookup_table[(num >> 9)&self.chunk_bits]<<18 |
                self.lookup_table[(num >> 18)&self.chunk_bits]<<9 |
                self.lookup_table[(num >> 27)&self.chunk_bits]
        )

class bit_transposer():
    def __init__(self):
        self.rows = 6
        self.chunk_bits = (1 << self.rows)-1
        self.lookup_table = {}
        for i in range(1 << self.rows):
            self.lookup_table[i] = self.slow_transpose(i)

    def slow_transpose(self, num):
        return (num&1)|((num&(1<<1))<<5)|((num&(1<<2))<<10)|((num&(1<<3))<<15)|((num&(1<<4))<<20)|((num&(1<<5))<<25)

    def transpose(self, num):
        return (self.lookup_table[num&self.chunk_bits] |
                self.lookup_table[(num>>6)&self.chunk_bits]<<1 |
                self.lookup_table[(num>>12)&self.chunk_bits]<<2 |
                self.lookup_table[(num>>18)&self.chunk_bits]<<3 |
                self.lookup_table[(num>>24)&self.chunk_bits]<<4 |
                self.lookup_table[(num>>30)&self.chunk_bits]<<5
        )

class mirror():
    def __init__(self):
        self.per_row = 6
        self.row_bits = [(2**(x+self.per_row)-1)-(2**x-1) for x in range(0,36,self.per_row)]
        self.column_bits = [reduce(lambda a,b:a|(2**((b*self.per_row)+x)), [c for c in range(self.per_row)], 0) for x in range(self.per_row)]

    def mirrory(self, num):
        return ((self.row_bits[0]&num)<<30 |
                (self.row_bits[1]&num)<<18 |
                (self.row_bits[2]&num)<<6 |
                (self.row_bits[3]&num)>>6 |
                (self.row_bits[4]&num)>>18 |
                (self.row_bits[5]&num)>>30
        )

    def mirrorx(self, num):
        return ((self.column_bits[0]&num)<<5 |
                (self.column_bits[1]&num)<<3 |
                (self.column_bits[2]&num)<<1 |
                (self.column_bits[3]&num)>>1 |
                (self.column_bits[4]&num)>>3 |
                (self.column_bits[5]&num)>>5
        )


class encoder():
    def __init__(self):
        self.rows = 6
        self.squares = self.rows**2
        self.prepowers = [3**i for i in range(self.squares)]

    def encode(self, pos):
        res = 0
        shifted = 1
        for i in range(self.squares):
            apow = self.prepowers[i]
            res += apow if pos[0]&shifted else 2*apow if pos[1]&shifted else 0
            shifted <<=1
        return res


class bitops():
    def __init__(self):
        self.bit_reverser = bit_reverser()
        self.bit_transposer = bit_transposer()
        self.mirror = mirror()
        self.encoder = encoder()
        self.reverse = self.bit_reverser.reverse
        self.transpose = self.bit_transposer.transpose
        self.mirrorx = self.mirror.mirrorx
        self.mirrory = self.mirror.mirrory
        self.encode = self.encoder.encode

    def ptranspose(self, p):
        return [self.transpose(p[0]), self.transpose(p[1])]

    def preverse(self, p):
        return [self.reverse(p[0]), self.reverse(p[1])]

    def pmirrorx(self, p):
        return [self.mirrorx(p[0]), self.mirrorx(p[1])]
    
    def pmirrory(self, p):
        return [self.mirrory(p[0]), self.mirrory(p[1])]