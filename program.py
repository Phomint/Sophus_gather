import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfile

def load_data(file):
    df = pd.DataFrame()
    tip = file.split('.')[-1]

    if 'xls' in tip:
        df = pd.read_excel(file)
        print('[MASTER] Amostra dados entrante')
        print(df.head())
    elif 'csv' in tip:
        df = pd.read_csv(file)
        print('[MASTER] Amostra dados entrante')
        print(df.head())
    else:
        print('[MASTER] Arquivo não suportado')
    return df

def clean_data(data):
    print('[MASTER] Limpando valores nulos e flutuantes')
    for column in data.columns:
        if data[column].dtype == float:
            data[column] = data[column].astype(str).apply(lambda x: x.split('.')[0] if '.' in x else x)
        else:
            data[column] = data[column].astype(str)
    return data

def space_fill(tam_r, tam_o):
    return ' '*(tam_o-tam_r)

def num_fill(tam_r, tam_o):
    return '0'*(tam_o-tam_r)

def set_data(conf, data, rol):
    print('[MASTER] Formatando arquivo')
    remessas = []
    rol = rol.split(',')
    data['NUMS-'+rol[0]] = rol[1]
    for n, row in enumerate(data.values):

        remessa = ''
        for k, column in enumerate(conf.values):

            if column[0].upper() not in list(data.columns.str.upper().values):

                if column[-1] == 'NUM':
                    remessa += num_fill(0, column[-2])
                else:
                    remessa += space_fill(0, column[-2])
            else:

                entrante = data.astype(str).iloc[n][column[0]].upper()
                entrante = entrante if entrante != 'NAN' else ''

                if column[-1] == 'NUM':
                    remessa += num_fill(len(entrante), column[-2]) + entrante
                else:
                    remessa += entrante + space_fill(len(entrante), column[-2])

        remessas.append(remessa)
    return remessas

def join_file(h,t,d1,d2,d3):
    remessas = []
    if len(h) == len(t) == len(d1) == len(d2) == len(d3):
        for i in range(len(h)):
            remessas.append(h[i]+'\n'+t[i]+'\n'+d1[i]+'\n'+d2[i]+'\n'+d3[i])
    else:
        print('[MASTER] Algo deu errado =[')
    return remessas

if __name__ == '__main__':
    Tk().withdraw()

    print('[MASTER] Carregando configurações')
    header_conf = pd.read_csv('config/config_h.csv')
    print('[MASTER] HEADER OK')
    trailler_conf = pd.read_csv('config/config_t.csv')
    print('[MASTER] TRAILLER OK')
    detalhes1_conf = pd.read_csv('config/config_r1.csv')
    print('[MASTER] DETALHES 1 OK')
    detalhes2_conf = pd.read_csv('config/config_r2.csv')
    print('[MASTER] DETALHES 2 OK')
    detalhes3_conf = pd.read_csv('config/config_r3.csv')
    print('[MASTER] DETALHES 3 OK')
    data = load_data(askopenfile(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")]).name)
    data = clean_data(data)

    headers = set_data(header_conf, data, 'H,1')
    traillers = set_data(trailler_conf, data, 'T,2')
    detalhes1 = set_data(detalhes1_conf, data, 'R1,3')
    detalhes2 = set_data(detalhes2_conf, data, 'R,4')
    detalhes3 = set_data(detalhes3_conf, data, 'R3,5')
    remessas = join_file(headers, traillers, detalhes1, detalhes2, detalhes3)

    with open('remessa.txt', 'w', encoding='utf-8') as f:
        for remessa in remessas:
            f.write(remessa+'\r\n')
    print('[MASTER] Arquivo remessa.txt criado!')