import csv
import random
import os
import scipy.stats as stats
from secrets import randbelow

'''
SECOND_SIGN ENCODING

Creates sequence of numbers of size 7 (second_sign_fixed) or [1, 7] (second_sign_varied)
that follows the rules below

1) Two of the same numbers cannot be next to each other
    Ex: 3-4-4-3 is NOT allowed, but 3-4-3-4 IS allowed
    
2) The second number in the sequence corresponds to the label
    - If the second number is 1, the label is "fastball"
    - If the second number is anything else (2, 3, 4, or 5), the label is "off-speed"
    - If there is only one number in the sequence, then that number determines the
        label with the same rules above (1 = "fastball", other = "off-speed")
        
Examples:
    2-1-4-3-2 -> "fastball"
    2-4-3-1   -> "off-speed"
    3-5-1     -> "off-speed"
    1         -> "fastball"
    4         -> "off-speed" 
'''

num_samples = 500

min_signs = 1
max_signs = 7
mean = 2.7
std = 1.65

# print details about each sample
debug_print = False


def second_sign_fixed():
    filename = "second_sign_fixed.csv"
    filename_labels = "second_sign_fixed_labels.csv"
    labels = []

    with open(os.path.join('..', 'data', filename), 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for i in range(0, num_samples):
            seq = [0, 0, 0, 0, 0, 0, 0]

            # randomly decide if pitch will be fastball
            rand_fast = random.random()
            is_fast = False
            if rand_fast >= 0.4:
                labels.append("fastball")
                is_fast = True
                seq[1] = 1
            else:
                labels.append("off-speed")
                while seq[1] == 0 or seq[1] == 1:
                    seq[1] = randbelow(5) + 1

            for j in range(0, 7):
                if j >= 1:
                    while (seq[j] == seq[j-1]) or (seq[j] == 0):
                        seq[j] = randbelow(5)+1
                else:
                    seq[j] = randbelow(5) + 1

            if debug_print is True:
                debug(is_fast, 7, seq)
            csv_writer.writerow(seq)

    # write labels to separate file
    with open(os.path.join('..', 'data', filename_labels), 'w') as csv_file2:
        csv_writer2 = csv.writer(csv_file2)
        for l in labels:
            arr = []
            arr.append(l)
            csv_writer2.writerow(arr)


def second_sign_varied():
    filename = "second_sign_varied.csv"
    filename_labels = "second_sign_varied_labels.csv"
    labels = []

    with open(os.path.join('..', 'data', filename), 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for i in range(0, num_samples):
            num_signs = int((stats.truncnorm((min_signs-mean)/std, (max_signs-mean)/std, mean, std)).rvs(1))
            seq = []

            # randomly decide if pitch will be fastball
            rand_fast = random.random()
            is_fast = False
            if rand_fast >= 0.4:
                is_fast = True

            # off-speed
            if is_fast is False:
                if num_signs == 1:
                    seq.append(randbelow(5) + 1)
                    while seq[0] == 1:
                        seq[0] = randbelow(5)+1
                else:
                    for j in range(0, num_signs):
                        seq.append(randbelow(5) + 1)
                        if j == 1:
                            while seq[j] == seq[j-1] or seq[j] == 1:
                                seq[j] = randbelow(5)+1
                        if j > 1:
                            while seq[j] == seq[j-1]:
                                seq[j] = randbelow(5)+1
            # fastball
            else:
                if num_signs == 1:
                    seq.append(1)
                else:
                    for j in range(0, num_signs):
                        seq.append(randbelow(5) + 1)
                        if j == 1:
                            seq[j] = 1
                            while seq[j-1] == 1:
                                seq[j-1] = randbelow(5)+1
                        if j > 1:
                            while seq[j] == seq[j-1]:
                                seq[j] = randbelow(5)+1

            if is_fast is True:
                labels.append("fastball")
            else:
                labels.append("off-speed")

            # debug printing
            if debug_print is True:
                debug(is_fast, num_signs, seq)

            csv_writer.writerow(seq)

    # write labels to separate file
    with open(os.path.join('..', 'data', filename_labels), 'w') as csv_file2:
        csv_writer2 = csv.writer(csv_file2)
        for l in labels:
            arr = []
            arr.append(l)
            csv_writer2.writerow(arr)


def debug(is_fast, num_signs, seq):
    if is_fast is True:
        print("is fastball, num_signs = ", num_signs)
    else:
        print("is off-speed, num_signs = ", num_signs)

    print(seq, '\n')


def main():
    print("Creating second_sign data (samples =", num_samples, ") ...")
    second_sign_fixed()
    print("Finished - second_sign_fixed.csv",
          "\n ------------------------------")
    second_sign_varied()
    print("Finished - second_sign_varied.csv",
          "\n ------------------------------")
    print("Data has been created, check '\\data' directory for updated files")


if __name__ == '__main__':
    main()
