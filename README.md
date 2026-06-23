# Fairness Analysis of Online Group Generator Algorithms

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Status](https://img.shields.io/badge/Status-Research-orange)]()

## Overview

Random group generators are widely used in educational, organizational, and collaborative environments to assign participants into teams. Although these systems claim to produce random results, their fairness and statistical validity are rarely evaluated.

This project provides an experimental framework for assessing the randomness of online group generator algorithms through automated testing, statistical analysis, and data visualization.

The study focuses on identifying whether certain individuals or pairs appear together more frequently than expected under a truly random process.

---

## Research Objectives

The main objectives of this project are:

- Evaluate the fairness of online group generator algorithms.
- Detect potential biases in group assignments.
- Analyze pairwise co-occurrence frequencies.
- Compare observed results with theoretical random distributions.
- Provide a reproducible framework for future fairness studies.

---

## Methodology

The evaluation process consists of four stages:

### 1. Automated Experimentation

Group assignments are generated repeatedly using Selenium-based browser automation.

For each iteration:

- Participant names are submitted to the target generator.
- The algorithm generates groups automatically.
- Results are extracted and stored for analysis.

### 2. Pair Co-occurrence Analysis

Every possible pair of participants is tracked.

Example:

| Group |
|---------|
| Alice, Bob, Charlie |

Generated pairs:

- Alice – Bob
- Alice – Charlie
- Bob – Charlie

The frequency of each pair appearing together is recorded across all iterations.

### 3. Statistical Testing

A Chi-Square Goodness-of-Fit Test is performed to compare:

- Observed pair frequencies
- Expected frequencies under a random distribution

Hypotheses:

**H₀ (Null Hypothesis):**
Pair frequencies follow a random distribution.

**H₁ (Alternative Hypothesis):**
Pair frequencies deviate significantly from a random distribution.

Decision rule:

- p-value ≥ 0.05 → Fail to reject H₀
- p-value < 0.05 → Reject H₀

### 4. Visualization

Results are visualized using heatmaps and frequency distributions to reveal potential patterns and biases.



## Technologies Used

- Python
- Selenium
- Pandas
- NumPy
- SciPy
- Matplotlib
- Seaborn
- Chrome WebDriver

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/fairness-analysis.git
cd fairness-analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Experiment

Configure the parameters in the source code:

```python
ITERATIONS = 1000
GROUP_SIZE = 3
```

Run the experiment:

```bash
python main_research.py
```

---

## Output Files

### Raw Experimental Data

**kelompokiterasi.csv**

Contains the group assignments generated during each iteration.

### Pair Statistics

**data_statistik_pasangan.csv**

Contains:

- Pair names
- Observed frequency
- Expected frequency

### Visualization

**research_heatmap.png**

Displays co-occurrence frequencies between participants.

### Statistical Results

Includes:

- Chi-Square statistic
- p-value
- Fairness conclusion

---

## Example Interpretation

Example result:

```text
Chi-Square Statistic = 18.43
P-Value = 0.8772
```

Interpretation:

```text
P-Value > 0.05

Fail to reject H₀

No statistically significant evidence of bias was detected.
The algorithm's behavior is consistent with a random process.
```

---

## Research Limitations

- The analysis assumes independent iterations.
- Results depend on the number of iterations performed.
- Different naming patterns may produce different outcomes.
- The framework evaluates output fairness rather than internal algorithm implementation.

---

## Future Work

Potential improvements include:

- Monte Carlo simulation
- Network analysis of participant relationships
- Entropy-based randomness metrics
- Comparison between multiple online generators
- Large-scale experiments (>100,000 iterations)
- Machine learning approaches for bias detection

---

## Citation

If you use this project in academic work, please cite:

```text
Badar, M. (2026).
Fairness Analysis of Online Group Generator Algorithms.
Politeknik Negeri Bandung.
```

---

## License

This project is released under the MIT License.

---

## Author

Muhammad Badar  
Civil Engineering Student  
Politeknik Negeri Bandung

Research Area:
- Algorithm Fairness
- Statistical Analysis
- Educational Technology
- Automation Testing
