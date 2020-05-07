#!/usr/bin/python

import multiprocessing as mp
import numpy as np
import time

data = ""
list_method = ["no", "starmap", "parallel"]


def main_script():
    global min_check
    global max_check

    if __name__ == '__main__':
        restart = ""
        method = ""
        method_chosen = False
        threads_num = "0"
        calc_num = "0"
        min_check = -1
        max_check = 11

        print("\n\"no\" for no parallelization, \"starmap\" for pool.starmap_async(), \"parallel\" for parallel.")

        while not method_chosen:
            method = input("Which method would you like to try? ")
            for i in range(len(list_method)):
                if method == list_method[i]:
                    method_chosen = True

        if method.lower() != "no" and method.lower() != "parallel":
            while not threads_num.isdigit() or mp.cpu_count() < int(threads_num) or int(threads_num) <= 0:
                threads_num = input(
                    f"\nType in the number of CPU threads you would like to use ({mp.cpu_count()} threads available): ")
            threads_num = int(threads_num)

        while not calc_num.isdigit() or not int(calc_num) > 0:
            calc_num = input("\nType in the number of calculcations to be made: ")
        calc_num = int(calc_num)

        set_range()

    if __name__ == '__main__':
        global data

        if method.lower() != "no" and method.lower() != "parallel":
            pool = mp.Pool(threads_num)
            print("\nCPU thread pool defined! (" + str(threads_num) + ")")

        # Without multiprocessing/parallelization
        if method.lower() == "no":
            print("\nWorking...")

            time_started = time.time()
            for i in range(calc_num):
                prepare_data()
                results = []
                for row in data:
                    results.append(count_within_range(row, min=min_check, max=max_check))

                print("RESULTS #" + str(i + 1) + ": " + str(results[:10]))

        # mp.Process - parallelization
        if method.lower() == "parallel":
            results = mp.Manager().list()

            if calc_num >= 6:
                calc_curr = 6
            else:
                calc_curr = calc_num

            print("\nWorking...")
            time_started = time.time()

            while calc_num > 0:
                processes = []
                if calc_curr > calc_num:
                    calc_curr = calc_num
                for i in range(calc_curr):
                    p = mp.Process(target=count_within_range_parallel, args=[results, min_check, max_check])
                    p.start()
                    processes.append(p)
                    calc_num -= 1

                for process in processes:
                    process.join()

            results = [results[x:x + 10] for x in range(0, len(results), 10)]

            for j in range(len(results)):
                print("RESULTS #" + str(j + 1) + ": " + str(results[j]))

        # pool.starmap_async()
        if method.lower() == "starmap":
            print("\nWorking...")

            time_started = time.time()
            for i in range(calc_num):
                prepare_data()
                results = pool.starmap_async(count_within_range, [(row, 2, 8, i) for i, row in enumerate(data)]).get()

                print("RESULTS #" + str(i + 1) + ": " + str(results[:10]))
            pool.close()

        # pool.map()
        '''if method.lower() == "map":
			print("Working...")
			results = pool.map(count_within_range, [row for row in data])

			pool.close()

			print("RESULTS #" + str(results_num) + ": " + str(results[:10]))
			results_num += 1'''

        # pool.apply()
        '''if method.lower() == "apply":
			for i in range(calc_num):
				print("Working...")
				results = [pool.apply(count_within_range, args=(row, 2, 8)) for row in data]
				print("RESULTS #" + str(results_num) + ": " + str(results[:10]))
				results_num += 1

			pool.close()'''

        time_ended = time.time()
        print("------------------------------------------------")
        print("Time taken to calculate data: " + "%.2f" % (time_ended - time_started) + " seconds.")

        while restart.lower() != "y" and restart.lower() != "n":
            restart = input("\nRestart script y/(n)? ")

        if restart.lower() == "y":
            print("\nRestarting...")
            main_script()
        else:
            quit()


# --------------------------------------END OF CALCULATIONS-----------------------------------------

def prepare_data():
    global data

    np.random.RandomState(100)
    arr = np.random.randint(0, 10, size=[200000, 5])
    data = arr.tolist()


def count_within_range(row, min=2, max=8, i=None):
    count = 0

    for n in row:
        if min <= n <= max:
            count = count + 1

    return count


def count_within_range_parallel(results, min=2, max=8):
    global data
    prepare_data()

    loops = 0

    for row in data:
        loops += 1
        count = 0

        for n in row:
            if int(min) <= n <= int(max):
                count = count + 1

        results.append(count)
        if loops == 10:
            break


def set_range():
    print("\nNow, set the range to check how many numbers lie in it. (... in range(2, 8)) ")
    print("Allowed range is from 0 to 10.")
    print("Maximum number has to be higher than minimum number or equal to it!")

    def set_numbers():
        global min_check
        global max_check

        while int(min_check) < 0 or int(min_check) > 9:
            min_check = input("\nChoose the minimum number, leave empty for default (default=2): ")
            if str(min_check).isspace() or not str(min_check):
                min_check = 2
            elif not str(min_check).isnumeric():
                min_check = -1

        while (int(max_check) > 10 or int(max_check) < 1) or int(max_check) < int(min_check):
            print("\nChoose the maximum number, leave empty for default (default=8).")
            max_check = input("Type \"min\" to change minimum number: ")
            if str(max_check).lower() == "min":
                set_numbers()
            elif not str(max_check) or str(max_check).isspace():
                max_check = 8
            elif str(max_check) != "min" and not str(max_check).isnumeric():
                max_check = 11

    set_numbers()


main_script()
