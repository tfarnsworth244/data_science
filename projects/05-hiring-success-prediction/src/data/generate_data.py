"""
Generate synthetic hiring success prediction dataset.

Creates realistic data for candidate assessments, interviews, and outcomes
to demonstrate classification models for predicting hiring success.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_hiring_data(n_candidates=3000):
    """Generate synthetic hiring and performance data."""

    print(f"Generating hiring data for {n_candidates} candidates...")

    data = []

    # Job roles and their characteristics
    job_roles = {
        'Software Engineer': {'base_difficulty': 0.65, 'tech_weight': 0.8, 'culture_weight': 0.5},
        'Data Scientist': {'base_difficulty': 0.70, 'tech_weight': 0.85, 'culture_weight': 0.5},
        'Product Manager': {'base_difficulty': 0.60, 'tech_weight': 0.5, 'culture_weight': 0.8},
        'Sales Representative': {'base_difficulty': 0.55, 'tech_weight': 0.3, 'culture_weight': 0.9},
        'Customer Support': {'base_difficulty': 0.45, 'tech_weight': 0.4, 'culture_weight': 0.85},
        'Marketing Specialist': {'base_difficulty': 0.50, 'tech_weight': 0.5, 'culture_weight': 0.75},
        'UX Designer': {'base_difficulty': 0.55, 'tech_weight': 0.6, 'culture_weight': 0.7},
        'Operations Manager': {'base_difficulty': 0.60, 'tech_weight': 0.4, 'culture_weight': 0.75}
    }

    departments = list(job_roles.keys())
    experience_levels = ['Entry', 'Mid', 'Senior', 'Lead']

    for candidate_id in range(1, n_candidates + 1):
        # Candidate basic info
        role = random.choice(departments)
        role_config = job_roles[role]
        experience_level = np.random.choice(experience_levels, p=[0.35, 0.40, 0.20, 0.05])

        # Experience (years)
        exp_ranges = {'Entry': (0, 2), 'Mid': (3, 6), 'Senior': (7, 12), 'Lead': (13, 20)}
        years_experience = np.random.uniform(*exp_ranges[experience_level])

        # Education level
        education = np.random.choice(['Bachelor', 'Master', 'PhD', 'Associate'],
                                    p=[0.50, 0.35, 0.10, 0.05])
        education_score = {'Associate': 0.6, 'Bachelor': 0.75, 'Master': 0.9, 'PhD': 1.0}[education]

        # Assessment scores (0-100)
        # Technical assessment
        tech_base = np.random.beta(5, 3) * 100
        tech_score = np.clip(tech_base + (years_experience * 2) + (education_score * 10), 0, 100)

        # Problem-solving assessment
        problem_solving_score = np.clip(np.random.beta(5, 3) * 100 + (years_experience * 1.5), 0, 100)

        # Communication assessment
        communication_score = np.clip(np.random.beta(6, 3) * 100, 0, 100)

        # Cultural fit score (1-10)
        culture_fit_score = np.random.beta(5, 3) * 9 + 1

        # Interview rounds (typically 3-5)
        num_interview_rounds = random.randint(3, 5)

        # Interview scores (average across rounds)
        interview_scores = []
        for _ in range(num_interview_rounds):
            score = np.random.beta(6, 3) * 9 + 1  # 1-10 scale
            interview_scores.append(score)
        avg_interview_score = np.mean(interview_scores)

        # Reference check (1-5)
        reference_score = np.random.beta(7, 2) * 4 + 1

        # Background check result
        background_clear = np.random.choice([0, 1], p=[0.05, 0.95])

        # Previous companies worked at
        num_prev_companies = int(np.clip(years_experience / 2.5, 1, 8))

        # Average tenure at previous companies (years)
        avg_tenure_prev = np.random.gamma(2, 1.5) if num_prev_companies > 0 else 0

        # Months to hire (time from application to offer)
        months_to_hire = np.random.gamma(2, 0.75)

        # Salary expectation vs offer
        salary_expectation_k = np.random.gamma(10, 6)
        salary_offered_k = salary_expectation_k * np.random.uniform(0.95, 1.15)

        # Calculate success probability
        # Success is influenced by multiple factors
        success_factors = []

        # Technical competence (weighted by role)
        tech_factor = (tech_score / 100) * role_config['tech_weight']
        success_factors.append(tech_factor)

        # Interview performance
        interview_factor = (avg_interview_score / 10) * 0.7
        success_factors.append(interview_factor)

        # Cultural fit (weighted by role)
        culture_factor = (culture_fit_score / 10) * role_config['culture_weight']
        success_factors.append(culture_factor)

        # Communication skills
        comm_factor = (communication_score / 100) * 0.6
        success_factors.append(comm_factor)

        # Experience relevance
        exp_factor = min(years_experience / 10, 1.0) * 0.5
        success_factors.append(exp_factor)

        # Stability (average tenure)
        stability_factor = min(avg_tenure_prev / 3, 1.0) * 0.4
        success_factors.append(stability_factor)

        # References
        ref_factor = (reference_score / 5) * 0.3
        success_factors.append(ref_factor)

        # Background check
        if not background_clear:
            success_factors.append(-0.5)

        # Calculate base success probability
        base_success_prob = np.mean(success_factors)

        # Add some noise
        success_prob = np.clip(base_success_prob + np.random.normal(0, 0.15), 0, 1)

        # Determine actual success (binary outcome)
        is_successful = 1 if np.random.random() < success_prob else 0

        # Performance after hire (only if successful)
        if is_successful:
            performance_rating = np.random.beta(6, 3) * 4 + 1  # 1-5 rating
            retention_12mo = 1 if np.random.random() < 0.85 else 0
            time_to_productivity_weeks = int(np.random.gamma(3, 2))
        else:
            performance_rating = np.random.beta(2, 5) * 4 + 1
            retention_12mo = 1 if np.random.random() < 0.50 else 0
            time_to_productivity_weeks = int(np.random.gamma(5, 3))

        # Application date
        hire_date = datetime.now() - timedelta(days=random.randint(365, 730))

        data.append({
            'candidate_id': f"CAND{str(candidate_id).zfill(5)}",
            'role': role,
            'experience_level': experience_level,
            'years_experience': np.round(years_experience, 1),
            'education': education,
            'technical_score': np.round(tech_score, 1),
            'problem_solving_score': np.round(problem_solving_score, 1),
            'communication_score': np.round(communication_score, 1),
            'culture_fit_score': np.round(culture_fit_score, 2),
            'num_interview_rounds': num_interview_rounds,
            'avg_interview_score': np.round(avg_interview_score, 2),
            'reference_score': np.round(reference_score, 2),
            'background_clear': background_clear,
            'num_previous_companies': num_prev_companies,
            'avg_tenure_previous': np.round(avg_tenure_prev, 2),
            'months_to_hire': np.round(months_to_hire, 2),
            'salary_expectation_k': np.round(salary_expectation_k, 1),
            'salary_offered_k': np.round(salary_offered_k, 1),
            'salary_delta_pct': np.round((salary_offered_k - salary_expectation_k) / salary_expectation_k * 100, 1),
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'success_12mo': is_successful,
            'performance_rating': np.round(performance_rating, 2),
            'retained_12mo': retention_12mo,
            'time_to_productivity_weeks': time_to_productivity_weeks
        })

    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    import os

    # Generate dataset
    hiring_df = generate_hiring_data(n_candidates=3000)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'hiring_candidates.csv')
    hiring_df.to_csv(output_path, index=False)

    print(f"\n✓ Dataset generated successfully!")
    print(f"\nDataset Shape: {hiring_df.shape}")
    print(f"Saved to: {output_path}")

    print(f"\n📊 Role Distribution:")
    print(hiring_df['role'].value_counts())

    print(f"\n📈 Success Rate:")
    success_rate = hiring_df['success_12mo'].mean() * 100
    print(f"Successful hires: {success_rate:.1f}%")
    print(hiring_df['success_12mo'].value_counts())

    print(f"\n💼 Experience Level Distribution:")
    print(hiring_df['experience_level'].value_counts())

    print(f"\n🎓 Education Distribution:")
    print(hiring_df['education'].value_counts())

    print(f"\n📊 Key Metrics (Successful vs Unsuccessful):")
    comparison = hiring_df.groupby('success_12mo').agg({
        'technical_score': 'mean',
        'avg_interview_score': 'mean',
        'culture_fit_score': 'mean',
        'years_experience': 'mean',
        'performance_rating': 'mean'
    }).round(2)
    comparison.index = ['Unsuccessful', 'Successful']
    print(comparison)

    print(f"\n🔍 Retention Rate:")
    retention_rate = hiring_df['retained_12mo'].mean() * 100
    print(f"Overall retention: {retention_rate:.1f}%")
    print(f"Successful hires retention: {hiring_df[hiring_df['success_12mo']==1]['retained_12mo'].mean()*100:.1f}%")
    print(f"Unsuccessful hires retention: {hiring_df[hiring_df['success_12mo']==0]['retained_12mo'].mean()*100:.1f}%")
