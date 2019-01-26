import copy

############## Unit Testing States ##################
state =  [ [0x19,0xa0,0x9a,0xe9],
            [0x3d,0xf4,0xc6,0xf8],
            [0xe3,0xe2,0x8d,0x48],
            [0xbe,0x2b,0x2a,0x08]];

testRound = [ [0xa4, 0x68, 0x6b, 0x02],
                [0x9c, 0x9f, 0x5b, 0x6a],
                [0x7f, 0x35, 0xea, 0x50],
                [0xf2, 0x2b, 0x43, 0x49]];
######################################################

Rcon = [ 0x00000000,
           0x01000000, 0x02000000, 0x04000000, 0x08000000,
           0x10000000, 0x20000000, 0x40000000, 0x80000000,
           0x1B000000, 0x36000000, 0x6C000000, 0xD8000000,
           0xAB000000, 0x4D000000, 0x9A000000, 0x2F000000,
           0x5E000000, 0xBC000000, 0x63000000, 0xC6000000,
           0x97000000, 0x35000000, 0x6A000000, 0xD4000000,
           0xB3000000, 0x7D000000, 0xFA000000, 0xEF000000,
           0xC5000000, 0x91000000, 0x39000000, 0x72000000,
           0xE4000000, 0xD3000000, 0xBD000000, 0x61000000,
           0xC2000000, 0x9F000000, 0x25000000, 0x4A000000,
           0x94000000, 0x33000000, 0x66000000, 0xCC000000,
           0x83000000, 0x1D000000, 0x3A000000, 0x74000000,
           0xE8000000, 0xCB000000, 0x8D000000]

Sbox = [
    [ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76 ] ,
    [ 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0 ] ,
    [ 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15 ] ,
    [ 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75 ] ,
    [ 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84 ] ,
    [ 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf ] ,
    [ 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8 ] ,
    [ 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2 ] ,
    [ 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73 ] ,
    [ 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb ] ,
    [ 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79 ] ,
    [ 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08 ] ,
    [ 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a ] ,
    [ 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e ] ,
    [ 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf ] ,
    [ 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 ]
    ];

InvSbox = [
    [ 0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb ] ,
    [ 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb ] ,
    [ 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e ] ,
    [ 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 ] ,
    [ 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92 ] ,
    [ 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 ] ,
    [ 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06 ] ,
    [ 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b ] ,
    [ 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73 ] ,
    [ 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e ] ,
    [ 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ] ,
    [ 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4 ] ,
    [ 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f ] ,
    [ 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef ] ,
    [ 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 ] ,
    [ 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d ]
    ];

#ffAdd() - adds two finite fields (see Section 4.1)
#I don't really ever use this since in Python it's just ^, but I figured I should include it
def ffAdd(a, b): return a ^ b

#xtime() - multiplies a finite field by x (see Section 4.2.1)
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

#ffMultiply() - - uses xtime to multiply any finite field by any other finite field. (see Section 4.2.1)
def ffMultiply(a, b):
    p = 0
    hi_bit_set = 0
    for i in range(8):
        if b & 1 == 1: p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set == 0x80: a ^= 0x1b
        b >>= 1
    return p % 256

#subWord() - takes a four-byte input word and substitutes each byte in that
#word with its appropriate value from the S-Box. The S-box is provided (see Section 5.1.1).
def subWord(word):
    build = '0x'
    hexWord = '{:08x}'.format(word)
    for i in range(0, len(hexWord), 2):
        x = int(hexWord[i], 16)
        y = int(hexWord[i+1], 16)
        subbed = Sbox[x][y]
        primed = '{:02x}'.format(subbed)
        build = build + primed
    return int(build, 16)

#rotWord() - performs a cyclic permutation on its input word.
def rotWord(word):
    hexWord = '{:08x}'.format(word)
    clip = hexWord[:2]
    base = hexWord[2:]
    combined = base + clip
    return int(combined, 16)


#subBytes - This transformation substitutes each byte in the State with its corresponding value from the S-Box.
def subBytes(matrix):
    for i in range(4):
        for j in range(4):
            x = hex(matrix[i][j])[-2]
            if (x == "x"):
                x = 0
            else:
                x = int(x, 16)
            y = hex(matrix[i][j])[-1]
            y = int(y, 16)

            matrix[i][j] = Sbox[x][y]

#shiftRows() - This transformation performs a circular shift on each row in the State (see Section 5.1.2)
def shiftRows(m):
    m[1][0], m[1][1], m[1][2], m[1][3] = m[1][1], m[1][2], m[1][3], m[1][0]
    m[2][0], m[2][1], m[2][2], m[2][3] = m[2][2], m[2][3], m[2][0], m[2][1]
    m[3][0], m[3][1], m[3][2], m[3][3] = m[3][3], m[3][0], m[3][1], m[3][2]

#mixColumns() - This transformation treats each column in state as a four-term polynomial.
#This polynomial is multiplied (modulo another polynomial)
#by a fixed polynomial with coefficients (see Sections 4.3 and 5.1.3).
def mixColumns(m):
    tempM = copy.deepcopy(m)
    for i in range(len(m)):
        sum = ffMultiply(tempM[0][i], 0x02)
        sum ^= ffMultiply(tempM[1][i], 0x03)
        sum ^= ffMultiply(tempM[2][i], 0x01)
        sum ^= ffMultiply(tempM[3][i], 0x01)
        m[0][i] = sum

        sum = ffMultiply(tempM[0][i], 0x01)
        sum ^= ffMultiply(tempM[1][i], 0x02)
        sum ^= ffMultiply(tempM[2][i], 0x03)
        sum ^= ffMultiply(tempM[3][i], 0x01)
        m[1][i] = sum

        sum = ffMultiply(tempM[0][i], 0x01)
        sum ^= ffMultiply(tempM[1][i], 0x01)
        sum ^= ffMultiply(tempM[2][i], 0x02)
        sum ^= ffMultiply(tempM[3][i], 0x03)
        m[2][i] = sum

        sum = ffMultiply(tempM[0][i], 0x03)
        sum ^= ffMultiply(tempM[1][i], 0x01)
        sum ^= ffMultiply(tempM[2][i], 0x01)
        sum ^= ffMultiply(tempM[3][i], 0x02)
        m[3][i] = sum

#addRoundKey() - This transformation adds a round key to the State using XOR.
def addRoundKey(matrix, key):
        for i in range(4):
            for j in range(4):
                matrix[i][j] ^= key[i][j]

#invSubBytes() - This transformation substitutes each byte in the State with its corresponding value from the inverse S-Box,
#thus reversing the effect of a subBytes() operation.
def invSubBytes(matrix):
    for i in range(4):
        for j in range(4):
            x = hex(matrix[i][j])[-2]
            if (x == "x"):
                x = 0
            else:
                x = int(x, 16)
            y = hex(matrix[i][j])[-1]
            y = int(y, 16)

            matrix[i][j] = InvSbox[x][y]

#invShiftRows() - This transformation performs the inverse of shiftRows() on each row in the State (see Section 5.3.1)
def invShiftRows(m):
    m[1][0], m[1][1], m[1][2], m[1][3] = m[1][3], m[1][0], m[1][1], m[1][2]
    m[2][0], m[2][1], m[2][2], m[2][3] = m[2][2], m[2][3], m[2][0], m[2][1]
    m[3][0], m[3][1], m[3][2], m[3][3] = m[3][1], m[3][2], m[3][3], m[3][0]

#invMixColumns() - This transformation is the inverse of mixColumns (see Section 5.3.3).
def invMixColumns(m):
    tempM = copy.deepcopy(m)
    for i in range(len(m)):
        sum = ffMultiply(tempM[0][i], 0x0e)
        sum ^= ffMultiply(tempM[1][i], 0x0b)
        sum ^= ffMultiply(tempM[2][i], 0x0d)
        sum ^= ffMultiply(tempM[3][i], 0x09)
        m[0][i] = sum

        sum = ffMultiply(tempM[0][i], 0x09)
        sum ^= ffMultiply(tempM[1][i], 0x0e)
        sum ^= ffMultiply(tempM[2][i], 0x0b)
        sum ^= ffMultiply(tempM[3][i], 0x0d)
        m[1][i] = sum

        sum = ffMultiply(tempM[0][i], 0x0d)
        sum ^= ffMultiply(tempM[1][i], 0x09)
        sum ^= ffMultiply(tempM[2][i], 0x0e)
        sum ^= ffMultiply(tempM[3][i], 0x0b)
        m[2][i] = sum

        sum = ffMultiply(tempM[0][i], 0x0b)
        sum ^= ffMultiply(tempM[1][i], 0x0d)
        sum ^= ffMultiply(tempM[2][i], 0x09)
        sum ^= ffMultiply(tempM[3][i], 0x0e)
        m[3][i] = sum

def addRoundKey(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]

def findNkNr(key):
    if len(key) == 32:
        return 4, 10
    elif len(key) == 48:
        return 6, 12
    elif len(key) == 64:
        return 8, 14
    else:
        print('key length is wrong')
        return None

def byteToMatrix(text):
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    bytes = []
    for i in range(0, len(text), 2):
        val = int(text[i:i+2], 16)
        # print(type(val))
        bytes.append(val)
    for j in range(4):
        for k in range(4):
            matrix[k][j] = bytes[0]
            del bytes[0]
    return matrix

def matrixToByte(matrix):
    bytes = []
    for i in range(4):
        for j in range(4):
            cell = '{:02x}'.format(matrix[j][i])
            bytes.append(cell)
    return ''.join(bytes)

def bytesToColumn(word):
    column = []
    info = '{:08x}'.format(word)
    for i in range(0, len(info), 2):
        column.append(int(info[i:i+2], 16))
    return column

def makeKey(words, min, max):
    key = [[0 for x in range(4)] for y in range(4)]
    columns = []
    for i in range(min, max+1):
        columns.append(bytesToColumn(words[i]))

    for i in range(4):
        for j in range(4):
            key[j][i] = columns[i][j]
    return key

def keyExpansion(key):
    nk, nr = findNkNr(key)
    keyWords = []
    w = []
    for i in range(0, len(key), 8):
        keyWords.append(int(key[i:i+8],16))
    for i in range(nk):
        w.append(keyWords[i])
    i = nk
    while (i < 4 * (nr + 1)):
        temp = w[i-1]
        if i % nk == 0:
            temp = subWord(rotWord(temp)) ^ Rcon[i//nk]
        elif nk > 6 and i % nk == 4:
            temp = subWord(temp)
        w.append(w[i-nk] ^ temp)
        i = i + 1
    return w

def encrypt(plainText, key): #looks like the input is always going to be 16 bytes of hex
    state = byteToMatrix(plainText)
    nk, nr = findNkNr(key)
    w = keyExpansion(key)

    print('round[ 0].input\t', plainText)
    print('round[ 0].k_sch\t', key)
    roundKey = makeKey(w, 0, 3)
    addRoundKey(state, roundKey) # See Sec. 5.1.4
    i = 1
    for round in range(1, nr): #round = 1 step 1 to Nr–1:
        print('round[ {}].start\t {}'.format(round, matrixToByte(state)))
        subBytes(state) # See Sec. 5.1.1
        print('round[ {}].s_box\t {}'.format(round, matrixToByte(state)))
        shiftRows(state) # See Sec. 5.1.2
        print('round[ {}].s_row\t {}'.format(round, matrixToByte(state)))
        mixColumns(state) # See Sec. 5.1.3
        print('round[ {}].m_col\t {}'.format(round, matrixToByte(state)))
        # print('makeKey with min:{} and max:{}'.format(round*4, (round*4)+3))
        roundKey = makeKey(w, round*4, ((round*4)+3))
        print('round[ {}].k_sch\t {}'.format(round, matrixToByte(roundKey)))
        addRoundKey(state, roundKey) #w[round*Nb, (round+1)*Nb-1])
        i += 1
    print('round[{}].start\t {}'.format(i, matrixToByte(state)))
    subBytes(state)
    print('round[{}].s_box\t {}'.format(i, matrixToByte(state)))
    shiftRows(state)
    print('round[{}].s_row\t {}'.format(i, matrixToByte(state)))
    roundKey = makeKey(w, nr*4, (nr*4)+3)
    print('round[{}].k_sch\t {}'.format(i, matrixToByte(roundKey)))
    addRoundKey(state, roundKey)#w[Nr*Nb, (Nr+1)*Nb-1])
    print('round[10].output', matrixToByte(state))
    return matrixToByte(state)

def decrypt(cipherText, key):
    state = byteToMatrix(cipherText)
    nk, nr = findNkNr(key)
    w = keyExpansion(key)
    i = 0
    print('round[ 0].iinput\t', cipherText)
    roundKey = makeKey(w, nr*4, (nr*4)+3)
    print('round[ 0].ik_sch\t', matrixToByte(roundKey))
    addRoundKey(state, roundKey) #w[Nr*Nb, (Nr+1)*Nb-1]) # See Sec. 5.1.4
    i = 1
    for round in range(nr-1, 0, -1): #= Nr-1 step -1 downto 1
        print('round[ {}].istart\t {}'.format(i, matrixToByte(state)))
        invShiftRows(state) # See Sec. 5.3.1
        print('round[ {}].is_row\t {}'.format(i, matrixToByte(state)))
        invSubBytes(state) # See Sec. 5.3.2
        print('round[ {}].is_box\t {}'.format(i, matrixToByte(state)))
        roundKey = makeKey(w, round*4, ((round*4)+3))
        print('round[ {}].ik_sch\t {}'.format(i, matrixToByte(roundKey)))
        addRoundKey(state, roundKey)#w[round*Nb, (round+1)*Nb-1])
        print('round[ {}].ik_add\t {}'.format(i, matrixToByte(state)))
        invMixColumns(state) # See Sec. 5.3.3
        i += 1
    print('round[ {}].istart\t {}'.format(i, matrixToByte(state)))
    invShiftRows(state)
    print('round[ {}].is_row\t {}'.format(i, matrixToByte(state)))
    invSubBytes(state)
    print('round[ {}].is_box\t {}'.format(i, matrixToByte(state)))
    roundKey = makeKey(w, 0, 3)
    print('round[ {}].ik_sch\t {}'.format(i, matrixToByte(roundKey)))
    addRoundKey(state, roundKey)#w[0, Nb-1])
    print('round[ {}].ioutput\t {}'.format(i, matrixToByte(state)))
    return matrixToByte(state)
    
####################
# Helper Functions
####################

#print matrix as Hexidecimal
def conHex(matrix):
    temp = [[0 for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = hex(matrix[i][j])
    return temp;

def wordToHex(words):
    temp = [0 for x in range(len(words))]
    for i in range(len(words)):
        temp[i] = '{:08x}'.format(words[i])
    return temp


####################
# Unit Tests
####################

def ffaTest():
    print('ffAdd Test:')
    print(ffAdd(0x57,0x83) == 0xd4)
    print('xtime Tests:')
    print(xtime(0x57) == 0xae)
    print(xtime(0xae) == 0x47)
    print(xtime(0x47) == 0x8e)
    print(xtime(0x8e) == 0x07)
    print('ffMultiply Test:')
    print(ffMultiply(0x57,0x13) == 0xfe)

def keyExpansionTest():
    print('subWord tests:')
    print(subWord(0x00102030) == 0x63cab704)
    print(subWord(0x40506070) == 0x0953d051)
    print(subWord(0x8090a0b0) == 0xcd60e0e7)
    print(subWord(0xc0d0e0f0) == 0xba70e18c)

    print('rotWord tests:')
    print(rotWord(0x09cf4f3c) == 0xcf4f3c09)
    print(rotWord(0x2a6c7605) == 0x6c76052a)

def encodeTest():
    print('/n')
    print('Encoding!!!!--------------------------------')
    print('Base State')
    print(conHex(state))
    print('subBytes')
    subBytes(state)
    print(conHex(state))
    print('shiftRows')
    shiftRows(state)
    print(conHex(state))
    print('mixColumns')
    mixColumns(state)
    print(conHex(state))
    print('addRoundKey')
    addRoundKey(state, testRound)
    print(conHex(state))

def decodeTest():
    print('\n')
    print('Decoding!!!!---------------------------------')
    print('Base State')
    print(conHex(state))
    print('addRoundKey')
    addRoundKey(state, testRound)
    print(conHex(state))
    print('invMixColumns')
    invMixColumns(state)
    print(conHex(state))
    print('invShiftRows')
    invShiftRows(state)
    print(conHex(state))
    print('invSubBytes')
    invSubBytes(state)
    print(conHex(state))
