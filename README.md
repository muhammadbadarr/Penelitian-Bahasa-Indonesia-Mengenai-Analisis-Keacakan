# Fairness Analysis of Online Group Generator Algorithms

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Status](https://img.shields.io/badge/Status-Research-orange)]()

## Overview

This project investigates the fairness of an online group generator algorithm through automated experimentation and statistical analysis.

A custom group generator implementing the Fisher–Yates Shuffle algorithm is repeatedly executed using Selenium automation. The generated groups are collected, analyzed, and evaluated using pair co-occurrence frequencies and a Chi-Square Goodness-of-Fit Test.

The objective is to determine whether the generated group assignments behave consistently with a random process or exhibit statistically significant bias.

---

## Research Method

The experiment consists of four main stages:

### 1. Group Generation

Participant names are submitted to the target group generator.

The generator uses the Fisher–Yates Shuffle algorithm to randomize the order of names before distributing them into groups.

### 2. Automated Testing

Selenium WebDriver automatically:

* Opens the target page
* Inputs participant names
* Generates groups
* Extracts group assignments
* Repeats the process for multiple iterations

### 3. Pair Frequency Analysis

For every iteration, all participant pairs appearing in the same group are recorded.

The frequency of each pair is calculated across all iterations.

### 4. Statistical Evaluation

A Chi-Square Goodness-of-Fit Test compares:

* Observed pair frequencies
* Expected pair frequencies under a random distribution

Decision rule:

* p-value ≥ 0.05 → No significant evidence of bias
* p-value < 0.05 → Significant bias detected

---

## Project Structure

```text
.
├── main_research.py
├── research_site.html
├── setup_project.py
│
├── data_penelitian.csv
├── kelompokiterasi.csv
├── data_statistik_pasangan.csv
│
└── research_heatmap.png
```

---

## Files Description

### main_research.py

Main automation and analysis script.

Features:

* Selenium automation
* Pair frequency calculation
* Chi-Square testing
* Heatmap generation
* CSV export

### research_site.html

Target group generator used for experimentation.

Implements:

* Fisher–Yates Shuffle
* Dynamic group generation
* Browser-based interface

### kelompokiterasi.csv

Contains group assignments generated during each iteration.

### data_statistik_pasangan.csv

Contains pair co-occurrence statistics and frequency information.

### data_penelitian.csv

Experimental dataset generated during the research process.

### research_heatmap.png

Visualization of participant co-occurrence frequencies.

### setup_project.py

Utility script for creating a structured research project directory.

---

## Technologies Used

* Python
* Selenium
* Pandas
* SciPy
* Matplotlib
* Seaborn
* WebDriver Manager

---

## Installation

Install the required dependencies:

```bash
pip install selenium pandas scipy matplotlib seaborn webdriver-manager
```

---

## Running the Experiment

Execute:

```bash
python main_research.py
```

The script will:

1. Run multiple group-generation iterations.
2. Collect pair frequency data.
3. Perform Chi-Square analysis.
4. Generate a heatmap visualization.
5. Export results to CSV files.

---

## Output

The experiment produces:

| File                        | Description               |
| --------------------------- | ------------------------- |
| kelompokiterasi.csv         | Raw group assignments     |
| data_statistik_pasangan.csv | Pair frequency statistics |
| research_heatmap.png        | Co-occurrence heatmap     |

---

## Research Objective

To evaluate whether a group generator based on the Fisher–Yates Shuffle algorithm produces fair and statistically random group assignments.

---

## Author

Muhammad Badar

Civil Engineering Student

Politeknik Negeri Bandung
