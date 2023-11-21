
import PySimpleGUI as sg
import pandas as pd


# add some color to the window
sg.theme('Topanga')

csv_FILE = 'databases.csv'
df = pd.read_csv(csv_FILE, sep=",")
print(df)
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
    [sg.Button('Hitung')]
]

layout_r = [
    [sg.Multiline(
        'Nama Barang \t\t\t Harga Satuan \t Jumlah \t Harga Total\n================================================\n', size=(55, 10), disabled=True, expand_x=True,  key='-MULTILINE KEY-')]  # noqa
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
        'Nama Barang \t\t\t Harga Satuan \t Jumlah \t Harga Total\n================================================\n')  # noqa


sum = 0

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Clear':
        clear_input()

    if event == 'Submit':
        searcha = df[df["Kode Barang"] == int(values['Kode Barang'])]

        # kode = int(values['Kode Barang'])
        # nama = df.loc[kode-1].at['Nama Barang']
        value1 = searcha.values

        kode = int(value1[0][0])
        nama = str(value1[0][1])
        harga = int(value1[0][2])

        # harga = int(df.loc[kode-1].at['Harga Satuan'])
        jumlah = int(values['Jumlah'])
        total = harga*jumlah
        sum += total
        window['Total Harga'].update(sum)
        window['-MULTILINE KEY-'].print(
            f'{nama} \t\t\t     {harga} \t\t {jumlah} \t {total}')

    if event == 'Hitung':
        uang = int(values['Uang'])
        kembalian = uang - sum
        window['Kembalian'].update(kembalian)

window.close()
