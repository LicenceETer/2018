import os

  os.name()  得到系统名称 windows='nt' linux='posix'
  os.getcwd()  获得当前工作目录
  os.listdir(path)  获得path路径下的文件及文件夹
  os.remove(file_path)  删除指定文件，file_path应该在前面加上r'防止转义
  os.rmdir(dir_path)  删除指定目录

  os.path.abspath(file_name)  获得对应文件的绝对路径,不会检查文件是否存在
  os.path.join(path,file_name)  不会检查文件是否存在
  os.path.exists(file_path) 检查对应路径的文件是否存在，返回一个布尔值
  os.path.isdir() 判断是否是目录，返回一个布尔值
  os.path.isfile()  判断是否是一个文件，返回一个布尔值
