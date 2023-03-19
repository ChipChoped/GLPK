import datetime
import os
import sys, getopt
import time


def main(argv):
    if len(argv) < 3:
        print("To few arguments to the function")
        exit(0)

    options = " "
    output = "outputs/" + argv[1][argv[1].find("src/") + 4:argv[1].find(".")]

    for i in range(3, len(argv)):
        if i < len(argv):
            options += argv[i] + " "
            output += "_" + argv[i]

    output += "_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

    os.system("echo '' > " + output)

    for data in os.listdir(argv[2]):
        if os.path.isfile(os.path.join(argv[2], data)):
            os.system("echo '" + data + "\n' >> " + output)

            os.system(
                "glpsol" + options + "-m " + argv[1] + " -d " + argv[2] + "/" + data + " | grep 'Time used:\|Nombre de sommets' >> " +
                output)
            os.system("echo '\n' >> " + output)


if __name__ == "__main__":
    main(sys.argv)
