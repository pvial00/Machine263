class Rotor:
    def __init__(self, k, rid):
        self.s = range(26)
        self.rid = rid
        klen = len(k)
        c = 0
        j = (rid + k[0])
        for x in xrange(klen):
            j = (j + k[x]) % 26
        i = 0
        rnds = (26 * rid) + rid + j
        for x in xrange(rnds):
            k[i] = (k[i] + self.s[j]) % 26
            j = (j + self.s[j] + k[i] + rid) % 26
            self.s[c], self.s[j] = self.s[j], self.s[c]
            c = (c + 1) % 26
            i = (i + 1) % klen

        self.k = 0
        for x in xrange(klen):
            self.k = (self.k + k[x]) % 26

        self.i = 0
        self.c = j
        self.notch = j

    def encipher(self, num):
        self.k = (self.k + self.s[self.k]) % 26
        return (self.s[self.k] + self.s[self.c] + num) % 26

    def decipher(self, num):
        self.k = (self.k + self.s[self.k]) % 26
        return (num - self.s[self.k] - self.s[self.c]) % 26

    def _clock(self):
        self.c = (self.c + 1) % 26
        self.s[self.c], self.s[self.k] = self.s[self.k], self.s[self.c]

class Wiring:
    def __init__(self, nrotors):
        self.n = nrotors
        self.r = []
        self.e = []

    def tonums(self, string):
        a = []
        for char in string:
            num = ord(char) - 65
            a.append(num)
        return a

    def rotorsetup(self, key):
        k = self.tonums(key)
        for rid in xrange(self.n):
            k = self._prock(k, (rid + 1))
            self.r.append(Rotor(k, (rid + 1)))

    def resetrotors(self):
        self.r = []
        
    def _prock(self, k, rid):
        for x in xrange(len(k)):
            k[x] = (k[x] + rid) % 26 
        return k

    def fillentropy(self, key):
        t = ""
        for x in xrange(1000):
            t += "A"
        t = self.encrypt(t, key)
        return self.tonums(t)

    def encrypt(self, chars, key):
        ctxt = []
        self.rotorsetup(key)
        for char in chars:
            num = ord(char) - 65
            for r in xrange(self.n):
                if self.r[r].c == self.r[r].notch:
                    self.r[(r+1) % self.n]._clock()
                num = self.r[r].encipher(num)
            ctxt.append(chr(num + 65))
        self.resetrotors()
        return "".join(ctxt)
    
    def decrypt(self, chars, key):
        ctxt = []
        self.rotorsetup(key)
        for char in chars:
            num = ord(char) - 65
            for r in range(self.n):
                if self.r[r].c == self.r[r].notch:
                    self.r[(r+1) % self.n]._clock()
                num = self.r[r].decipher(num)
            ctxt.append(chr(num + 65))
        self.resetrotors()
        return "".join(ctxt)

class Machine:
    nrotors = 3
    def __init__(self):
        self.wiring = Wiring(self.nrotors)

    def encrypt(self, msg, key):
        return self.wiring.encrypt(msg, key)
    
    def decrypt(self, msg, key):
        return self.wiring.decrypt(msg, key)
