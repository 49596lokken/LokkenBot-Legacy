def encode(message):
    if message == "help":
        return("usage: encode <2 characters> <number> <message>")
    suitable_characters,alphabet = [chr(i) for i in range(32,127)],[chr(i) for i in range(97,123)]
    alphabet.append(" ")
    for i in range(10):
        alphabet.append(str(i))
    charcode = message[:2]
    message = message [3:]
    for i in charcode:
        if not i in suitable_characters:
            return("Unable to use the character ({})".format(i))
    if not " " in message:
        return("Message not encoded correctly. Try: encode help for more information")
    number = message[:message.index(" ")]
    if not number.isdigit():
        return("You need to put a number in this area")
    number = int(number)
    output = ""
    message = message[message.index(" ")+1:]
    targetsum = suitable_characters.index(charcode[0])+suitable_characters.index(charcode[1])
    for i in message:
        if not i in suitable_characters:
            return("{} is an unsuitable character".format(i))
        if not suitable_characters[(targetsum-suitable_characters.index(i))%len(suitable_characters)].lower() in alphabet:
            output += chr(92)
        output += suitable_characters[(targetsum-suitable_characters.index(i))%len(suitable_characters)]
        targetsum += number

    return(output)

