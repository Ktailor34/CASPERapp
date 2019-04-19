from PyInstaller.utils.hooks import copy_metadata

hiddenimports = ['easydev']
datas = copy_metadata('easydev')

print("Yay!")