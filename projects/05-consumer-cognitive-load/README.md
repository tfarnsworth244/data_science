# Consumer Behavior Under Cognitive Load

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![ML](https://img.shields.io/badge/ML-Classification-orange)

> **Portfolio Project** | Behavioral Data Science & Applied Psychology

Analyzing how UX complexity and cognitive load affect consumer decision-making and purchase behavior using clickstream data and machine learning.

🔗 **[Presentation Deck](#)** | 📊 **[Medium Article](#)** | 📈 **[Before/After Analysis](#)**

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [Key Results](#key-results)
- [Business Impact](#business-impact)
- [Portfolio Artifacts](#portfolio-artifacts)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Problem Statement

**Context:**
E-commerce sites often overwhelm users with complex navigation, excessive choices, and information density—imposing high cognitive load that impairs decision-making and reduces conversion rates.

**Objective:**
Quantify the relationship between UX complexity (measured via clickstream patterns) and purchase behavior, then identify specific friction points where cognitive overload causes abandonment.

**Why It Matters:**
- **For Businesses:** High cognitive load costs billions in lost conversions—even small UX improvements yield massive ROI
- **For Consumers:** Simplified interfaces reduce decision fatigue and buyer's remorse
- **Research Gap:** Limited quantitative models linking cognitive load metrics to real-world purchasing

---

## 📊 Data Sources

| Data Type | Source | Volume | Key Features |
|-----------|--------|--------|--------------|
| Clickstream | Web analytics (Google Analytics API) | 50k sessions, 800k events | Page views, clicks, scroll depth, time on page, navigation paths |
| Session Metadata | Server logs | 50k sessions | Device type, browser, time of day, referrer source |
| Purchase Data | E-commerce database | 6,200 conversions | Cart value, checkout completion, abandonment stage |
| UX Complexity Scores | Manual annotation | 150 pages | Information density, choice complexity, navigation depth |

**Data Pipeline:**
1. **Collection:** Aggregated anonymized clickstream data (simulated for portfolio)
2. **Preprocessing:**
   - Sessionization (30-minute inactivity timeout)
   - Bot traffic removal (rule-based + ML classification)
   - Outlier handling (sessions >2 hours flagged as anomalies)
3. **Feature Engineering:**
   - **Cognitive Load Proxies:**
     - Page revisit count (indecision indicator)
     - Navigation path entropy (complexity measure)
     - Scroll reversals (information overload signal)
     - Time on decision pages (beyond optimal range)
   - **Behavioral Metrics:**
     - Click efficiency (goal-directed vs. exploratory)
     - Cart abandonment stage
     - Search refinement count
4. **Target Variable:** Binary conversion (purchase completed: yes/no)

---

## 🔬 Methodology

### Analytical Approach

**Framework:** Problem → Data → Methods → Results → Presentation

**Techniques Used:**

#### 1. Exploratory Data Analysis (EDA)
- **Conversion funnel analysis:** 68% of dropoffs occur at product comparison stage (highest complexity)
- **Path analysis:** Users visiting >7 pages before purchase have 42% lower conversion than 3-5 page visitors
- **Temporal patterns:** Cognitive load effects stronger in evening sessions (decision fatigue)

#### 2. Cognitive Load Metrics

**Quantifying UX Complexity:**
- **Information Density Score:** Elements per page / optimal range (based on Miller's Law: 7±2 items)
- **Choice Overload Index:** Number of options × decision depth
- **Navigation Entropy:** -Σ(p(path) × log(p(path))) - measures unpredictability
- **Interaction Cost:** Clicks + scrolls required to complete task

**Validation:**
- Correlated computed metrics with expert UX ratings (r = 0.74)
- A/B tested simplified pages to confirm metric-conversion relationships

#### 3. Model Development

**Classification Models:**
- **Logistic Regression** (baseline, interpretable)
- **Random Forest** (capture non-linear patterns)
- **Gradient Boosting (XGBoost)** - selected for best performance
- **Neural Network (MLP)** - tested but overfitted on this dataset

**Feature Selection:**
- Mutual information scores to rank features
- Recursive Feature Elimination (RFE)
- Final model: 18 features (from initial 47)

**Class Imbalance Handling:**
- SMOTE (Synthetic Minority Over-sampling) for training set
- Stratified cross-validation
- Optimized for F1 score (not just accuracy)

#### 4. Validation Strategy
- **Train/test split:** 70/30, stratified by conversion
- **Cross-validation:** 5-fold stratified CV
- **Metrics:** AUC-ROC, precision, recall, F1 score
- **Feature importance:** SHAP values for interpretability

**Research Foundations:**
- Sweller (1988) - Cognitive Load Theory
- Iyengar & Lepper (2000) - "The Jam Study" on choice overload
- Nielsen Norman Group - UX complexity heuristics

---

## 📈 Key Results

### Model Performance

| Model | AUC-ROC | Precision | Recall | F1 Score |
|-------|---------|-----------|--------|----------|
| **XGBoost** | **0.87** | 0.79 | 0.82 | 0.80 |
| Random Forest | 0.84 | 0.76 | 0.79 | 0.77 |
| Logistic Reg | 0.78 | 0.71 | 0.73 | 0.72 |
| Baseline (Random) | 0.50 | - | - | - |

### Feature Importance (Top 5)

| Feature | SHAP Value | Interpretation |
|---------|------------|----------------|
| Page Revisit Count | 0.24 | Indecision signal (strong negative impact on conversion) |
| Navigation Entropy | 0.19 | Complex paths reduce conversion |
| Time on Product Page | 0.16 | U-shaped: too short or too long both harm conversion |
| Scroll Reversals | 0.14 | Information overload indicator |
| Choice Overload Index | 0.12 | Paradox of choice effect |

### Key Findings

✅ **Finding 1:** High navigation entropy (complex paths) reduces conversion by **38%** compared to linear paths

✅ **Finding 2:** **Choice overload threshold: 9 options**—conversion drops 23% when users face >9 product variants

✅ **Finding 3:** Page revisits (indecision) are strongest predictor—each revisit reduces conversion odds by **14%**

✅ **Finding 4:** **Optimal product page time: 45-90 seconds**—shorter suggests superficial evaluation, longer indicates confusion

✅ **Finding 5:** Simplified UX intervention increased conversion by **12%** in A/B test (validated model predictions)

**Visual Summary:**
![Cognitive Load vs Conversion](reports/figures/cognitive_load_conversion.png)
*Conversion rate decreases as cognitive load increases (quantified)*

![Choice Overload Impact](reports/figures/choice_overload.png)
*Conversion rate by number of product options—drop-off after 9 options*

![Before/After UX Simplification](reports/figures/before_after_ux.png)
*A/B test results: simplified navigation improved conversion by 12%*

---

## 💼 Business Impact

**For Businesses:**
- 🎯 **Increase conversion rate by 12%** through data-driven UX simplification
- 📊 **Identify friction points:** Prioritize UX improvements with highest ROI
- 🔍 **Optimize product catalogs:** Reduce choice overload strategically
- ⚡ **Personalization:** Adapt complexity to user segments (novice vs. expert shoppers)

**For Consumers:**
- 👤 **Reduced decision fatigue:** Clearer pathways to desired products
- 🚀 **Faster decisions:** Streamlined navigation saves time
- 🤝 **Higher satisfaction:** Lower cognitive load correlates with post-purchase confidence

**ROI Estimation:**
For an e-commerce site with $10M annual revenue:
- Baseline conversion rate: 2.4%
- Traffic: 2M annual visitors
- Avg. order value: $208

**After UX optimization (+12% conversion):**
- New conversion rate: 2.69%
- Additional conversions: 5,800/year
- Revenue increase: 5,800 × $208 = **$1.21M/year**
- UX redesign cost: ~$100k
- **ROI: 1110% in year 1**

---

## 🎨 Portfolio Artifacts

### Primary Deliverables

#### 1. Executive Presentation Deck
- **Format:** PowerPoint/PDF (20 slides)
- **Content:**
  - Problem statement and business case
  - Methodology overview (simplified for non-technical stakeholders)
  - Key findings with visual evidence
  - Before/after UX comparison (mockups + metrics)
  - Actionable recommendations for design team
- **[View Presentation (PDF)](#)** | **[SlideShare Link](#)**

#### 2. Technical Documentation
- **Jupyter Notebooks:**
  - `01_eda_clickstream_analysis.ipynb` - Exploratory data analysis
  - `02_cognitive_load_metrics.ipynb` - Feature engineering
  - `03_conversion_prediction_model.ipynb` - ML classification
  - `04_ab_test_validation.ipynb` - UX intervention results
- **[View Notebooks](#)**

#### 3. Written Analysis
- **Medium Article:** "The Hidden Cost of Complexity: How Cognitive Load Kills Conversions"
  - Real-world case study with anonymized data
  - Interactive charts (embedded Plotly)
  - UX design recommendations
  - Psychology of choice overload
- **[Read Article](#)**

#### 4. Before/After UX Mockups
- **Visual Comparison:**
  - Original complex product page (annotated with friction points)
  - Simplified redesign (data-driven changes highlighted)
  - Conversion lift metrics overlaid
- **[View Mockups](#)**

---

## 🛠️ Tech Stack

**Programming & Analysis:**
- **Python 3.9**: Core language
- **pandas, NumPy**: Data manipulation
- **scikit-learn**: Classification models, preprocessing, SMOTE
- **XGBoost**: Gradient boosting for final model
- **imbalanced-learn**: Handling class imbalance

**Visualization:**
- **matplotlib, seaborn**: Static plots
- **Plotly**: Interactive funnel charts, path visualizations
- **Sankey diagrams**: User flow visualization

**Feature Engineering:**
- **scipy**: Entropy calculations
- **networkx**: Navigation path graph analysis

**Tools & Workflow:**
- **Jupyter Lab**: Analysis and documentation
- **Git**: Version control
- **Google Analytics API**: Data extraction (simulated)

---

## 📁 Project Structure

```
consumer-cognitive-load/
├── data/
│   ├── raw/
│   │   ├── clickstream_events.csv
│   │   ├── session_metadata.csv
│   │   ├── purchase_data.csv
│   │   └── ux_complexity_scores.csv
│   ├── processed/
│   │   ├── sessions_with_features.parquet
│   │   └── cognitive_load_metrics.csv
│   └── interim/
│       └── navigation_paths.json
├── notebooks/
│   ├── 01_eda_clickstream_analysis.ipynb
│   ├── 02_cognitive_load_metrics.ipynb
│   ├── 03_conversion_prediction_model.ipynb
│   └── 04_ab_test_validation.ipynb
├── src/
│   ├── data/
│   │   └── preprocess_clickstream.py
│   ├── features/
│   │   ├── cognitive_load.py
│   │   └── behavioral_metrics.py
│   ├── models/
│   │   ├── train_classifier.py
│   │   └── evaluate.py
│   └── visualization/
│       ├── plot_funnels.py
│       └── sankey_flows.py
├── models/
│   ├── xgboost_conversion_model.pkl
│   └── feature_scaler.pkl
├── reports/
│   ├── figures/
│   │   ├── cognitive_load_conversion.png
│   │   ├── choice_overload.png
│   │   ├── before_after_ux.png
│   │   └── user_flow_sankey.html
│   ├── presentation_deck.pdf
│   └── ux_recommendations.pdf
├── tests/
│   └── test_cognitive_load_metrics.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 How to Run

### Prerequisites

```bash
Python 3.8+
pip package manager
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/consumer-cognitive-load.git
cd consumer-cognitive-load

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

#### Full Pipeline
```bash
# Process clickstream → engineer features → train model → evaluate
python src/main.py
```

#### Step-by-Step
```bash
# 1. Preprocess clickstream data
python src/data/preprocess_clickstream.py

# 2. Calculate cognitive load metrics
python src/features/cognitive_load.py

# 3. Train conversion prediction model
python src/models/train_classifier.py

# 4. Evaluate and interpret
python src/models/evaluate.py
```

#### Interactive Exploration
```bash
jupyter lab notebooks/01_eda_clickstream_analysis.ipynb
```

### Generating Visualizations

```bash
# Create user flow Sankey diagram
python src/visualization/sankey_flows.py

# Generate conversion funnel plots
python src/visualization/plot_funnels.py
```

---

## 🔮 Future Enhancements

- [ ] **Real-time monitoring:** Dashboard for live cognitive load tracking
- [ ] **Personalized complexity:** Adapt UX based on user expertise (novice vs. power users)
- [ ] **Eye-tracking integration:** Add gaze patterns for deeper cognitive load insights
- [ ] **Causal inference:** Use propensity score matching to isolate UX effects from confounders
- [ ] **Multi-device analysis:** Compare cognitive load effects across mobile/desktop/tablet
- [ ] **Recommendation system:** Auto-suggest UX simplifications based on clickstream patterns

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note:** This is a portfolio project using synthetic/anonymized data.

---

## 📬 Contact

**[Your Name]**
📧 Email: your.email@example.com
💼 LinkedIn: [linkedin.com/in/yourprofile](#)
🐙 GitHub: [github.com/yourusername](#)
📝 Portfolio: [yourwebsite.com](#)

---

## 🙏 Acknowledgments

- Research foundation: Sweller (Cognitive Load Theory), Iyengar & Lepper (Choice Overload)
- Inspired by Nielsen Norman Group UX research
- Clickstream analysis methodology informed by Google Analytics best practices

---

**⭐ If you found this project useful, please consider giving it a star!**

---

## 📚 Related Projects

- [Cognitive Bias Detection](#)
- [Adaptive Learning System](#)
- [Behavioral Nudges for Habit Formation](#)
