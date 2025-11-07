# Data Setup Guide

This portfolio uses **real-world datasets** from Kaggle and other open sources. Follow this guide to download and prepare all datasets.

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# 1. Set up Kaggle API credentials (one-time setup)
# Visit https://www.kaggle.com/settings → API → Create New Token
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# 2. Run automated download script
./setup_kaggle.sh
```

### Option 2: Manual Setup

Install Kaggle API:
```bash
pip install kaggle
```

Download datasets individually:
```bash
cd projects/01-employee-burnout/src/data
python download_data.py
```

---

## Dataset Overview

| Project | Dataset | Source | Size | Status |
|---------|---------|--------|------|--------|
| 01 - Employee Burnout | Are Your Employees Burning Out? | Kaggle | 22,750 rows | ✅ Real |
| 02 - Wellness Optimization | FitBit Fitness Tracker Data | Kaggle | 940 users | ✅ Real |
| 03 - Cognitive Bias Detection | Custom Synthetic | Generated | 5,000 samples | ⚙️ Synthetic |
| 04 - Sleep Pattern Analytics | Sleep Health and Lifestyle | Kaggle | 400+ records | ✅ Real |
| 05 - Hiring Success Prediction | 70k+ Job Applicants Data | Kaggle | 70,000 rows | ✅ Real |
| 06 - Learning Path Optimization | Online Course Engagement | Kaggle | 100k+ records | ✅ Real |
| 07 - Team Composition Analysis | Custom Network Data | Generated | 500 employees | ⚙️ Synthetic |
| 08 - Meeting Effectiveness NLP | Custom Transcripts | Generated | 1,000 meetings | ⚙️ Synthetic |
| 09 - Burnout Time Series | Longitudinal Synthetic | Generated | 15,600 obs | ⚙️ Synthetic |
| 10 - Employee Engagement CNN | IBM HR Analytics | Kaggle | 1,470 employees | ✅ Real |

### Why Some Projects Use Synthetic Data?

**Project 3 (Cognitive Bias)**: Real cognitive bias datasets require expert psychology annotation and are mostly proprietary research data.

**Project 7 (Team Composition)**: Organizational team interaction data is sensitive and not publicly available at scale.

**Project 8 (Meeting Effectiveness)**: Corporate meeting transcripts contain confidential information; public datasets are limited.

**Project 9 (Burnout Time Series)**: Longitudinal employee data with weekly measurements is rare due to privacy concerns.

---

## Detailed Setup Instructions

### Step 1: Kaggle API Setup

1. **Create Kaggle Account**
   - Visit https://www.kaggle.com and sign up

2. **Generate API Token**
   - Go to https://www.kaggle.com/settings
   - Scroll to "API" section
   - Click "Create New Token"
   - This downloads `kaggle.json`

3. **Install Credentials**
   ```bash
   mkdir -p ~/.kaggle
   mv ~/Downloads/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. **Verify Setup**
   ```bash
   kaggle datasets list
   ```

### Step 2: Download Datasets

#### Automated (All Projects)
```bash
./setup_kaggle.sh
```

#### Manual (Individual Projects)

**Project 1 - Employee Burnout**
```bash
cd projects/01-employee-burnout/src/data
python download_data.py
```

**Project 2 - Wellness Optimization**
```bash
cd projects/02-wellness-optimization/src/data
python download_data.py
```

**Project 4 - Sleep Pattern Analytics**
```bash
cd projects/04-sleep-pattern-analytics/src/data
python download_data.py
```

**Project 5 - Hiring Success**
```bash
cd projects/05-hiring-success-prediction/src/data
python download_data.py
```

**Project 6 - Learning Path Optimization**
```bash
cd projects/06-learning-path-optimization/src/data
python download_data.py
```

**Project 10 - Employee Engagement**
```bash
cd projects/10-engagement-cnn/src/data
python download_data.py
```

### Step 3: Generate Synthetic Data (For Projects 3, 7, 8, 9)

```bash
# Project 3
python projects/03-cognitive-bias-detection/src/data/generate_data.py

# Project 7
python projects/07-team-composition-analysis/src/data/generate_data.py

# Project 8
python projects/08-meeting-effectiveness-nlp/src/data/generate_data.py

# Project 9
python projects/09-burnout-time-series/src/data/generate_data.py
```

---

## Dataset Details

### Project 1: Employee Burnout Prediction
- **Dataset**: Are Your Employees Burning Out?
- **Features**: Mental Fatigue Score, Burn Rate, Resource Allocation, WFH Setup
- **Target**: Burnout level (continuous)
- **Use Case**: Predict burnout risk and identify key factors

### Project 2: Wellness Optimization
- **Dataset**: FitBit Fitness Tracker Data
- **Features**: Daily steps, calories, heart rate, sleep, activity intensity
- **Use Case**: Cluster users and recommend personalized wellness interventions

### Project 4: Sleep Pattern Analytics
- **Dataset**: Sleep Health and Lifestyle Dataset
- **Features**: Sleep duration, quality, disorders, BMI, blood pressure, stress
- **Use Case**: Correlate sleep patterns with health and productivity metrics

### Project 5: Hiring Success Prediction
- **Dataset**: 70k+ Job Applicants Data
- **Features**: Education, experience, training history, skills, demographics
- **Use Case**: Predict hiring success and optimize recruitment process

### Project 6: Learning Path Optimization
- **Dataset**: Predict Online Course Engagement Dataset
- **Features**: User demographics, course details, engagement, completion
- **Use Case**: Recommend optimal learning paths using collaborative filtering

### Project 10: Employee Engagement CNN
- **Dataset**: IBM HR Analytics Employee Attrition & Performance
- **Features**: Job satisfaction, environment, work-life balance, demographics
- **Use Case**: Predict attrition risk using deep learning on engagement surveys

---

## Troubleshooting

### Kaggle API Not Found
```bash
pip install kaggle
```

### Permission Denied
```bash
chmod 600 ~/.kaggle/kaggle.json
```

### Dataset Download Failed
- Check internet connection
- Verify you've accepted dataset terms on Kaggle website
- Ensure kaggle.json is in correct location
- Try manual download from Kaggle website

### Disk Space Issues
Each dataset ranges from 1MB to 50MB. Total: ~200MB for all real datasets.

---

## Alternative Data Sources

If Kaggle download fails, manually download from:

1. **Kaggle Website**: Visit dataset URL and download ZIP
2. **Extract to project**: Unzip to `projects/XX-project-name/data/raw/`

Dataset URLs are documented in [DATA_SOURCES.md](./DATA_SOURCES.md)

---

## Verification

After setup, verify datasets:

```bash
# Check all data directories
ls -lh projects/*/data/raw/

# Quick verification script
python -c "
import os
projects = ['01-employee-burnout', '02-wellness-optimization', '04-sleep-pattern-analytics',
            '05-hiring-success-prediction', '06-learning-path-optimization', '10-engagement-cnn']
for p in projects:
    path = f'projects/{p}/data/raw'
    files = os.listdir(path) if os.path.exists(path) else []
    print(f'{p}: {len(files)} files')
"
```

---

## Next Steps

After data setup:

1. **Explore Data**: Run EDA notebooks for each project
2. **Build Models**: Execute model training scripts
3. **View Results**: Check reports/figures/ directories
4. **Run Dashboards**: Launch Streamlit/Gradio apps (where available)

See individual project READMEs for specific instructions.
