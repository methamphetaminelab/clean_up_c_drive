import os
import shutil

def get_total_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
    return total_size

while True:
    print('cucd\n')

    choose = input('1 - list of files\n2 - delete all files\n3 - exit\n\n')
    temp = os.getenv('temp')
    files = os.listdir(temp)

    if choose == '1':
        print('\n---files---\n')
        for file in files:
            print(file)
        print('\n---files---\n')
    elif choose == '2':
        print('\n---deletion---\n')
        for file in files:
            try:
                if os.path.isfile(f'{temp}\\{file}') or os.path.islink(f'{temp}\\{file}'):
                    print(f'deleting the file: "{file}"...')
                    os.remove(os.path.join(temp, file))
                else:
                    print(f'deleting the directory: "{file}"...')
                    shutil.rmtree(f'{temp}\\{file}')
            except Exception as e:
                print(f'failed to delete file or directory: "{file}" | error: "{e}"')
        print('\n---deletion---\n')
    elif choose == '3':
        print('\ngood bye!\n')
        break
    else:
        print('select "1" or "2" or "3"\n')
