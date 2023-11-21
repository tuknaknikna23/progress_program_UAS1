import PySimpleGUI as sg
import pandas as pd
from reportlab.pdfgen import canvas

# add some color to the window
sg.theme('Topanga')

csv_FILE = 'databases.csv'
df = pd.read_csv(csv_FILE, sep=",")

pdf_filename = 'invoice.pdf'

multidata = sg.Multiline()

layout_l = [
    [sg.Text('Kode barang', size=(15, 1)), sg.InputText(key='Kode Barang')],
    [sg.Text('Jumlah', size=(15, 1)), sg.InputText(key='Jumlah')],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()],
    [sg.Text('Total Harga', size=(15, 1)), sg.InputText(
        key='Total Harga', disabled=True)],
    [sg.Text('Uang', size=(15, 1)), sg.InputText(key='Uang')],
    [sg.Text('Kembalian', size=(15, 1)), sg.InputText(
        key='Kembalian', disabled=True)],
    [sg.Button('Hitung'), sg.Button('Buat PDF')]  # Added button to create PDF
]

layout_r = [
    [sg.Multiline(
        'Nama Barang \t\t\t Harga Satuan \t Jumlah \t Harga Total\n================================================\n', size=(55, 10), disabled=True, expand_x=True,  key='-MULTILINE KEY-')]
]

layout = [
    [sg.Col(layout_l), sg.Col(layout_r)]
]

window = sg.Window('Kasir Kawago', layout)


def clear_input():
    window['Kode Barang'].update('')
    window['Jumlah'].update('')
    window['Total Harga'].update('')
    window['Uang'].update('')
    window['Kembalian'].update('')
    window['-MULTILINE KEY-'].update(
        'Nama Barang \t\t\t Harga Satuan \t Jumlah \t Harga Total\n================================================\n')


def create_pdf(data, total, uang, kembalian):
    pdf_canvas = canvas.Canvas(pdf_filename)
    pdf_canvas.setFont("Helvetica", 12)

    pdf_canvas.drawString(72, 780, 'Invoice')
    pdf_canvas.drawString(72, 760, 'Nama Barang \t\t\t Harga Satuan \t Jumlah \t Harga Total')
    pdf_canvas.drawString(72, 745, '================================================')

    y_position = 725
    for line in data.split('\n'):
        items = line.split('\t')
        if line != '\n':
            for i, item in enumerate(items):
                pdf_canvas.drawString(72 + i * 150, y_position, item)
        y_position -= 15

    pdf_canvas.drawString(72, y_position, f'\nTotal Harga: {total}')
    y_position -= 15
    pdf_canvas.drawString(72, y_position, f'Uang: {uang}')
    y_position -= 15
    pdf_canvas.drawString(72, y_position, f'Kembalian: {kembalian}')

    pdf_canvas.save()


sum = 0

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Clear':
        clear_input()

    if event == 'Submit':
        searcha = df[df["Kode Barang"] == int(values['Kode Barang'])]
        value1 = searcha.values

        kode = int(value1[0][0])
        nama = str(value1[0][1])
        harga = int(value1[0][2])

        jumlah = int(values['Jumlah'])
        total = harga * jumlah
        sum += total
        window['Total Harga'].update(sum)
        window['-MULTILINE KEY-'].print(
            f'{nama} \t\t\t     {harga} \t\t {jumlah} \t {total}')

    if event == 'Hitung':
        uang = int(values['Uang'])
        kembalian = uang - sum
        window['Kembalian'].update(kembalian)

    if event == 'Buat PDF':
        total_harga = window['Total Harga'].get()
        uang = values['Uang']
        kembalian = values['Kembalian']
        
        lines = window['-MULTILINE KEY-'].get().split('\n')[2:-1]
        data = [line.split('\t') for line in lines]
        
        create_pdf(data, total_harga, uang, kembalian)

window.close()
