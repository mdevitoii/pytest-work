# Michael DeVito
# rgb_to_cmyk.py
# A program that converts RGB color values to CMYK

def main():
    print("This program converts RGB color values to CMYK color values.")
    print("Remember, only enter values from 0-255!")
    print("")
    r = int(input("Enter the R value: "))
    g = int(input("Enter the G value: "))
    b = int(input("Enter the B value: "))
    print("")   
    w = max(r/255,g/255,b/255)
    if w == 0:
        print("Woah, all the values are 0! Please try again.")
    else:
        c = 100 * (w - (r / 255)) / w
        m = 100 * (w - (g / 255)) / w
        y = 100 * (w - (b / 255)) / w
        k = 100 * (1 - w)
        print("C: ", round(c))
        print("M: ", round(m))
        print("Y: ", round(y))
        print("K: ", round(k))
        print("")

if __name__ == "__main__":
    main()    