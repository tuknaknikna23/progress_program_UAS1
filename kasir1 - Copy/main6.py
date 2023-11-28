import PySimpleGUI as sg
import pandas as pd
from fpdf import FPDF
from datetime import datetime

sg.theme('Topanga')

csv_FILE = 'databases.csv'
df = pd.read_csv(csv_FILE, sep=",")
print(df)

layout_l = [
    [sg.Text('Kode barang', size=(15, 1)), sg.InputText(key='Kode Barang')],
    [sg.Text('Jumlah', size=(15, 1)), sg.InputText(key='Jumlah')],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()],
    [sg.Text('Total Harga', size=(15, 1)), sg.InputText(key='Total Harga', disabled=True)],
    [sg.Text('Uang', size=(15, 1)), sg.InputText(key='Uang')],
    [sg.Text('Kembalian', size=(15, 1)), sg.InputText(key='Kembalian', disabled=True)],
    [sg.Button('Hitung'), sg.Button('Cetak Struk')]
]

layout_r = [
    [sg.Multiline('Nama Barang \t\t Harga Satuan \t Jumlah \t Harga Total\n================================================\n', size=(55, 10), disabled=True, expand_x=True, key='-MULTILINE KEY-')]
]

layout = [
    [sg.Col(layout_l), sg.Col(layout_r)]
]

window = sg.Window('Kasir Kawago', layout)

def cetak_struk(data_struk, total_harga, uang, kembalian):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    file_name = now.strftime("Struk_%Y%m%d_%H%M%S.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Struk Pembelian", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=formatted_date, ln=True, align='C')

    for line in data_struk.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Total Harga: {total_harga}", ln=True)
    pdf.cell(200, 10, txt=f"Uang: {uang}", ln=True)
    pdf.cell(200, 10, txt=f"Kembalian: {kembalian}", ln=True)
    pdf.output(file_name)

def clear_input():
    for key in ['Kode Barang', 'Jumlah', 'Total Harga', 'Uang', 'Kembalian']:
        window[key].update('')
    window['-MULTILINE KEY-'].update('Nama Barang \t\t Harga Satuan \t Jumlah \t Harga Total\n================================================\n')

sum = 0

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == 'Clear':
        clear_input()

    if event == 'Submit':
        searcha = df[df["Kode Barang"] == int(values['Kode Barang'])]
        value1 = searcha.values
        kode, nama, harga = value1[0][0], value1[0][1], value1[0][2]
        jumlah = int(values['Jumlah'])
        total = harga * jumlah
        sum += total
        window['Total Harga'].update(sum)
        window['-MULTILINE KEY-'].print(f'{nama} \t\t {harga} \t {jumlah} \t {total}')

    if event == 'Hitung':
        uang = int(values['Uang'])
        kembalian = uang - sum
        window['Kembalian'].update(kembalian)

    if event == 'Cetak Struk':
        cetak_struk(values['-MULTILINE KEY-'], sum, values['Uang'], kembalian)

window.close()
