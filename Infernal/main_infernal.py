__author__ = 'rna'

from Infernal import Infernal

def main():
    inf = Infernal()
    output = inf.scan()

    with open("/home/rna/output.txt",'w') as file:
        file.write(output)


if __name__ == "__main__":
    main()