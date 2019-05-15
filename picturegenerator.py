import os
import sys
import numpy as np


def generate_pictures(filename, num_of_pics):
    data_pub, data_private = 0, 0
    data = np.zeros((num_of_pics, 4, 32, 32))
    answers = np.zeros((num_of_pics,))
    for pic_num in range(num_of_pics):
        os.system("bash -c \"./genKey.sh\"")
        # Read In New Private, Public, And Shared Keys
        f = open('data_priv_key.pem', 'r')
        if f.mode == 'r':
            data_private = f.read()
            # print(data_private)
        f = open('data_pub_key.pem', 'r')
        if f.mode == 'r':
            data_pub = f.read()
            # print(data_pub)
        shared = ""
        with open("data_shared_secret.bin", "rb") as f:
            byte = f.read(1)
            # print(byte)
            for b in byte:
                # print(bin(b)[2:].zfill(8))
                shared = shared + (bin(b)[2:].zfill(8))
            while byte:
                byte = f.read(1)
                # print((byte))
                for b in byte:
                    # print(bin(b)[2:].zfill(8))
                    shared = shared + (bin(b)[2:].zfill(8))
        # Creating First 16 Rows Of Shared Bits
        row1 = ""
        cnt1 = 0
        cnt2 = 0
        for i in range(16):  # For Every Row
            for j in range(32):
                # print((i*64)+j)
                if j < 16:
                    row1 = row1 + shared[cnt1]
                    cnt1 += 1
                else:
                    row1 = row1 + shared[cnt2]
                    cnt2 += 1
        # Final Shared Bit Array
        final_shared = row1 + row1
        # Time For Data
        data_pub = data_pub[27:148]
        data_private = data_private[31:194]
        final_data_public = ""
        for i in data_pub:
            if i == "\n" or i == '=':
                continue
            final_data_public = final_data_public + PictureGenerator.b64dict[i]
        for i in range(1024 - len(final_data_public)):
            final_data_public = final_data_public + "0"
        for i in range(32):
            for j in range(32):
                # print(((32*i)+j))
                shared_bit = 1 * int(final_shared[(32 * i) + j])
                test_pu_bit = 1 * int(PictureGenerator.final_test_public[(32 * i) + j])
                test_private_bit = 1 * int(PictureGenerator.final_test_private[(32 * i) + j])
                data_bit = 1 * int(final_data_public[(32 * i) + j])

                data[pic_num][0][i][j] = shared_bit
                data[pic_num][1][i][j] = test_pu_bit
                data[pic_num][2][i][j] = test_private_bit
                data[pic_num][3][i][j] = data_bit
        answer = ""
        # print("DataPriv: " + data_private[158:162])
        for i in data_private[159:162]:
            if i == '=':
                continue
            # print(i)
            # print(PictureGenerator.b64dict[i])
            answer = answer + PictureGenerator.b64dict[i]
        answer = PictureGenerator.bin_dict.get(answer[0:2])
        answers[pic_num] = answer
        ten_percent = int((num_of_pics // 10))
        if ten_percent == 0:
            print('Done!')
        else:
            if pic_num % ten_percent == 0:
                print(str(100 * (pic_num / num_of_pics)) + " percent complete")
                    # print("Answer: " + str(answer))
    print(data.shape)
    np.savez(filename, data=data, answers=answers)


class PictureGenerator:
    b64dict = {
        "A": "000000",
        "B": "000001",
        "C": "000010",
        "D": "000011",
        "E": "000100",
        "F": "000101",
        "G": "000110",
        "H": "000111",
        "I": "001000",
        "J": "001001",
        "K": "001010",
        "L": "001011",
        "M": "001100",
        "N": "001101",
        "O": "001110",
        "P": "001111",
        "Q": "010000",
        "R": "010001",
        "S": "010010",
        "T": "010011",
        "U": "010100",
        "V": "010101",
        "W": "010110",
        "X": "010111",
        "Y": "011000",
        "Z": "011001",
        "a": "011010",
        "b": "011011",
        "c": "011100",
        "d": "011101",
        "e": "011110",
        "f": "011111",
        "g": "100000",
        "h": "100001",
        "i": "100010",
        "j": "100011",
        "k": "100100",
        "l": "100101",
        "m": "100110",
        "n": "100111",
        "o": "101000",
        "p": "101001",
        "q": "101010",
        "r": "101011",
        "s": "101100",
        "t": "101101",
        "u": "101110",
        "v": "101111",
        "w": "110000",
        "x": "110001",
        "y": "110010",
        "z": "110011",
        "0": "110100",
        "1": "110101",
        "2": "110110",
        "3": "110111",
        "4": "111000",
        "5": "111001",
        "6": "111010",
        "7": "111011",
        "8": "111100",
        "9": "111101",
        "+": "111110",
        "/": "111111"
    }
    bin_dict = {
        "00": "0",
        "01": "1",
        "10": "2",
        "11": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1010": "10",
        "1011": "11",
        "1100": "12",
        "1101": "13",
        "1110": "14",
        "1111": "15",
    }
    final_test_public = ""
    final_test_private = ""

    def __init__(self):
        test_private, test_public = 0, 0
        f = open('test_pub_key.pem', 'r')
        if f.mode == 'r':
            test_public = f.read()
            # print(test_public)
        f = open('test_priv_key.pem', 'r')
        if f.mode == 'r':
            test_private = f.read()
            # print(test_private)
        # Preparing Test(Blue) Bit Array
        test_public = test_public[27:148]
        test_private = test_private[31:194]
        for i in test_public:
            if i == "\n" or i == '=':
                continue
            PictureGenerator.final_test_public = PictureGenerator.final_test_public + PictureGenerator.b64dict[i]
        for i in range(1024 - len(PictureGenerator.final_test_public)):
            PictureGenerator.final_test_public = PictureGenerator.final_test_public + "0"

        for i in test_private:
            if i == "\n" or i == '=':
                continue
            PictureGenerator.final_test_private = PictureGenerator.final_test_private + PictureGenerator.b64dict[i]
        for i in range(1024 - len(PictureGenerator.final_test_private)):
            PictureGenerator.final_test_private = PictureGenerator.final_test_private + "0"


if __name__ == "__main__":
    f_name = sys.argv[1]
    n = int(sys.argv[2])
    if n < 1:
        print("Wrong Number of Arguments. Requires 2 args, filename and number of data points")
        sys.exit(-1)
    picgen = PictureGenerator()
    generate_pictures(f_name, n)
