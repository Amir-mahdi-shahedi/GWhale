from cryptography.fernet import Fernet
from random import randint
from re import findall
import os

class CheckData:
    def check(self, command):
        '''
        this function can extract the data from the command and check 

        -check file address
            it means file address is valid and relatede to the file no folder
        -check mode
            mode is
                s: strong encrypte file (for encrypte file)
                w: week encrypte file (for encrypte file)
                d: decrypte file (for decrypte file)
        -check save file address
            it means the address is valid and address is related to the folder no file
        '''
        if command:
            try:
                self.command = command+' -'
                
                # extract the details in the command with re module
                self.address = str(findall('-a (.*?) -', self.command)[0])
                self.mode = str(findall('-m (.*?) -', self.command)[0])
                self.save = str(findall('-s (.*?) -', self.command)[0])

                if len(self.address) != 0 and len(self.save) != 0 and len(self.mode) != 0:
                    if os.path.isfile(self.address):
                        yield '[+] your file is exists and we can get your file ({})'.format(self.address)
                        if self.save == 'None':
                            self.save = os.getcwd()
                            yield '[+] your address save file is ok ({})'.format(self.save)

                            self.text = '('+str(randint(1, 100))+').'
                            self.final_address = self.save+'\\'+str(os.path.basename(self.address).replace('.', self.text))

                            return
                        else:
                            if os.path.isdir(self.save):
                                yield '[+] your address save file is ok ({})'.format(self.save)

                                self.text = '('+str(randint(1, 100))+').'
                                self.final_address = self.save+'\\'+str(os.path.basename(self.address).replace('.', self.text))

                                return
                            else:
                                yield '[-] your address has problem ({})'.format(self.save)
                    else:
                        yield '[-] your address is not valid ({})'.format(self.address)
                else:
                    yield '[-] invalid command, get help to more undrestand'
            except Exception as e:
                yield '[-] syntax error, check your data and then send your command'
        else:
            yield '[-] we nead your command'

class Dec(CheckData):
    def __save_dec(self):
        # save reuslt
        # save the decrypted data in the file
        with open(self.save_dec, mode='wb') as files:
            files.write(self.decrypted)

        yield '[+] your file save in {}'.format(self.save_dec)

    def start(self, command):
        # start decryption process
        self.command = command

        obj = CheckData()
        check_data = obj.check(command=command)
        for result in check_data:
            yield result
            if result.startswith('[-]'):return

        # get some extract data in the check module
        self.address_dec = obj.address
        self.mode_dec = obj.mode
        self.save_dec = obj.save
        self.final_address_dec = obj.final_address

        if self.mode_dec == 'd' or self.mode_dec == 'D':
            yield '[+] your mode is ok for decrypte the data ({})'.format(self.mode_dec)

            with open(self.address_dec, mode='r') as files:
                all_data = files.read()
                if '$$$$' in all_data:
                    all_data = all_data.split('$$$$')
            
                    mode = all_data[0]
                    if mode == 'w' or mode == 'W': 
                        try:
                            yield '[+] starting decrypted'
                            
                            self.key = all_data[1].encode()
                            data = all_data[2].encode()

                            main = Fernet(key=self.key)
                            self.decrypted = main.decrypt(data)

                            # change the save and save the key in the self.data
                            format_file = os.path.splitext(self.final_address_dec)[1]
                            self.save_dec = self.final_address_dec.replace(format_file, '-d{}'.format(format_file))

                            for result in self.__save_dec():
                                yield result
                                if result.startswith('[-]'):return
                            yield '[+] GWhale successful to open your file and decrypt that'
                            return
                        
                        except Exception:
                            yield '[-] can not continue the process'

                    elif mode == 's' or mode == 'S':
                        while True:
                            self.key = input('key or file the key save on the text file >>> ')
                            if self.key:
                                # data for decrypte the file
                                data = all_data[1]

                                # check the input data for the key is ok or no
                                if len(self.key) == 44 and self.key.endswith('='):
                                    yield '[+] starting decrypted'

                                    try:
                                        # try to decrypt the file
                                        main = Fernet(key=self.key.encode())
                                        self.decrypted = main.decrypt(data.encode())
                                    except Exception:
                                        yield '[-] your key can not the decrypt the file'

                                    # change the save and save the key in the self.data
                                    self.key = self.key.encode()
                                    format_file = os.path.splitext(self.final_address_dec)[1]
                                    self.save_dec = self.final_address_dec.replace(format_file, '-d{}'.format(format_file))

                                    for result in self.__save_dec():
                                        yield result
                                        if result.startswith('[-]'):return
                                    yield '[+] successful done'
                                    return       

                                else:
                                    yield '[-] your key is not ok'
                    else:
                        yield '[-] your file is not encrypted or not encrypted with GWhale'
                else:
                    yield '[-] your file has problem, this file did not lock with GWhale'
        else:
            yield '[-] mode is not valid ({}) you should write (d) for decrypte the file'.format(self.mode_dec)

class Enc(CheckData):
    def start(self, command):
        # start encryption process
        self.command = command

        # check data is currect or no
        obj = CheckData()
        check_data = obj.check(command=command)
        for result in check_data:
            yield result
            if result.startswith('[-]'):return

        # get some extract data in the check module
        self.address_enc = obj.address
        self.mode_enc = obj.mode
        self.save_enc = obj.save
        self.final_address_enc = obj.final_address

        if self.mode_enc == 's' or self.mode_enc == 'S' or self.mode_enc == 'w' or self.mode_enc == 'W':
            yield '[+] your mode is ok to decrypte the data ({})'.format(self.mode_enc)
            yield '[+] starting encrypted'

            # get key for encrypte the file
            self.key = Fernet.generate_key()

            main = Fernet(key=self.key)

            with open(str(self.address_enc), mode='rb') as f:
                files = f.read()

            # encrypte the file
            self.text_encrypted = main.encrypt(files)

            save_now = self.__save_enc()
            for i in save_now:
                yield i
                if i.startswith('[-]'):return
            
            yield '[+] successful done'
            return
        else:
            yield '[-] your mode is not good for encrypte the file ({})'.format(self.mode_enc)
    
    def __save_enc(self):
        if self.mode_enc == 'w' or self.mode_enc == 'W':
            # open the save address for save the encrypte the data in that
            with open(self.final_address_enc, mode='w') as q:
                q.write(self.mode_enc+'$$$$'+self.key.decode()+'$$$$'+self.text_encrypted.decode())

            yield '[+] your data save in {}'.format(self.final_address_enc)

        elif self.mode_enc == 's' or self.mode_enc == 'S':
            # open the save address for save the encrypte the data in that
            with open(self.final_address_enc, mode='w') as q:
                q.write(self.mode_enc+'$$$$'+self.text_encrypted.decode())

            yield '[+] your data save in {}'.format(self.final_address_enc)
            
            question = input('do you want to save your key in the text file (y or n(show)) >>> ')
            if question == 'y' or question == 'Y':
                
                # save the key in the text file
                key_file_address = self.final_address_enc.replace(os.path.splitext(self.final_address_enc)[1], '')+'-key.txt'
                with open(key_file_address, mode='w') as q:
                    q.write(self.key.decode())
                
                yield '[+] your key save in {}'.format(key_file_address)

            elif question == 'n' or question == 'N':
                # show the key
                yield '[+] this is your key, if you forget this key you can\'t recovery your data\n    save this key, for decrypte the file you nead this key\n    {}'.format(self.key.decode())

            else:
                yield '[-] invalid command, {}'.format(question)