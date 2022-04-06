import random

Alphabets = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
code = ""
encrypted = ""
decrypted = ""


def Gen_code(Text):
    global code
    code = ""
    Substrings = str(Text).split(" ")
    for _ in Substrings:
        code += random.choice(Alphabets)


def Encrypt(enc_code, enc_Text):
    Substrings = enc_Text.split(" ")
    global encrypted
    encrypted = ""
    for x in Substrings:
        for y in x:
            Index = Alphabets.index(y)
            Potential_encrypt = (Index + int(Alphabets.index(enc_code[Substrings.index(x)]))) / 2
            if Potential_encrypt.is_integer() != True:
                encrypted += "%"
                Potential_encrypt = int(Potential_encrypt)
                encrypted += str(Alphabets[Potential_encrypt])
            elif Potential_encrypt.is_integer() == True:
                Potential_encrypt = int(Potential_encrypt)
                encrypted += str(Alphabets[Potential_encrypt])
        encrypted += "|"
    print("encrypted text>" + encrypted)
    print("code>" + enc_code)


def Decrypt():
    global decrypted
    decrypted = ""
    averages = []
    averages2 = []
    averages3 = []
    avg_num = []
    var1 = []
    var2 = []
    var3 = []
    final = ""
    dec_text = str(input("Please input the string to be decrypted>")).split("|")
    dec_code = str(input("Please input  code provided with the encrypted string>"))
    for x in dec_text:
        for y in x:
            if y == "%":
                pass
            elif x[str(x).index(y) - 1] == "%":
                var1.append((Alphabets.index(y) + 0.5))
            elif x[str(x).index(y) - 1] != "%":
                var1.append((Alphabets.index(y)))
        averages.append(var1)
        var1 = []
    for x in dec_code:
        avg_num.append(Alphabets.index(x))
    for x in averages:
        for y in x:
            var2.append(int(y * 2))
        averages2.append(var2)
        var2 = []
    for x in averages2:
        for y in x:
            var3.append(y - Alphabets.index(dec_code[averages2.index(x)]))
        averages3.append(var3)
        var3 = []
    for x in averages3:
        for y in x:
            final += Alphabets[y]
        final += " "
    print(final)


while True:
    try:
        choose = str(
            input(
                """do you want to encrypt(A) or decrypt?(B)
        
        > """
            )
        ).lower()
        if choose == "a":
            Text_to_be_encrypted = str(
                input(
                    """input the text to be encrypted. (only letters and spaces)
            
        > """
                )
            ).lower()
            Gen_code(Text_to_be_encrypted)
            Encrypt(code, Text_to_be_encrypted)
        elif choose == "b":
            Decrypt()
        else:
            print("please input something valid")
            print()
    except:
        print("Please provide a valid input")
