# Data Sources for Behavioral Data Science Portfolio

This document lists all real-world datasets used across the 10 portfolio projects.

## Project 1: Employee Burnout Prediction
**Dataset**: Are Your Employees Burning Out?
- **Source**: Kaggle
- **URL**: https://www.kaggle.com/datasets/blurredmachine/are-your-employees-burning-out
- **Alternative**: IBM HR Analytics Employee Attrition & Performance
  - URL: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- **Size**: 22,750 rows
- **Features**: Employee ID, Date of Joining, Gender, Company Type, WFH Setup, Designation, Resource Allocation, Mental Fatigue Score, Burn Rate
- **License**: Open Data

## Project 2: Wellness Optimization
**Dataset**: FitBit Fitness Tracker Data
- **Source**: Kaggle
- **URL**: https://www.kaggle.com/datasets/arashnic/fitbit
- **Alternative**: Gym Members Exercise Dataset
  - URL: https://www.kaggle.com/datasets/valakhorasani/gym-members-exercise-dataset
- **Size**: 940 users, 30 days of tracking
- **Features**: Daily activity, steps, calories, intensities, heart rate, sleep, weight
- **License**: CC0 Public Domain

## Project 3: Cognitive Bias Detection
**Dataset**: Custom dataset from academic research
- **Source**: BiasBuster Dataset (EMNLP 2024)
- **URL**: https://github.com/cognitive-bias-research (if available)
- **Alternative**: Build custom dataset from Reddit CMV, Wikipedia NPOV edits
- **Size**: 13,465 prompts with cognitive bias labels
- **Features**: Text samples, bias type, context
- **License**: Research use

## Project 4: Sleep Pattern Analytics
**Dataset**: Sleep Health and Lifestyle Dataset
- **Source**: Kaggle
- **URL**: https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset
- **Alternative**: Sleep Efficiency Dataset
  - URL: https://www.kaggle.com/datasets/equilibriumm/sleep-efficiency
- **Size**: 400+ sleep records
- **Features**: Sleep duration, quality, disorders, lifestyle factors, health metrics
- **License**: Open Data

## Project 5: Hiring Success Prediction
**Dataset**: 70k+ Job Applicants Data (Human Resource)
- **Source**: Kaggle
- **URL**: https://www.kaggle.com/datasets/ayushtankha/70k-job-applicants-data-human-resource
- **Alternative**: Recruitment Dataset
  - URL: https://www.kaggle.com/datasets/surendra365/recruitement-dataset
- **Size**: 70,000+ applicant records
- **Features**: Education, experience, training, age, previous companies, skills
- **License**: Open Data

## Project 6: Learning Path Optimization
**Dataset**: Predict Online Course Engagement Dataset
- **Source**: Kaggle
- **URL**: https://www.kaggle.com/datasets/rabieelkharoua/predict-online-course-engagement-dataset
- **Alternative**: Online Course Student Engagement Metrics
  - URL: https://www.kaggle.com/datasets/thedevastator/online-course-student-engagement-metrics
- **Size**: 100,000+ course enrollment records
- **Features**: User demographics, course details, engagement metrics, completion status
- **License**: Open Data

## Project 7: Team Composition Analysis
**Dataset**: GitHub collaboration network data or Software Development Team Performance
- **Source**: GitHub API or academic research
- **Alternative**: Build from Git commits and collaboration patterns
- **Size**: TBD
- **Features**: Developer interactions, commit patterns, team metrics
- **License**: Public/MIT

## Project 8: Meeting Effectiveness NLP
**Dataset**: AMI Meeting Corpus or Custom corporate meeting dataset
- **Source**: Academic research / Edinburgh University
- **URL**: http://groups.inf.ed.ac.uk/ami/corpus/
- **Alternative**: Synthesize from meeting best practices
- **Size**: 100 hours of meeting recordings
- **Features**: Transcripts, annotations, participant info, outcomes
- **License**: Academic research use

## Project 9: Burnout Prediction Time Series
**Dataset**: IBM HR Analytics (Extended with time series simulation)
- **Source**: Kaggle
- **URL**: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- **Size**: 1,470 employees with multiple time points
- **Features**: Satisfaction, performance, work-life balance over time
- **License**: Open Data

## Project 10: Employee Engagement CNN
**Dataset**: Employee Attrition Classification Dataset
- **Source**: Kaggle
- **URL**: https://www.kaggle.com/datasets/stealthtechnologies/employee-attrition-dataset
- **Alternative**: Employee Attrition Prediction Dataset
  - URL: https://www.kaggle.com/datasets/ziya07/employee-attrition-prediction-dataset
- **Size**: Multiple survey waves with engagement metrics
- **Features**: Job satisfaction, environment satisfaction, work-life balance, attrition
- **License**: Open Data

---

## Data Download Instructions

### Install Kaggle API
```bash
pip install kaggle
```

### Configure Kaggle Credentials
1. Go to https://www.kaggle.com/settings
2. Create new API token (downloads kaggle.json)
3. Place in ~/.kaggle/kaggle.json
4. Set permissions: chmod 600 ~/.kaggle/kaggle.json

### Download Datasets
Each project includes a download script that uses the Kaggle API or direct download methods.

Run from project root:
```bash
cd projects/XX-project-name/src/data
python download_data.py
```

---

## Data Ethics and Usage

All datasets used in this portfolio:
- Are publicly available or properly licensed
- Have been ethically sourced
- Respect privacy (no personal identifiable information)
- Include proper attribution and citations
- Follow license terms for usage and redistribution

For academic datasets, proper citation is included in project READMEs.
