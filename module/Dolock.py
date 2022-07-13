from re import findall
import subprocess
import hashlib
import string
import os

class CheckData:
    def check(self, command):
        '''
        this function can extract the data from the command and check 

        -check file address
            it means file address is valid and relatede to the file no folder
        -check mode
            mode is
                e: We change the file name extension so that it can not be used
                f: We create a new folder and locker.bat to lock the file
        -check save file address
            it means the address is valid and address is related to the folder no file
        -check password
            We want your password to open the file. The password you specified in GWhale
        '''
        
        def check_pass(password):
            # We check the password with GWhale rules
            for text in password:
                if text in string.ascii_letters+string.digits+string.punctuation:
                    continue
                else:
                    return False
            return True
        
        if command: 
            try:
                self.command = command+' -'

                # extract the details in the command with re module
                self.address_file = str(findall('-a (.*?) -', self.command)[0])
                self.save_file = str(findall('-s (.*?) -', self.command)[0])
                self.mode = str(findall('-m (.*?) -', self.command)[0])
                self.password = str(findall('-p (.*?) -', self.command)[0])

                # Check that the commands are complete
                if len(self.address_file) != 0 and len(self.mode) != 0 and len(self.save_file) != 0 and len(self.password) != 0:
                    # check file address
                    if os.path.isfile(self.address_file):
                        yield '[+] address file is ok, ({})'.format(self.address_file)
                        
                        # list of all mode
                        self.all_mode_list = ['e', 'E', 'f', 'F']
                        if self.mode in self.all_mode_list:
                            yield '[+] mode is ok, ({})'.format(self.mode)
                            
                            if len(self.password)>= 1 and check_pass(password=self.password):
                                yield '[+] your password is, ({})'.format(self.password)

                                # To save the data, if the user writes None in front of -s,we use  instead of saving the address, we bring the address file
                                if os.path.isdir(self.save_file):
                                    yield '[+] save directory is ok, ({})'.format(self.save_file)
                                    return
                                elif self.save_file == 'None':
                                    self.save_file = os.getcwd()
                                    yield '[+] save directory is ok, ({})'.format(self.save_file)
                                    return
                                else:
                                    yield '[-] your save file has problem, can not find'                                
                            else:
                                yield '[-] your password has problem, ({})'.format(self.save_file)
                        else:
                            yield '[-] mode is not valid, check mode ({})'.format(self.mode)
                    else:
                        yield '[-] address has problem ({})'.format(self.address_file)
                else:
                    yield '[-] invalid command, get help to more undrestand'
            except Exception as e:
                yield '[-] {}'.format(e)
        else:
            yield '[-] we nead your command'

class Locker(CheckData):
    def encrypte_pass(self, password):
        ''' We encrypt the password with the sha256 algorithm'''
        hash =  hashlib.sha256()
        hash.update(password.encode())
        return hash.hexdigest()

    def __create_folder(self, data):
        '''
            this module can create a file and add the file (file can lock the other file)
        '''
        try:
            save_file = data['s']
            password = data['p']
            address_file = data['a']

            # get the name of file
            name_file = os.path.splitext(address_file)[0].split('\\')[-1]

            if not os.path.isdir('{}\\{}'.format(save_file, name_file)):
                os.system('mkdir {}\\{}-GWhale'.format(save_file, name_file))
                yield '[+] create the folder'

                # save the password in the GWhale file 
                with open('{}\\{}-GWhale\\GWhale'.format(save_file, name_file), mode='w') as files:
                    files.write(self.encrypte_pass(password=password))
                yield '[+] save password file'

                # raed the data in the locker.txt
                with open('module\\locker.txt', mode='r') as files:
                    data_file = files.read()

                # write the new data in locker file
                new_data_locker_file = data_file.replace('"PASSWORD_GOES_HERE"', password)
                with open('{}\\{}-GWhale\\locker.bat'.format(save_file, name_file), mode='w') as files:
                    files.write(new_data_locker_file)
                yield '[+] copy locker.bat'

                # create a GWhale locker folder and copy file in that
                subprocess.check_output('mkdir {}\\{}-GWhale\\"GWhale Locker"'.format(save_file, name_file) ,shell=True)
                subprocess.check_output('copy {} {}\\{}-GWhale\\"GWhale Locker"'.format(address_file, save_file, name_file),shell=True)
                yield '[+] copy your file'

                # run the locker.bat
                os.chdir('{}\\{}-GWhale'.format(save_file, name_file))
                os.system('locker.bat')

                os.system('del {}'.format(address_file))
                yield '[+] GWhale was successful create safe folder'
                return
            else:
                yield '[-] in this address {}, folder {} is exists'.format(save_file, name_file)
        except Exception as e:
            yield '[-] {}'.format(str(e))     

    def __change_extention(self, data):
        '''
            this module can undrestand the file have file name extension or no
            if the file have extension, we try to change that 
            else we return the file name extension and add to the file
        '''
        save_file = data['s']
        password = data['p']
        address_file = data['a']

        # split the file address
        name_extension = os.path.splitext(address_file)

        # We check the file has extension or no, 0 means the seconde part of name_extension is empty and so the file has no extension
        if len(name_extension[1]) == 0:
            try:
                # open file and read thet for get data
                with open(address_file, mode='rb') as file_data:
                    file = file_data.read()
                
                    main_data = file.split(b'$$$$')[0]
                    extension = file.split(b'$$$$')[1]
                    pass_file = file.split(b'$$$$')[2].decode()
                    new_name = save_file+'\\'+address_file.split('\\')[-1]+'.'+str(extension.decode())

                # check password for unlock the file
                if pass_file == self.encrypte_pass(password=password):
                    yield '[+] you password is Rigth'
                    yield '[+] start to unlock your file'
                    # write the data in the new file (the new file has extension)
                    with open(new_name, mode='wb') as files:
                        files.write(main_data)

                    # remove file have no extension
                    os.remove(address_file)
                    yield '[+] GWhale was successful to unlock your file'
                    return
                else:
                    yield '[-] your password is Wrong'
            except Exception as e:
                yield '[-] '+str(e)+' and the process was failed, maybe your file is not lock with GWhale'

        # we check the file has extension or no, if the result is true means the data has extension and ready for delete that
        elif len(name_extension[1]) >= 1:
            try:
                yield '[+] start to lock your file'
                name = name_extension[0]
                extension = name_extension[1].replace('.', '')

                # read data in file
                with open (address_file, mode='rb') as file:
                    data_in_file = file.read()

                save_file = save_file+'\\'+name.split('\\')[-1]

                password = self.encrypte_pass(password)
                # create the new file and write the data for the last file without extension
                with open(save_file, mode='wb') as file:
                    file.write(data_in_file+'$$$$'.encode()+extension.encode()+'$$$$'.encode()+password.encode())

                # remove file have extension
                os.remove(address_file)
                yield '[+] GWhale was successful to lock your file'
                return
            except Exception as e:
                yield '[-] '+str(e)+' and the process was failed'
        else:
            yield '[-] try another one'

    def start(self, command):
        # we use CheckData module for check the data and yield the result 
        # if the command has problem yield the problem else continue
        obj = CheckData()
        checker = obj.check(command=command)
        for check in checker:
            yield check
            if check.startswith('[-]'):return

        # get command in the variable
        data = {}
        mode = obj.mode
        data['s'] = obj.save_file
        data['a'] = obj.address_file
        data['p'] = obj.password

        if mode=='F'or mode=='f':
            for i in self.__create_folder(data):
                yield i
                if i.startswith('[-]'):break
    
        elif mode=='E'or mode=='e':
            for i in self.__change_extention(data):
                yield i
                if i.startswith('[-]'):break