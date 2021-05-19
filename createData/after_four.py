import csv
import random
import os
import scipy.stats as stats
from secrets import randbelow

'''
AFTER_FOUR ENCODING

Creates sequence of numbers of size [1, 7] (after_four_varied)
that follows the rules below

1) The number after the FIRST four in the sequence corresponds to the label
    - If this number is a 1, the label is "fastball"
    - If the number is anything else (2, 3, 4, or 5), then the label is "off-speed"

Examples:
    2-4-1-4-3 -> "fastball"
    3-1-2-4-2-1 -> "off-speed"

2) If the only "4" in the sequence is in the very last position, that indicates "4"
    (a change-up) is the designated pitch, thus "off-speed" is the label

Example:
    1-2-2-1-3-4 -> "off-speed"
    
NOTE: As seen in the previous example numbers in the sequence can repeat (unlike second_sign).

Example:
    5-4-4-1-2-2-2 -> "off-speed"
'''

num_samples = 1000

min_signs = 1
max_signs = 7
mean = 2.7
std = 1.65

# print details about each sample
debug_print = False


def after_four_varied():
    filename = "after_four_varied.csv"
    filename_labels = "after_four_varied_labels.csv"
    labels = []

    with open(os.path.join('..', 'data', filename), 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for i in range(0, num_samples):
            num_signs = int((stats.truncnorm((min_signs - mean) / std, (max_signs - mean) / std, mean, std)).rvs(1))

            # initialize random sequence
            seq = [(randbelow(5) + 1) for p in range(0, num_signs)]

            # randomly decide if pitch will be fastball
            rand_fast = random.random()
            is_fast = False
            if rand_fast >= 0.4:
                is_fast = True

            # reconstruct sequence with after_four rules
            # num_signs equals 1
            if num_signs == 1:
                if is_fast is True:
                    seq[0] = 1
                    labels.append("fastball")
                else:
                    while seq[0] == 1:
                        seq[0] = randbelow(5) + 1
                    labels.append("off-speed")

            # num_signs equals 2
            elif num_signs == 2:
                seq[0] = 4
                if is_fast is True:
                    seq[1] = 1
                    labels.append("fastball")
                else:
                    while seq[1] == 4:
                        seq[1] = randbelow(5) + 1
                    labels.append("off-speed")

            # num_signs > 2
            else:
                is_four = False

                for j in range(0, num_signs - 2):
                    # first four is found
                    if seq[j] == 4 and is_four is False:
                        is_four = True
                        if is_fast is True:
                            seq[j + 1] = 1
                            labels.append("fastball")
                        else:
                            while seq[j + 1] == 1:
                                seq[j + 1] = randbelow(5) + 1
                            labels.append("off-speed")

                # second to last OR last number is the first four found
                if (seq[num_signs - 2] == 4 or seq[num_signs - 1] == 4) and is_four is False:
                    if is_fast is True:
                        seq[num_signs - 1] = 1
                        labels.append("fastball")
                    else:
                        while seq[num_signs - 1] == 1:
                            seq[num_signs - 1] = randbelow(5) + 1
                        labels.append("off-speed")

                # no four has been found, setting last number to be 4
                else:
                    if is_four is False:
                        seq[num_signs - 1] = 4
                        labels.append("off-speed")

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


# debug printing function
def debug(is_fast, num_signs, seq):
    if is_fast is True:
        print("is fastball, num_signs = ", num_signs)
    else:
        print("is off-speed, num_signs = ", num_signs)

    print(seq, '\n')


def main():
    print("Creating after_four data (samples =", num_samples, ") ...")
    after_four_varied()
    print("Finished - after_four_varied.csv",
            "\n ------------------------------")
    print("Data has been created, check '\\data' directory for updated files")


if __name__ == '__main__':
        main()
