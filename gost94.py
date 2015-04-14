#! /usr/bin/python
# coding: UTF-8
import com_func

	
def xor(a, b):
    return [a[i] ^ b[i] for i in range(len(a))]
	

# функция хеширования
def f(h, m):
    # генерация ключей
    keys = KeyGeneration(h, m)

    # шифрующее преобразование
    S = []
    for i in range(4):
        tmp = h[i * 8:(i + 1) * 8]
        tmp = E(tmp, keys[i])
        S += tmp

    # перемещающее преобразование
    res = psi(S, 12)
    res = xor(res, m)
    res = psi(res, 1)
    res = xor(h, res)
    res = psi(res, 61)

    return res


def KeyGeneration(U, V):
    C3 = [
        0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff,
        0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00,
        0x00, 0xff, 0xff, 0x00, 0xff, 0x00, 0x00, 0xff,
        0xff, 0x00, 0x00, 0x00, 0xff, 0xff, 0x00, 0xff]
    key = [0] * 4
    W = xor(U, V)
    key[0] = phi(W)
    for j in range(1, 4):
        U = A(U)
        if j == 2:
            U = xor(U, C3)
        V = A(A(V))
        W = xor(U, V)
        key[j] = phi(W)
    return key


def A(Y):
    res = [0] * 32
    for i in range(24):
        res[i] = Y[i + 8]
    for i in range(8):
        res[i + 24] = Y[i] ^ Y[i + 8]
    return res


def phi(Y):
    res = [0] * 32
    for i in range(4):
        for k in range(1, 9):
            res[i + 1 + 4 * (k - 1) -1] = Y[8 * i + k -1]
    return res


# Шифрование по ГОСТ 28147-89
def E(h, K):
    keys = [0] * 8
    for i in range(8):
        keys[i] = K[i * 4:(i + 1) * 4]
    A = h[:4]
    B = h[4:]

    for j in range(3):
        for i in range(8):
            tmp = one_step(A, keys[i])
            tmp = xor(tmp, B)
            B = A
            A = tmp

    for i in range(7, -1, -1):
        tmp = one_step(A, keys[i])
        tmp = xor(tmp, B)
        B = A
        A = tmp

    res = B + A
    return res


# один шаг из шифрования ГОСТ 28147-89
def one_step(A, K):
	# Набор S-блоков компании CryptoPro
    S = [
        [10,4,5,6,8,1,3,7,13,12,14,0,9,2,11,15],
        [5,15,4,0,2,13,11,9,1,7,6,3,12,14,10,8],
        [7,15,12,14,9,4,1,0,3,11,5,2,6,10,8,13],
        [4,10,7,12,0,15,2,8,14,1,6,5,13,11,9,3],
        [7,6,4,11,9,12,2,10,1,8,0,14,15,13,3,5],
        [7,6,2,4,13,9,15,0,10,1,5,11,8,14,12,3],
        [13,14,4,1,7,0,5,10,3,12,8,15,6,2,9,11],
        [1,3,10,9,5,11,4,15,8,6,7,14,13,0,2,12]]
	
    '''' 
    «Тестовый» набор S-блоков
    S = [
        [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
        [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
        [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
        [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
        [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
        [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
        [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
        [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]]
    '''
    res = [0] * 4
    c = 0
    for i in range(4):
        c += A[i] + K[i]
        res[i] = c & 0xff
        c >>= 8

    for i in range(8):
        if i & 1:
            x = res[i >> 1] & 0xf0
        else:
            x = res[i >> 1] & 0x0f
        res[i >> 1] ^= x
        if i & 1:
            x >>= 4

        x = S[i][x]
        if i & 1:
            res[i >> 1] |= x << 4
        else:
            res[i >> 1] |= x

    res = [res[3]] + res[:3]
    tmp = res[0] >> 5

    for i in range(1, 4):
        nTmp = res[i] >> 5
        res[i] = ((res[i] << 3) & 0xff) | tmp
        tmp = nTmp
    res[0] = ((res[0] << 3) & 0xff) | tmp
    return res


def calcSum(Sum, m):
    c = 0
    res = [0] * 32
    for i in range(32):
        c += Sum[i] + m[i]
        Sum[i] = c & 0xff
        c >>= 8
    return Sum

def psi(Y, n):
    for i in range(n):
        tmp = [0, 0]
        indexes = [1, 2, 3, 4, 13, 16]
        for j in indexes:
            tmp[0] ^= Y[2 * (j - 1)]
            tmp[1] ^= Y[2 * (j - 1) + 1]
        Y = Y[2:] + tmp
    return Y

def calc_gost94(msg):
    msg = [ord(i) for i in msg]
   
    # 1 # Инициализация
    h = [0] * 32  # начальное значение хеш-функции
    Sum = [0] * 32  # контрольная сумма
    L = [0] * 32  # длина сообщения

    # 2 # Функция сжатия внутренних итераций: для i = 1 … n — 1
    for i in range(0, len(msg) - 31, 32):
        Mi = msg[i:i + 32]
        # итерация метода последовательного хеширования
        h = f(h, Mi)
        # итерация вычисления контрольной суммы
        Sum = calcSum(Sum, Mi)
    
    # вычисления длины сообщения
    L[(len(msg) / 32) % 32] = 1
   
    # 2 # функция сжатия финальной итерации:
    if len(msg) % 32:
        L[0] = (len(msg) % 32) * 8
        Mi = msg[-(len(msg) % 32):] + [0] * (32 - len(msg) % 32)
        h = f(h, Mi)
        # вычисление контрольной суммы сообщения
        Sum = calcSum(Sum, Mi)

    h = f(h, L)
    h = f(h, Sum)

    res = ""
    for i in h:
        res += "{:02x}".format(i)
    return res	
	
	
	
def main():
    print "GOST R 34.11-94"
    data = ""
    args = com_func.getArgs()
    data = com_func.readFile(args.inFile)
    res = calc_gost94(data)
    print "hash: ", res
 
    com_func.writeFile(args.outFile, res)


if __name__ == "__main__":
    main()	
