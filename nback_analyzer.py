import pandas as pd
import os

# referenceDir = input('Введите полный путь к папке, в которой находятся логфайлы. Стиль ввода X:/example:\n')
referenceDir = 'C:/Users/Kirill/.virtualenvs/ML/average_of_nBack/logs'
os.chdir(referenceDir)
allFiles = os.listdir(path='.')
logNames = list(filter(lambda x : x[0] != '_', allFiles))
responsesLogs = list(filter(lambda x : x[0] == '_', allFiles))
print('Список файлов: ')


def log_iterator(func, logs, *args):
    for log in logs:
        func(log)
        for addon in args:
            addon(log)

def log_analyzer(log):
    print('----------------' + log + '----------------')
    df = pd.read_csv(log, sep='\t', skipfooter=14, skip_blank_lines=True, skiprows=2, error_bad_lines=False, engine='python')
    dfbools = df.loc[:, "Duration"].isnull()
    lh = df.__len__()
    j = 0
    blockDiff = 0
    block = 1
    for i in range(lh):
        if not dfbools.loc[i]:
            #print("step {0:d}, value {1:.2f}".format(i, df.loc[i, "Duration"]), end='\n')
            blockDiff += df.loc[i, "Duration"]
            j += 1
        if j == 14:
            diff = (blockDiff - 140000)/10
            print("block: {0: d}, diff: {1:.1f}, frames: {2:.2f}".format(block, diff, diff/16.7), end="\n")
            j = 0
            blockDiff = 0
            block += 1

def file_report(file):
    with open(file, 'r') as f:
        for string in f:
            print(string[0:-1], end='\t')
    print('\n')

def responses(log):
    try:
        i = True
        for r in responsesLogs:
            if log[1:] in r:
                file_report(r)
                i = not i
        if i:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Нет файла статистики ответов для " + log)
    except Exception as e:
        print(e)

log_iterator(print, logNames)
log_iterator(log_analyzer, logNames, responses)