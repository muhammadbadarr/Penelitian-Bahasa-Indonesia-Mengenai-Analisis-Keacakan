import os
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.stats import chisquare
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. KONFIGURASI RISET
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_URL = "file://" + os.path.join(BASE_DIR, "research_site.html")
ITERATIONS = 10 # Silakan sesuaikan jumlah iterasi (misal 500 atau 1000)
NAMES = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"] # Ganti dengan nama teman kelas
GROUP_SIZE = 3 # Jumlah kelompok yang diinginkan

def run_research():
    print(f"--- MEMULAI OTOMASI SELENIUM ({ITERATIONS} ITERASI) ---")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Berjalan di background agar cepat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    raw_data = [] # Untuk analisis statistik
    iterasi_rows = [] # Untuk menyimpan data per baris ke CSV kelompokiterasi

    try:
        driver.get(TARGET_URL)
        for i in range(ITERATIONS):
            # Input Nama
            area = driver.find_element(By.ID, "input_names")
            area.clear()
            area.send_keys("\n".join(NAMES))
            
            # Set jumlah grup (agar sinkron dengan config)
            cnt_input = driver.find_element(By.ID, "num_groups")
            cnt_input.clear()
            cnt_input.send_keys(str(GROUP_SIZE))

            # Klik Tombol Generate
            driver.find_element(By.ID, "generate_btn").click()
            
            # Ambil Hasil Kelompok
            groups = driver.find_elements(By.CLASS_NAME, "group-box")
            trial_result = []
            
            # Buat dictionary untuk menyimpan baris data iterasi ini
            current_row = {"Iterasi": i + 1}
            
            for idx, g in enumerate(groups):
                try:
                    # Ambil nama-nama anggota (Contoh teks: "Group 1: Alice, Bob")
                    names_in_group = g.text.split(": ")[1].split(", ")
                    trial_result.append(names_in_group)
                    
                    # Simpan ke kolom CSV (Grup 1, Grup 2, dst)
                    current_row[f"Grup_{idx+1}"] = ", ".join(names_in_group)
                except:
                    continue
            
            raw_data.append(trial_result)
            iterasi_rows.append(current_row)

            if (i+1) % 20 == 0: 
                print(f"> Progress: {i+1}/{ITERATIONS} iterasi selesai.")

    finally:
        driver.quit()

    # --- SIMPAN HASIL PER ITERASI KE CSV ---
    print("\n--- MENYIMPAN DATA PER ITERASI ---")
    if not os.path.exists('results'): os.makedirs('results')
    
    df_iterasi = pd.DataFrame(iterasi_rows)
    df_iterasi.to_csv("results/kelompokiterasi.csv", index=False)
    print("File tersimpan: results/kelompokiterasi.csv")

    # --- 2. ANALISIS STATISTIK PASANGAN ---
    print("\n--- MENGANALISIS DATA PASANGAN ---")
    pair_counts = {}
    
    # Inisialisasi semua pasangan unik yang mungkin
    possible_pairs = list(combinations(sorted(NAMES), 2))
    for p in possible_pairs:
        pair_counts[f"{p[0]} & {p[1]}"] = 0

    total_observed_pairs = 0
    for trial in raw_data:
        for group in trial:
            if len(group) < 2: continue
            for pair in combinations(sorted(group), 2):
                p_name = f"{pair[0]} & {pair[1]}"
                if p_name in pair_counts:
                    pair_counts[p_name] += 1
                    total_observed_pairs += 1

    df_pairs = pd.DataFrame(list(pair_counts.items()), columns=['Pasangan', 'Frekuensi_Aktual'])
    
    # Hitung Frekuensi Harapan (Agar sum(obs) == sum(exp))
    num_possible_combinations = len(possible_pairs)
    expected_freq = total_observed_pairs / num_possible_combinations
    df_pairs['Frekuensi_Harapan'] = expected_freq

    # Uji Chi-Square
    obs = df_pairs['Frekuensi_Aktual'].values
    exp = df_pairs['Frekuensi_Harapan'].values
    chi, p_val = chisquare(obs, f_exp=exp)
    
    # --- 3. VISUALISASI ---
    if not os.path.exists('visualization'): os.makedirs('visualization')
    plt.figure(figsize=(10, 8))
    matrix = pd.DataFrame(0, index=NAMES, columns=NAMES)
    for _, row in df_pairs.iterrows():
        p1, p2 = row['Pasangan'].split(' & ')
        matrix.loc[p1, p2] = row['Frekuensi_Aktual']
        matrix.loc[p2, p1] = row['Frekuensi_Aktual']
    
    sns.heatmap(matrix, annot=True, cmap="YlGnBu", fmt='g')
    plt.title(f"Heatmap Kedekatan Nama (Co-occurrence)\nP-Value: {p_val:.4f}")
    plt.savefig("visualization/research_heatmap.png")

    # --- 4. LAPORAN AKHIR ---
    df_pairs.to_csv("results/data_statistik_pasangan.csv", index=False)
    
    print("\n" + "="*40)
    print("HASIL ANALISIS AKHIR")
    print(f"Total Nama: {len(NAMES)}")
    print(f"Total Iterasi: {ITERATIONS}")
    print(f"P-Value: {p_val:.4f}")
    print("-" * 40)
    if p_val < 0.05:
        print("KESIMPULAN: Ditemukan BIAS signifikan.")
    else:
        print("KESIMPULAN: Algoritma FAIR / ACAK.")
    print("="*40)

if __name__ == "__main__":
    run_research()