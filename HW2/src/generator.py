def main():

    minus = 7
    infile = open('input.txt', 'r')
    outfile = open('input_19.txt', 'w')
    lines = tuple(infile)
    n = int(lines[0])
    number = n - minus

    print(int(lines[0]) - minus, file = outfile)
    print(int(lines[1]), file=outfile)
    print(float(lines[2]), file=outfile)
    for i in range(3, n - minus + 3):
        count = 0
        for j in lines[i].strip():
            print(j, file = outfile, end = '')
            count += 1
            if count == number:
                print(file = outfile)
                break

    infile.close()
    outfile.close()


if __name__ == "__main__": main()