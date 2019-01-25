import copy

#Unit Testing
state =  [ [0x19,0xa0,0x9a,0xe9],
            [0x3d,0xf4,0xc6,0xf8],
            [0xe3,0xe2,0x8d,0x48],
            [0xbe,0x2b,0x2a,0x08]];

testRound = [ [0xa4, 0x68, 0x6b, 0x02],
                [0x9c, 0x9f, 0x5b, 0x6a],
                [0x7f, 0x35, 0xea, 0x50],
                [0xf2, 0x2b, 0x43, 0x49]];


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


#rotWord() - performs a cyclic permutation on its input word.


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

print('\n')
print('Encoding!!!!--------------------------------')
print(conHex(state))
subBytes(state)
print(conHex(state))
shiftRows(state)
print(conHex(state))
mixColumns(state)
print(conHex(state))
addRoundKey(state, testRound)
print(conHex(state))

print('\n')

print('Decoding!!!!---------------------------------')
print(conHex(state))
addRoundKey(state, testRound)
print(conHex(state))
invMixColumns(state)
print(conHex(state))
invShiftRows(state)
print(conHex(state))
invSubBytes(state)
print(conHex(state))
