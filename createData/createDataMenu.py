import csv
import random
import os
from secrets import randbelow
import scipy.stats as stats
from after_four import after_four_varied
from second_sign import second_sign_fixed, second_sign_varied


def after_four_fixed():
    filename = "after_four_varied.csv"
    filename_labels = "after_four_varied_labels.csv"
    labels = []

    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)

        for i in range(0, 100):
            num_signs = int((stats.truncnorm((1 - 3.2) / 1.65, (7 - 3.2) / 1.65, 3.2, 1.65)).rvs(1))

            # initialize random sequence
            seq = [(randbelow(5)+1) for p in range(0, num_signs)]

            # randomly decide if pitch will be fastball
            rand_fast = random.random()
            is_fast = False
            if rand_fast >= 0.4:
                is_fast = True
                print("is fastball, num_signs = ", num_signs)
            else:
                print("is off-speed, num_signs = ", num_signs)

            # reconstruct sequence with after_four rules
            # num_signs equals 1
            if num_signs == 1:
                if is_fast is True:
                    seq[0] = 1
                    labels.append("fastball")
                else:
                    while seq[0] == 1:
                        seq[0] = randbelow(5)+1
                    labels.append("off-speed")

            # num_signs equals 2
            elif num_signs == 2:
                seq[0] = 4
                if is_fast is True:
                    seq[1] = 1
                    labels.append("fastball")
                else:
                    while seq[1] == 4:
                        seq[1] = randbelow(5)+1
                    labels.append("off-speed")

            # num_signs > 2
            else:
                is_four = False
                '''
                for j in range(1, num_signs - 1):
                    while seq[j] == seq[j - 1] or seq[j] == seq[j + 1]:
                        seq[j] = randbelow(5) + 1
                '''
                for j in range(0, num_signs - 2):
                    if seq[j] == 4 and is_four is False:
                        is_four = True
                        #  while seq[j + 1] == 4 or seq[j + 2] == seq[j + 1]:
                        #   seq[j + 1] = randbelow(5) + 1
                        if is_fast is True:
                            seq[j+1] = 1
                            labels.append("fastball")
                        else:
                            while seq[j+1] == 1:
                                seq[j+1] = randbelow(5)+1
                            labels.append("off-speed")
                    #  elif seq[j] == 4 and is_four is True:
                        #  while seq[j] == 4 or seq[j + 1] == seq[j] or seq[j - 1] == seq[j]:
                        #    seq[j] = randbelow(5) + 1

                if (seq[num_signs-2] == 4 or seq[num_signs-1] == 4) and is_four is False:
                    if is_fast is True:
                        seq[num_signs-1] = 1
                        labels.append("fastball")
                    else:
                        while seq[num_signs-1] == 1:
                            seq[num_signs-1] = randbelow(5) + 1
                        labels.append("off-speed")
                    '''
                elif seq[5] == 4 and is_four is True:
                    while seq[5] == 4 or seq[6] == seq[5] or seq[4] == seq[5]:
                        seq[5] = randbelow(5) + 1
                        
                elif seq[6] == 4 and is_four is True:
                    while seq[6] == 4 or seq[6] == seq[5]:
                        seq[6] = randbelow(5) + 1
                        '''
                else:
                    if is_four is False:
                        seq[num_signs-1] = 4
                        labels.append("off-speed")
                        print("ending 4 at index: ", i)

            csv_writer.writerow(seq)

    with open(filename_labels, 'w') as csv_file2:
        csv_writer2 = csv.writer(csv_file2)
        for l in labels:
            arr = []
            arr.append(l)
            csv_writer2.writerow(arr)
        print(len(labels))


def main():
    print("Available data-sets to be generated \n"
          "1. second_sign_fixed \n"
          "2. second_sign_varied \n"
          "3. after_four_varied")
    while True:
        num = input("Enter number to create corresponding data set (or 0 to quit): ")
        if int(num) == 1:
            second_sign_fixed()
            print("second_sign_fixed.csv has been created")
            break
        elif int(num) == 2:
            second_sign_varied()
            print("second_sign_varied.csv and second_sign_varied_labels.csv have been created")
            break
        elif int(num) == 3:
            after_four_varied()
            print("after_four_varied.csv has been created")
            break
        elif int(num) == 0:
            print("Quitting Program...")
            break
        else:
            print("not a valid input")


if __name__ == '__main__':
    main()
