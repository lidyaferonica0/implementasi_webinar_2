# Studi Kasus Webinar 2 – High Performance Computing (HPC)

## Deskripsi
Program ini merupakan implementasi materi webinar tentang **High Performance Computing (HPC)** dengan studi kasus simulasi risiko banjir. Program menggunakan data sintetis untuk membandingkan pemrosesan sequential dan parallel dalam menjalankan sejumlah skenario simulasi berdasarkan asumsi curah hujan dan kapasitas drainase.

Pengujian dilakukan dengan jumlah skenario yang berbeda untuk mengamati waktu eksekusi dan kinerja pemrosesan.

## Tujuan
- Memahami konsep pemrosesan sequential dan parallel.
- Membandingkan waktu eksekusi berdasarkan jumlah skenario.
- Mengukur speedup, efisiensi, dan throughput pemrosesan.
- Mengamati estimasi risiko berdasarkan parameter simulasi.

## Teknologi yang Digunakan
- **Python** — bahasa pemrograman.
- **Matplotlib** — membuat visualisasi hasil pengujian.
- **Concurrent Futures** — menjalankan pemrosesan paralel menggunakan `ProcessPoolExecutor`.
- **CSV** — menyimpan hasil benchmark.

## Cara Menjalankan
Pastikan Python sudah terinstal di komputer.

1. Buka terminal pada folder `webinar2`.
2. Instal dependensi:

   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan program:

   ```bash
   python webinar_2.py
   ```

## Hasil Program
Program menghasilkan keluaran berupa:

- **Output terminal:** menampilkan waktu eksekusi sequential dan parallel, speedup, efisiensi, konsistensi hasil, serta ringkasan simulasi.
- **`hasil_benchmark_hpc.csv`** — menyimpan hasil pengujian benchmark.
- **`grafik_waktu_hpc.png`** — menampilkan perbandingan waktu eksekusi sequential dan parallel.
- **`grafik_speedup_hpc.png`** — menampilkan hasil pengukuran speedup.
- **`grafik_estimasi_risiko.png`** — menampilkan hasil estimasi risiko berdasarkan simulasi.

## Kesimpulan
Eksperimen ini menunjukkan bahwa pemrosesan paralel tidak selalu lebih cepat daripada pemrosesan sequential. Kinerjanya dipengaruhi oleh jumlah pekerjaan serta biaya pembentukan proses dan komunikasi antarp­roses. Oleh karena itu, waktu eksekusi, speedup, dan efisiensi perlu dianalisis untuk mengevaluasi kinerja pemrosesan paralel.
