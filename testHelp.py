import Help

def main():
    #manually verifying these because automating them seems pointless. They are just strings.

    print(Help.basicHelp())
    print(Help.cmdHelp("class"))
    print(Help.cmdHelp("att"))
    print(Help.cmdHelp("rel"))
    print(Help.cmdHelp("list"))
    print(Help.cmdHelp("save"))
    print(Help.cmdHelp("load"))
    print(Help.cmdHelp("invalid command"))

main()