# Nutrition and Cognitive Focus

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Analysis](https://img.shields.io/badge/Analysis-Regression-yellow)

> **Portfolio Project** | Behavioral Data Science & Applied Psychology

Modeling the relationship between dietary patterns and cognitive performance to generate evidence-based nutritional recommendations for knowledge workers.

🔗 **[Data Story Blog](#)** | 📊 **[Interactive Visualizations](#)** | 📈 **[Correlation Analysis](#)**

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
Knowledge workers report productivity fluctuations throughout the day but rarely connect these patterns to dietary choices. Nutritional impact on cognitive performance is discussed in popular media but lacks personalized, data-driven insights.

**Objective:**
Quantify the relationship between meal composition (macronutrients, meal timing, caloric density) and cognitive performance metrics (focus duration, task accuracy, mental energy) to provide actionable dietary recommendations.

**Why It Matters:**
- **For Individuals:** Optimize diet for peak mental performance and sustained energy
- **For Organizations:** Understand how workplace food options affect employee productivity
- **Research Gap:** Most nutrition-cognition studies are lab-based; real-world longitudinal data on knowledge workers is limited

---

## 📊 Data Sources

| Data Type | Source | Volume | Key Features |
|-----------|--------|--------|--------------|
| Food Diaries | Mobile app (MyFitnessPal-style) | 150 participants, 90 days | Meals logged with macros (carbs, protein, fat), timing, calories |
| Cognitive Tests | Daily assessments | 13,500 test sessions | Working memory (N-back), attention (Stroop), processing speed |
| Productivity Logs | Time tracking (RescueTime) | 13,500 user-days | Hours of focused work, task completion, productivity score |
| Context Variables | Self-reported + sensors | Daily | Sleep quality, exercise, stress level, caffeine intake |

**Data Pipeline:**
1. **Collection:** Multi-source data synchronized by timestamp and user ID
2. **Preprocessing:**
   - **Food Diaries:** Standardized portion sizes, calculated macro ratios
   - **Cognitive Tests:** Z-score normalization per user (control for individual baselines)
   - **Missing Data:** Forward-filled up to 2-day gaps (conservative approach)
3. **Feature Engineering:**
   - **Nutritional Metrics:**
     - Macro ratios (% carbs, protein, fat)
     - Glycemic load proxy (simple carbs %)
     - Meal timing relative to work hours
     - Caloric density and meal size
   - **Temporal Features:**
     - Time since last meal
     - Post-meal windows (0-2hr, 2-4hr, 4-6hr)
     - Breakfast quality score (protein-to-carb ratio)
4. **Target Variables:**
   - Focus duration (hours of deep work)
   - Cognitive test composite score
   - Self-reported mental clarity (1-10 scale)

---

## 🔬 Methodology

### Analytical Approach

**Framework:** Problem → Data → Methods → Results → Presentation

**Techniques Used:**

#### 1. Exploratory Data Analysis (EDA)
- **Correlation analysis:** Protein % positively correlated with afternoon focus (r = 0.42)
- **Meal timing patterns:** Large carb-heavy lunches associated with 2-4pm productivity dip
- **Individual variability:** Wide inter-individual differences suggest personalization is critical

#### 2. Model Development

**Regression Models:**
- **Linear Regression** (baseline for interpretability)
- **Ridge Regression** (L2 regularization for multicollinearity)
- **Random Forest Regressor** (capture non-linear relationships)
- **Gradient Boosting (XGBoost)** - selected for best performance

**Target Variables (separate models):**
1. **Focus Duration** (hours of deep work)
2. **Cognitive Test Score** (composite: memory + attention + processing speed)
3. **Mental Clarity** (self-reported)

**Feature Selection:**
- Recursive Feature Elimination (RFE)
- Correlation thresholds to remove redundant features
- Domain expertise (nutrition science principles)
- Final models use 14-18 features (from initial 32)

**Clustering for Personalization:**
- **K-Means Clustering** on nutritional patterns
- Identified 4 dietary personas:
  1. **High-Carb Consumers** (40%): >55% carbs
  2. **Balanced Eaters** (28%): Macro ratios within 30/30/40
  3. **High-Protein Enthusiasts** (20%): >35% protein
  4. **Irregular Eaters** (12%): Erratic meal timing and composition

#### 3. Validation Strategy
- **Time-based split:** Train on first 75 days, test on final 15 days (no future leakage)
- **Cross-validation:** Time-series CV with expanding window
- **Metrics:** R² score, RMSE, MAE
- **Baseline comparison:** Predict today's performance = yesterday's (naive model)
- **Stratified analysis:** Separate models per dietary persona (personalization)

**Research Foundations:**
- Benton & Parker (1998) - Breakfast, blood glucose, and cognition
- Gomez-Pinilla (2008) - Brain foods: Effects of nutrients on brain function
- Lieberman et al. (2005) - Effects of glucose and caffeine on cognitive performance

---

## 📈 Key Results

### Model Performance (Predicting Focus Duration)

| Model | R² Score | RMSE (hours) | MAE (hours) |
|-------|----------|--------------|-------------|
| **XGBoost** | **0.67** | 0.94 | 0.71 |
| Random Forest | 0.64 | 1.02 | 0.78 |
| Ridge Regression | 0.56 | 1.18 | 0.89 |
| Baseline (Naive) | 0.31 | 1.64 | 1.25 |

### Feature Importance (Top 10)

| Feature | Importance Score | Direction |
|---------|------------------|-----------|
| Protein % | 0.18 | ↑ Higher protein → better focus |
| Time since last meal | 0.15 | ↑ Optimal window: 2-3 hours |
| Simple carbs % | 0.14 | ↓ High simple carbs → energy crash |
| Sleep quality (previous night) | 0.12 | ↑ (Control variable) |
| Meal timing (breakfast) | 0.11 | ↑ Earlier breakfast → better AM focus |
| Caloric density | 0.09 | ↓ Heavy meals → afternoon slump |
| Fat % | 0.08 | ↑ Moderate fat → sustained energy |
| Caffeine intake | 0.07 | ↑ (Up to 300mg, then diminishing) |
| Complex carbs % | 0.04 | ↑ Slow-release energy |
| Hydration | 0.02 | ↑ (Weak but consistent) |

### Key Findings

✅ **Finding 1:** **Protein-rich breakfasts** (>25g protein) predict **2.1 hours more focus** than carb-heavy breakfasts (<10g protein)

✅ **Finding 2:** **Post-lunch dip** is 3x worse after meals with >60% simple carbs—complex carbs show minimal dip

✅ **Finding 3:** Optimal meal timing for focus: **2-3 hours post-meal**—too soon = digestive load, too long = hunger distraction

✅ **Finding 4:** **Individual variability is high**—persona-specific models improve R² by +0.11 vs. one-size-fits-all

✅ **Finding 5:** Combined diet+sleep model outperforms diet-only by +0.15 R²—**sleep quality is dominant factor**, but diet is actionable

**Visual Summary:**
![Protein and Focus Correlation](reports/figures/protein_focus_scatter.png)
*Scatter plot: Protein % vs. afternoon focus hours (positive correlation)*

![Meal Timing Impact](reports/figures/meal_timing_performance.png)
*Line plot: Cognitive performance by hours since last meal (optimal window: 2-3hrs)*

![Dietary Personas](reports/figures/dietary_personas.png)
*Radar chart comparing macro ratios and performance across 4 personas*

---

## 💼 Business Impact

**For Individuals:**
- 🎯 **Optimize diet for peak performance:** Data-driven meal planning for focus
- 📊 **Personalized recommendations:** Tailored to dietary preferences and metabolic responses
- 🔍 **Identify problem patterns:** Recognize meals that cause energy crashes
- ⚡ **Sustained energy:** Avoid afternoon slumps with strategic meal composition

**For Organizations:**
- 💼 **Optimize workplace food options:** Cafeteria/snack choices that support productivity
- 📈 **Wellness program design:** Nutrition interventions backed by data
- 🎓 **Employee education:** Share evidence-based dietary guidelines
- 💡 **Policy considerations:** Meal timing for meetings, flexible lunch schedules

**ROI Estimation:**
For a knowledge-work organization with 200 employees:
- Avg. focus hours lost to poor nutrition: **0.8 hours/day** (based on model predictions)
- Cost: 200 employees × 0.8 hrs × 250 days × $60/hr = **$2.4M/year**
- Nutrition optimization intervention (education + cafeteria upgrade): **$50k**
- Even 25% improvement = **$600k/year productivity gain**
- **ROI: 1100% annually**

---

## 🎨 Portfolio Artifacts

### Primary Deliverables

#### 1. Data Story Blog
- **Medium Article:** "Eat Smarter, Think Clearer: The Data-Driven Guide to Nutrition for Knowledge Workers"
  - Personal journey narrative (anonymized participant case study)
  - Interactive Plotly visualizations embedded
  - Actionable takeaways (breakfast recipes, meal timing tips)
  - Debunking myths with data (e.g., "keto for focus")
- **[Read Blog Post](#)**

#### 2. Interactive Visualizations
- **Built with:** Plotly + HTML export
- **Charts:**
  - Correlation heatmap (nutrients vs. cognitive metrics)
  - 3D scatter: Protein/Carbs/Fat % colored by focus score
  - Time-series: Daily nutrition and performance trends
  - Persona comparison radar charts
- **[View Gallery](#)** | **[Try Interactive Demo](#)**

#### 3. Technical Documentation
- **Jupyter Notebooks:**
  - `01_eda_nutrition_patterns.ipynb` - Exploratory data analysis
  - `02_feature_engineering.ipynb` - Nutritional metrics creation
  - `03_regression_modeling.ipynb` - Predictive models
  - `04_clustering_personas.ipynb` - Dietary segmentation
  - `05_results_visualization.ipynb` - Publication-quality plots
- **[View Notebooks](#)**

#### 4. Evidence-Based Recommendations Guide
- **PDF Report:** "Nutritional Guidelines for Cognitive Performance"
  - Summary of findings
  - Meal templates (breakfast, lunch, snacks)
  - Timing strategies
  - Individualization framework
- **[Download Guide (PDF)](#)**

---

## 🛠️ Tech Stack

**Programming & Analysis:**
- **Python 3.9**: Core language
- **pandas, NumPy**: Data manipulation
- **scikit-learn**: Regression models, clustering, preprocessing
- **XGBoost**: Gradient boosting for final model
- **scipy, statsmodels**: Statistical testing (correlation, ANOVA)

**Visualization:**
- **matplotlib, seaborn**: Static EDA plots
- **Plotly**: Interactive 3D scatter, time-series charts
- **Plotly Express**: Rapid exploratory visualization

**Statistical Analysis:**
- **pingouin**: Partial correlation, robust statistics
- **scipy**: Pearson/Spearman correlation, hypothesis testing

**Tools & Workflow:**
- **Jupyter Lab**: Analysis and documentation
- **Git**: Version control

---

## 📁 Project Structure

```
nutrition-focus/
├── data/
│   ├── raw/
│   │   ├── food_diaries.csv
│   │   ├── cognitive_tests.csv
│   │   ├── productivity_logs.csv
│   │   └── context_variables.csv
│   ├── processed/
│   │   ├── nutrition_performance_merged.parquet
│   │   └── macro_features.csv
│   └── interim/
│       └── user_baselines.csv
├── notebooks/
│   ├── 01_eda_nutrition_patterns.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_regression_modeling.ipynb
│   ├── 04_clustering_personas.ipynb
│   └── 05_results_visualization.ipynb
├── src/
│   ├── data/
│   │   └── preprocess_nutrition.py
│   ├── features/
│   │   └── build_nutrition_features.py
│   ├── models/
│   │   ├── train_regression.py
│   │   ├── cluster_personas.py
│   │   └── evaluate.py
│   └── visualization/
│       └── plot_correlations.py
├── models/
│   ├── xgboost_focus_model.pkl
│   ├── kmeans_personas.pkl
│   └── feature_scaler.pkl
├── reports/
│   ├── figures/
│   │   ├── protein_focus_scatter.png
│   │   ├── meal_timing_performance.png
│   │   ├── dietary_personas.png
│   │   └── correlation_heatmap.html
│   ├── nutrition_guidelines.pdf
│   └── data_story_draft.md
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
git clone https://github.com/yourusername/nutrition-focus.git
cd nutrition-focus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

#### Full Pipeline
```bash
# Process data → engineer features → train models → generate visualizations
python src/main.py
```

#### Step-by-Step
```bash
# 1. Preprocess nutrition and performance data
python src/data/preprocess_nutrition.py

# 2. Build nutritional features
python src/features/build_nutrition_features.py

# 3. Train regression models
python src/models/train_regression.py

# 4. Cluster dietary personas
python src/models/cluster_personas.py

# 5. Evaluate models
python src/models/evaluate.py
```

#### Interactive Exploration
```bash
jupyter lab notebooks/01_eda_nutrition_patterns.ipynb
```

### Generating Visualizations

```bash
# Create correlation plots
python src/visualization/plot_correlations.py

# Output: reports/figures/correlation_heatmap.html
```

---

## 🔮 Future Enhancements

- [ ] **Mobile app integration:** Sync with MyFitnessPal, Cronometer for real-time tracking
- [ ] **Causal inference:** Use DoWhy to isolate diet effects from confounders (sleep, exercise)
- [ ] **Micronutrient analysis:** Expand beyond macros to vitamins, minerals, polyphenols
- [ ] **Longitudinal models:** Time-series forecasting for multi-day nutrition effects
- [ ] **Recommendation system:** Meal suggestions based on upcoming work demands (e.g., creative vs. analytical tasks)
- [ ] **Genetic integration:** Explore nutrigenomics (how genetics modify diet-cognition relationships)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note:** This is a research/portfolio project using anonymized data. Recommendations are informational, not medical advice.

---

## 📬 Contact

**[Your Name]**
📧 Email: your.email@example.com
💼 LinkedIn: [linkedin.com/in/yourprofile](#)
🐙 GitHub: [github.com/yourusername](#)
📝 Portfolio: [yourwebsite.com](#)

---

## 🙏 Acknowledgments

- Research foundation: Gomez-Pinilla (brain foods), Lieberman et al. (glucose and cognition)
- Inspired by Quantified Self nutrition experiments
- Nutritional data methodology informed by MyFitnessPal and Cronometer APIs

---

**⭐ If you found this project useful, please consider giving it a star!**

---

## 📚 Related Projects

- [Sleep Pattern Analytics](#)
- [Personalized Wellness Optimization](#)
- [Stress Detection](#)
