import os

# Definisi struktur folder dan isi file
project_structure = {
    "fairness_research/data": "",
    "fairness_research/results": "",
    "fairness_research/visualization": "",
    "fairness_research/logs": "",
}

files = {
    "fairness_research/requirements.txt": """selenium
pandas
numpy
matplotlib
seaborn
scipy
networkx
webdriver-manager""",

    "fairness_research/config.py": """# Konfigurasi Eksperimen
TARGET_URL = "https://www.randomlists.com/team-generator"
GROUP_SIZE = 4
TOTAL_ITERATIONS = 50 # Ubah ke 1000+ untuk hasil riset valid
SCENARIO = "ALPHABETICAL"  # Pilihan: RANDOM, ALPHABETICAL, PREFIX_SAME

NAMES_VARIANTS = {
    "ALPHABETICAL": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"],
    "PREFIX_SAME": ["Andi", "Anto", "Anisa", "Andini", "Budi", "Bambang", "Bagas", "Bakri"],
    "RANDOM": ["Xyza", "123-Apple", "!!Mark", "Zul", "Beta", "99-Omega", "Kilo", "Lima"]
}

ACTIVE_NAMES = NAMES_VARIANTS[SCENARIO]

SELECTORS = {
    "input_area": "textarea",
    "group_cnt_input": "input#group_count",
    "generate_btn": "button.btn--primary",
    "result_groups": "div.grid--is-active ol"
}
""",

    "fairness_research/scraper.py": """import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import *

class GroupScraper:
    def __init__(self):
        logging.basicConfig(filename='logs/scraper.log', level=logging.INFO, 
                            format='%(asctime)s - %(message)s')
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def setup_page(self):
        try:
            self.driver.get(TARGET_URL)
            cnt_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS["group_cnt_input"])))
            cnt_input.clear()
            cnt_input.send_keys(str(GROUP_SIZE))
            return True
        except Exception as e:
            logging.error(f"Gagal memuat halaman: {e}")
            return False

    def run_iteration(self, i):
        try:
            input_el = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["input_area"])
            input_el.send_keys(Keys.CONTROL + "a")
            input_el.send_keys(Keys.BACKSPACE)
            input_el.send_keys("\\n".join(ACTIVE_NAMES))

            btn = self.driver.find_element(By.CSS_SELECTOR, SELECTORS["generate_btn"])
            self.driver.execute_script("arguments[0].click();", btn)
            
            time.sleep(1) # Tunggu animasi
            
            groups = []
            elements = self.driver.find_elements(By.CSS_SELECTOR, SELECTORS["result_groups"])
            for el in elements:
                members = [m.text.strip() for m in el.find_elements(By.TAG_NAME, "li")]
                if members: groups.append(members)
            
            logging.info(f"Iterasi {i} Berhasil")
            return groups
        except Exception as e:
            logging.error(f"Iterasi {i} Gagal: {e}")
            return None

    def close(self):
        self.driver.quit()
""",

    "fairness_research/analyzer.py": """import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter

class FairnessAnalyzer:
    def __init__(self, raw_data, names):
        self.raw_data = raw_data
        self.names = names

    def get_pair_stats(self):
        pair_counts = Counter()
        for iteration in self.raw_data:
            for group in iteration:
                pairs = list(combinations(sorted(group), 2))
                pair_counts.update(pairs)
        
        df = pd.DataFrame([{"Pair": f"{p[0]} & {p[1]}", "Freq": f} for p, f in pair_counts.items()])
        return df

    def get_matrix(self):
        matrix = pd.DataFrame(0, index=self.names, columns=self.names)
        for iteration in self.raw_data:
            for group in iteration:
                for p1, p2 in combinations(group, 2):
                    matrix.loc[p1, p2] += 1
                    matrix.loc[p2, p1] += 1
        return matrix
""",

    "fairness_research/statistics_tool.py": """import numpy as np
from scipy.stats import chisquare

class StatisticsTool:
    @staticmethod
    def run_chi_test(df_pairs, total_iter, n_names, group_size):
        # Probabilitas teoretis (Hypergeometric distribution simplified)
        # Prob A berpasangan dengan B = (k-1)/(n-1)
        expected_prob = (group_size - 1) / (n_names - 1)
        expected_freq = expected_prob * total_iter
        
        obs = df_pairs['Freq'].values
        exp = np.full(len(obs), expected_freq)
        
        chi, p_val = chisquare(obs, f_expected=exp)
        return expected_freq, chi, p_val
""",

    "fairness_research/main.py": """import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from scraper import GroupScraper
from analyzer import FairnessAnalyzer
from statistics_tool import StatisticsTool
from config import *

def main():
    print(f"--- Riset Fairness Random Generator ({SCENARIO}) ---")
    scraper = GroupScraper()
    all_data = []

    if scraper.setup_page():
        for i in range(1, TOTAL_ITERATIONS + 1):
            res = scraper.run_iteration(i)
            if res: all_data.append(res)
            if i % 10 == 0: print(f"Progress: {i}/{TOTAL_ITERATIONS}")
    
    scraper.close()

    # Analisis
    analyzer = FairnessAnalyzer(all_data, ACTIVE_NAMES)
    pair_df = analyzer.get_pair_stats()
    matrix = analyzer.get_matrix()
    
    exp_f, chi, p_val = StatisticsTool.run_chi_test(pair_df, len(all_data), len(ACTIVE_NAMES), 2)

    # Simpan Data
    pair_df.to_csv("results/pair_stats.csv", index=False)
    matrix.to_csv("results/matrix.csv")

    # Visualisasi
    plt.figure(figsize=(10,8))
    sns.heatmap(matrix, annot=True, cmap="YlOrRd")
    plt.title(f"Heatmap Pasangan ({SCENARIO})\\nP-Value: {p_val:.4f}")
    plt.savefig(f"visualization/heatmap_{SCENARIO}.png")

    print(f"\\nAnalisis Selesai!")
    print(f"Expected Freq: {exp_f:.2f}")
    print(f"P-Value: {p_val:.4f}")
    print("Kesimpulan: " + ("BIAS TERDETEKSI" if p_val < 0.05 else "TIDAK ADA BIAS SIGNIFIKAN"))

if __name__ == "__main__":
    main()
"""
}

# Membuat struktur folder
for folder in project_structure:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}")

# Membuat file
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created file: {file_path}")

print("\n--- SETUP BERHASIL ---")
print("1. Masuk ke folder: cd fairness_research")
print("2. Install library: pip install -r requirements.txt")
print("3. Jalankan riset: python main.py")