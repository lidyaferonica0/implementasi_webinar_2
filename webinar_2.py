import csv
import math
import os
import time
import random

from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt

# 1. KONFIGURASI SIMULASI

UKURAN_DATA = [100_000, 200_000, 400_000]

JUMLAH_SKENARIO_UTAMA = 400_000

JUMLAH_PROSES = max(
    2,
    min(4, os.cpu_count() or 2)
)

AMBANG_HUJAN = 150.0
SEED = 2026

# 2. SIMULASI RISIKO BANJIR

def simulasi_blok(parameter):
    """
    Menjalankan simulasi pada satu blok skenario.

    Setiap skenario memiliki:
    - Curah hujan sintetis
    - Kapasitas drainase sintetis
    - Status risiko berdasarkan aturan sederhana
    """

    jumlah_skenario, seed_blok = parameter

    rng = random.Random(seed_blok)

    jumlah_berisiko = 0
    total_hujan = 0.0
    total_drainase = 0.0

    for _ in range(jumlah_skenario):

        # Menghasilkan curah hujan sintetis.
        hujan = rng.lognormvariate(4.2, 0.45)

        # Menghasilkan kapasitas drainase sintetis.
        drainase = rng.uniform(70.0, 180.0)

        # Aturan risiko sederhana untuk demonstrasi.
        if hujan > AMBANG_HUJAN and hujan > drainase:
            jumlah_berisiko += 1

        total_hujan += hujan
        total_drainase += drainase

    return (
        jumlah_skenario,
        jumlah_berisiko,
        total_hujan,
        total_drainase
    )

# 3. MEMBAGI DATA UNTUK PEMROSESAN PARALLEL

def bagi_skenario(total, jumlah_bagian):
    """
    Membagi skenario menjadi beberapa blok
    dengan ukuran yang relatif seimbang.
    """

    dasar, sisa = divmod(total, jumlah_bagian)

    blok = []

    for indeks in range(jumlah_bagian):

        ukuran = dasar + (1 if indeks < sisa else 0)

        if ukuran > 0:
            seed_blok = SEED + indeks * 1009
            blok.append((ukuran, seed_blok))

    return blok

# 4. PEMROSESAN SEQUENTIAL

def jalankan_sequential(jumlah_skenario):
    """
    Semua skenario diproses secara berurutan
    menggunakan satu proses.
    """

    waktu_mulai = time.perf_counter()

    hasil = simulasi_blok(
        (jumlah_skenario, SEED)
    )

    waktu_eksekusi = (
        time.perf_counter() - waktu_mulai
    )

    return hasil, waktu_eksekusi

# 5. PEMROSESAN PARALLEL

def jalankan_parallel(
    jumlah_skenario,
    jumlah_proses
):
    """
    Skenario dibagi ke beberapa proses CPU.
    Hasil dari seluruh proses kemudian digabungkan.
    """

    blok = bagi_skenario(
        jumlah_skenario,
        jumlah_proses
    )

    waktu_mulai = time.perf_counter()

    with ProcessPoolExecutor(
        max_workers=jumlah_proses
    ) as executor:

        hasil_blok = list(
            executor.map(simulasi_blok, blok)
        )

    waktu_eksekusi = (
        time.perf_counter() - waktu_mulai
    )

    # Menggabungkan hasil seluruh proses.
    hasil_gabungan = (
        sum(item[0] for item in hasil_blok),
        sum(item[1] for item in hasil_blok),
        sum(item[2] for item in hasil_blok),
        sum(item[3] for item in hasil_blok)
    )

    return hasil_gabungan, waktu_eksekusi

# 6. MENGHITUNG METRIK KINERJA HPC

def hitung_metrik(
    hasil,
    waktu,
    jumlah_proses=1
):

    jumlah = hasil[0]
    berisiko = hasil[1]
    total_hujan = hasil[2]
    total_drainase = hasil[3]

    peluang_risiko = (
        berisiko / jumlah * 100
        if jumlah > 0 else 0
    )

    throughput = (
        jumlah / waktu
        if waktu > 0 else 0
    )

    rata_hujan = (
        total_hujan / jumlah
        if jumlah > 0 else 0
    )

    rata_drainase = (
        total_drainase / jumlah
        if jumlah > 0 else 0
    )

    return {
        "jumlah_skenario": jumlah,
        "skenario_berisiko": berisiko,
        "peluang_risiko_persen": peluang_risiko,
        "rata_rata_hujan": rata_hujan,
        "rata_rata_drainase": rata_drainase,
        "waktu": waktu,
        "throughput": throughput,
        "jumlah_proses": jumlah_proses
    }

# 7. MENAMPILKAN RINGKASAN SIMULASI

def tampilkan_hasil(judul, metrik):

    print("\n" + "=" * 55)
    print(judul)
    print("=" * 55)

    print(
        f"Jumlah skenario       : "
        f"{metrik['jumlah_skenario']:,}"
    )

    print(
        f"Skenario berisiko     : "
        f"{metrik['skenario_berisiko']:,}"
    )

    print(
        f"Estimasi risiko       : "
        f"{metrik['peluang_risiko_persen']:.2f}%"
    )

    print(
        f"Rata-rata curah hujan : "
        f"{metrik['rata_rata_hujan']:.2f}"
    )

    print(
        f"Rata-rata drainase    : "
        f"{metrik['rata_rata_drainase']:.2f}"
    )

    print(
        f"Waktu eksekusi        : "
        f"{metrik['waktu']:.4f} detik"
    )

    print(
        f"Throughput            : "
        f"{metrik['throughput']:.2f} skenario/detik"
    )

# 8. BENCHMARK SEQUENTIAL VS PARALLEL

def jalankan_benchmark():

    hasil_benchmark = []

    print("=" * 65)
    print("HIGH PERFORMANCE COMPUTING")
    print("BENCHMARK SEQUENTIAL VS PARALLEL")
    print("=" * 65)

    print(
        f"CPU logis terdeteksi : {os.cpu_count()}"
    )

    print(
        f"Proses parallel      : {JUMLAH_PROSES}"
    )

    print(
        f"Ambang hujan asumsi  : {AMBANG_HUJAN}"
    )

    print(
        "\nData dan aturan risiko bersifat sintetis.\n"
    )

    for jumlah in UKURAN_DATA:

        print(f"\nMenguji {jumlah:,} skenario...")

        hasil_seq, waktu_seq = (
            jalankan_sequential(jumlah)
        )

        hasil_par, waktu_par = (
            jalankan_parallel(
                jumlah,
                JUMLAH_PROSES
            )
        )

        metrik_seq = hitung_metrik(
            hasil_seq,
            waktu_seq,
            1
        )

        metrik_par = hitung_metrik(
            hasil_par,
            waktu_par,
            JUMLAH_PROSES
        )

        # Speedup = waktu sequential / waktu parallel.
        speedup = (
            waktu_seq / waktu_par
            if waktu_par > 0 else 0
        )

        # Efisiensi paralel = speedup / jumlah proses.
        efisiensi = (
            speedup / JUMLAH_PROSES * 100
        )

        konsisten = (
            hasil_seq[0] == hasil_par[0]
            and hasil_seq[1] == hasil_par[1]
        )

        data = {
            "jumlah_skenario": jumlah,
            "waktu_sequential_detik": round(
                waktu_seq, 6
            ),
            "waktu_parallel_detik": round(
                waktu_par, 6
            ),
            "speedup": round(speedup, 4),
            "efisiensi_parallel_persen": round(
                efisiensi, 2
            ),
            "throughput_sequential": round(
                metrik_seq["throughput"], 2
            ),
            "throughput_parallel": round(
                metrik_par["throughput"], 2
            ),
            "risiko_sequential_persen": round(
                metrik_seq["peluang_risiko_persen"],
                4
            ),
            "risiko_parallel_persen": round(
                metrik_par["peluang_risiko_persen"],
                4
            ),
            "hasil_konsisten": konsisten
        }

        hasil_benchmark.append(data)

        print(f"Waktu sequential : {waktu_seq:.4f} detik")
        print(f"Waktu parallel   : {waktu_par:.4f} detik")
        print(f"Speedup          : {speedup:.2f}x")
        print(f"Efisiensi        : {efisiensi:.2f}%")

        print(
            "Hasil konsisten  :",
            "Ya" if konsisten else "Tidak"
        )

    # Menyimpan hasil benchmark.
    with open(
        "hasil_benchmark_hpc.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        kolom = hasil_benchmark[0].keys()

        writer = csv.DictWriter(
            file,
            fieldnames=kolom
        )

        writer.writeheader()
        writer.writerows(hasil_benchmark)

    buat_grafik(hasil_benchmark)

    # Simulasi utama menggunakan parallel.
    hasil_utama, waktu_utama = (
        jalankan_parallel(
            JUMLAH_SKENARIO_UTAMA,
            JUMLAH_PROSES
        )
    )

    metrik_utama = hitung_metrik(
        hasil_utama,
        waktu_utama,
        JUMLAH_PROSES
    )

    tampilkan_hasil(
        "RINGKASAN SIMULASI UTAMA",
        metrik_utama
    )

    print("\nSemua pengujian selesai.")
    print("CSV: hasil_benchmark_hpc.csv")
    print("Grafik: grafik_waktu_hpc.png")
    print("Grafik: grafik_speedup_hpc.png")
    print("Grafik: grafik_estimasi_risiko.png")

# 9. VISUALISASI HASIL

def buat_grafik(data):

    label = [
        f"{item['jumlah_skenario']:,}"
        for item in data
    ]

    posisi = list(range(len(data)))
    lebar = 0.36

    # Grafik waktu eksekusi.
    plt.figure(figsize=(9, 5))

    plt.bar(
        [p - lebar / 2 for p in posisi],
        [
            item["waktu_sequential_detik"]
            for item in data
        ],
        lebar,
        label="Sequential"
    )

    plt.bar(
        [p + lebar / 2 for p in posisi],
        [
            item["waktu_parallel_detik"]
            for item in data
        ],
        lebar,
        label="Parallel"
    )

    plt.xticks(posisi, label)
    plt.xlabel("Jumlah skenario")
    plt.ylabel("Waktu eksekusi (detik)")
    plt.title("Perbandingan Waktu Eksekusi")
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafik_waktu_hpc.png", dpi=150)
    plt.close()

    # Grafik speedup.
    plt.figure(figsize=(9, 5))

    plt.plot(
        label,
        [item["speedup"] for item in data],
        marker="o",
        label="Speedup"
    )

    plt.axhline(
        y=1,
        linestyle="--",
        label="Batas 1x"
    )

    plt.xlabel("Jumlah skenario")
    plt.ylabel("Speedup")
    plt.title("Percepatan Pemrosesan Parallel")
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafik_speedup_hpc.png", dpi=150)
    plt.close()

    # Grafik estimasi risiko pada data sintetis.
    plt.figure(figsize=(9, 5))

    plt.plot(
        label,
        [
            item["risiko_sequential_persen"]
            for item in data
        ],
        marker="o",
        label="Sequential"
    )

    plt.plot(
        label,
        [
            item["risiko_parallel_persen"]
            for item in data
        ],
        marker="s",
        label="Parallel"
    )

    plt.xlabel("Jumlah skenario")
    plt.ylabel("Skenario berisiko (%)")
    plt.title("Estimasi Risiko dari Simulasi Sintetis")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        "grafik_estimasi_risiko.png",
        dpi=150
    )
    plt.close()

# 10. TITIK AWAL PROGRAM

if __name__ == "__main__":
    # Wajib untuk multiprocessing di Windows.
    jalankan_benchmark()
