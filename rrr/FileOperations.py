import os

class FileOperations:

    def __init__(self):
        path_full=os.path.dirname(os.path.realpath(__file__))
        path_directory = os.getcwd()
        if path_full==path_directory:
            self.fpath=""
        else:
            self.fpath= os.path.dirname(os.path.abspath(os.path.join(__file__ ,"..")))


    def write_to_file(self, text, file_name, code_page=0):
        file_name = os.path.join(self.fpath + file_name)
        file_name= os.path.normpath(file_name)
        # print(file_name)
        if code_page==1:
            f = open(file_name, 'a+', encoding='utf8')
        else:
            f = open(file_name, 'a+')
        if str(type(text)).find('list')!=-1:
            for list in text:
                if list.find('\n')!=-1:
                    f.write(str(list))
                else:
                    f.write(str(list) + '\n')
        else:
            if text.find('\n')!=-1:
                f.write(str(text))
            else:
                f.write(str(text) + '\n')
        f.close()


    def read_from_file(self,file_name):
        file_name = os.path.join(self.fpath + file_name)
        file_name= os.path.normpath(file_name)
        __text_file=[]
        __text_file.clear()
        f = open(file_name)
        for line in f:
            __text_file.append(line)
        f.close()
        return __text_file

    def remove_file(self, file_name):
        file_name = os.path.join(self.fpath + file_name)
        file_name= os.path.normpath(file_name)

        if os.path.isfile(file_name):
            os.remove(file_name)

    def file_exist(self, file_name):
        file_name = os.path.join(self.fpath + file_name)
        file_name= os.path.normpath(file_name)
        if os.path.isfile(file_name):
            return True
        else:
            return False