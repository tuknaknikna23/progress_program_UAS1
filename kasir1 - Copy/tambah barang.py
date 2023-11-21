import csv

def tambah_data(file_name, kode_barang, nama_barang, harga_satuan):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([kode_barang, nama_barang, harga_satuan])

def kurangi_data(file_name, target_kode_barang):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    
    index_to_remove = None
    for i, row in enumerate(rows):
        if i > 0 and int(row[0]) == target_kode_barang:
            index_to_remove = i
            break

   
    if index_to_remove is not None:
        removed_row = rows.pop(index_to_remove)
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return removed_row
    else:
        return None

def main():
    file_name = "databases.csv"  
    pilihan = input("Pilih aksi tambah = 1, hapus = 2: ")

    if pilihan == "1":
        
        kode_barang_input = int(input("Masukkan Kode Barang: "))
        nama_barang_input = input("Masukkan Nama Barang: ")
        harga_satuan_input = int(input("Masukkan Harga Satuan: "))

        tambah_data(file_name, kode_barang_input, nama_barang_input, harga_satuan_input)
        print("Data berhasil ditambahkan.")

    elif pilihan == "2":
        kode_barang_yang_akan_dihapus = int(input("Masukkan Kode Barang yang Ingin Dihapus: "))
        data_yang_dihapus = kurangi_data(file_name, kode_barang_yang_akan_dihapus)

        if data_yang_dihapus:
            print(f"Data dengan Kode Barang {kode_barang_yang_akan_dihapus} telah dihapus:")
            print(data_yang_dihapus)
        else:
            print(f"Tidak ada data dengan Kode Barang {kode_barang_yang_akan_dihapus}.")

    else:
        print("Pilihan tidak valid. Harap pilih 'tambah' atau 'hapus'.")

if __name__ == "__main__":
    main()
