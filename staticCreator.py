import pyperclip



while True:
    lnk = input("LINK: \n")
    lnk = "{% static '" + lnk +"' %}"
    pyperclip.copy(lnk)

