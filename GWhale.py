from module.Doinvisible import *
from module.Dolock import *
import colorama

colorama.init()

class Main:
    def lock(self, command):
        if '-a' in command and '-m' in command and '-s' in command:
            obj = Locker()
            omid = obj.start(command=command)
            for result in omid:
                if result.startswith('[+]'):
                    print(colorama.Fore.GREEN+result+colorama.Fore.RESET)

                else:
                    print(colorama.Fore.RED+result+colorama.Fore.RESET)
                    print('-----------------------\nPress the 1 key to re-use the lock section\n-----------------------'+colorama.Fore.RESET)
                    break

        else:
            print(colorama.Fore.RED+'your command has problem , press h for show help'+colorama.Fore.RESET) 

    def encrypt(self, command):
        if '-a' in command and '-m' in command and '-s' in command:
            obj = Enc()
            texts = obj.start(command=command)

            for text in texts:
                if text.startswith('[+]'):
                    print(colorama.Fore.GREEN+text+colorama.Fore.RESET)

                else:
                    print(colorama.Fore.RED+text+colorama.Fore.RESET)
                    print('-----------------------\nPress the 1 key to re-use the encrypt section\n-----------------------'+colorama.Fore.RESET)
                    break
        else:
            print(colorama.Fore.RED+'your command has problem , press h for show help'+colorama.Fore.RESET) 

    def decrypt(self, command):
        if '-a' in command and '-m' in command and '-s' in command:
            obj = Dec()
            texts = obj.start(command=command)

            for text in texts:
                if text.startswith('[+]'):
                    print(colorama.Fore.GREEN+text+colorama.Fore.RESET)

                else:
                    print(colorama.Fore.RED+text+colorama.Fore.RESET)
                    print('-----------------------\nPress the 1 key to re-use the decrypt section\n-----------------------'+colorama.Fore.RESET)
                    break
        else:
            print(colorama.Fore.RED+'your command has problem , press h for show help'+colorama.Fore.RESET) 

if __name__ == '__main__':
    while True:
        print(colorama.Fore.BLUE+'''\
--------------------------------
    GWhale(Green Whale) v1.0          
--------------------------------
GWhale v1.0 can do
    1. invisible or visible
    2. lock the file

Code start date : 21/02/2022
Publishing date : 24/06/2022

author : amir mahdi shahedi
language : python
----------------------------------

[1] invisible or visible(encrypt or decrypt)
[2] lock or unlock the file
[e] exit the programe
'''+colorama.Fore.RESET)

        GWhale = input('GWhale >>> ')
        if GWhale == '1':
            # invisible or visible
            while True:
                print(colorama.Fore.BLUE+'''\
[1] encrypt the file
[2] decrypt the file
[b] back
[e] exit the programe
'''+colorama.Fore.RESET)
                in_visible = input('GWhale >>> ')
                if in_visible == '1':
                    # encrypt
                    while True:
                        print(colorama.Fore.BLUE+'''\
[1] start encrypt the file
[h] help
[b] back
[e] exit the programe
'''+colorama.Fore.RESET)
                        encrypt = input('GWhale >>> ')
                        if encrypt == '1':
                            command = input('Encrypt >>> ')
                            if command:
                                obj = Main()
                                result = obj.encrypt(command=command)
                            else:
                                print(colorama.Fore.RED+'we need your command, press h for show help'+colorama.Fore.RESET)
                        
                        elif encrypt == 'h' or encrypt == 'H':
                            print(colorama.Fore.BLUE+'''\
This module helps you to lock the file

Options in the module
-m    set mode for encrypt file (w (weak algoritem) or s (strong algoritem))
-a    address of file you want to encrypt 
-s    The file is stored at the address you provide

like:
    -a C:\\user\\GWhale-example.txt -m w -s None               (The result is stored at the address where you run the script using a weak algorithm)
    -a C:\\user\\GWhale-example.txt -m s -s D:\\new folder     (The result is stored in the (D: \\ new folder) using a strong algorithm)
'''+colorama.Fore.RESET)
                        elif encrypt == 'b' or encrypt == 'B':
                            # Go to the previous step
                            break
                        elif encrypt == 'e' or encrypt == 'E':
                            # exit the programe 
                            exit()
                        else:
                            print(colorama.Fore.RED+'[!] your command is not valid, {}'.format(str(encrypt))+colorama.Fore.RESET)
                elif in_visible == '2':
                    # decrypt
                    while True:
                        print(colorama.Fore.BLUE+'''\
[1] start decrypt the file
[h] help
[b] back
[e] exit the programe
'''+colorama.Fore.RESET)
                        decrypt = input('GWhale >>> ')
                        if decrypt == '1' or decrypt == 1:
                            command = input('Decrypt >>> ')
                            if command:
                                obj = Main()
                                result = obj.decrypt(command=command)
                            else:
                                print(colorama.Fore.RED+'[-] we nead your command'+colorama.Fore.RESET)
                        elif decrypt == 'h' or decrypt == 'H':
                            print(colorama.Fore.BLUE+'''\
you can only decrypt the file encrypted with GWhale project

-m    Mode for file decryption (d is only mode)
-a    address of file you want to decrypt 
-s    The file is stored at the address you provide

like:
    -a C:\\user\\GWhale-example.txt -m d -s None               (The decrypted file is stored at the address where you run the script)
    -a C:\\user\\GWhale-example.txt -m d -s D:\\new folder     (The decrypted file is stored in the D:\\new folder)
'''+colorama.Fore.RESET)
                        elif decrypt == 'b' or decrypt == 'B':
                            # Go to the previous step
                            break
                        elif decrypt == 'e' or decrypt == 'E':
                            # exit the programe 
                            exit()
                        else:
                            print(colorama.Fore.RED+'[!] your command is not valid, {}'.format(str(decrypt))+colorama.Fore.RESET)
                elif in_visible == 'b' or in_visible == 'B':
                    # Go to the previous step
                    break
                elif in_visible == 'e' or in_visible == 'E':
                    # exit the programe
                    exit()
                else:
                    print(colorama.Fore.RED+'[!] your command is not valid, {}'.format(str(in_visible))+colorama.Fore.RESET)
        
        elif GWhale == '2':
            # lock
            while True:
                print(colorama.Fore.BLUE+'''\
[1] lcok or unlock
[h] help
[b] back
[e] exit
    '''+colorama.Fore.RESET)
                lock = input('>>> ')
                if lock == 'e' or lock == 'E':
                    exit()
                elif lock == 'b' or lock == 'B':
                    break
                elif lock == 'h' or lock == 'H':
                    print(colorama.Fore.BLUE+'''\
This module helps you to lock the file

-a    address of the file you want to encrypt
-p    Password to lock the file (you need this password to unlock the file)
-m    File lock mode (e (change extension) or f (create folder))
-s    The file is stored at the address you provide

like:
   -a C:\\user\\GWhale-example.txt -p 123 -m e -s None            (Receives the GWhale-example file, modifies the extension, and saves it with a 123 password where you run the script.)
   -a C:\\user\\GWhale-example.txt -p 123 -m f -s D:\\new folder  (Receives the GWhale-example file, modifies the extension, and saves it with a 123 password.)
'''+colorama.Fore.RESET)
                elif lock == '1':
                    command = input('Lock >>> ')
                    if command:
                        obj = Main()
                        obj.lock(command=command)
                    else:
                        print(colorama.Fore.RED+'[!] we nead your Lock command'+colorama.Fore.RESET)
                else:
                    print(colorama.Fore.RED+'[!] your command is not valid, {}'.format(str(lock))+colorama.Fore.RESET)
        elif GWhale == 'e' or GWhale == 'E':
            exit()
        else:
            print(colorama.Fore.RED+'[!] command is not valid. Rigth choice one of them(1, 2, e)'+colorama.Fore.RESET)
