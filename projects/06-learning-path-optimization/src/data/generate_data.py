"""
Generate synthetic learning path optimization dataset.

Creates realistic data for courses, learners, interactions, and outcomes
to demonstrate recommendation systems for personalized learning.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_learning_data(n_learners=1500, n_courses=200):
    """Generate synthetic learning platform data."""

    print(f"Generating learning data for {n_learners} learners and {n_courses} courses...")

    # Course catalog
    course_categories = {
        'Programming': ['Python Basics', 'JavaScript Fundamentals', 'Java Advanced', 'C++ Programming',
                       'Web Development', 'Mobile App Development', 'Full Stack Development'],
        'Data Science': ['Statistics Fundamentals', 'Machine Learning', 'Deep Learning', 'Data Visualization',
                        'SQL for Analytics', 'Big Data Processing', 'NLP Basics'],
        'Business': ['Project Management', 'Agile Methodology', 'Leadership Skills', 'Strategic Thinking',
                    'Business Analytics', 'Marketing Fundamentals', 'Finance Basics'],
        'Design': ['UI/UX Design', 'Graphic Design', 'Product Design', 'Design Thinking',
                  'Prototyping Tools', 'Visual Design', 'User Research'],
        'Cloud': ['AWS Fundamentals', 'Azure Basics', 'Cloud Architecture', 'DevOps Essentials',
                 'Kubernetes', 'Docker Containers', 'Cloud Security']
    }

    difficulty_levels = ['Beginner', 'Intermediate', 'Advanced']

    # Generate course catalog
    courses = []
    course_id = 1

    for category, course_names in course_categories.items():
        for i in range(int(n_courses / len(course_categories))):
            if len(course_names) > 0:
                course_name = random.choice(course_names)
            else:
                course_name = f"{category} Course {i+1}"

            difficulty = random.choice(difficulty_levels)
            duration_hours = {
                'Beginner': np.random.uniform(5, 15),
                'Intermediate': np.random.uniform(15, 40),
                'Advanced': np.random.uniform(40, 80)
            }[difficulty]

            courses.append({
                'course_id': f"CRS{str(course_id).zfill(4)}",
                'course_name': f"{course_name} {difficulty}",
                'category': category,
                'difficulty': difficulty,
                'duration_hours': np.round(duration_hours, 1),
                'num_modules': int(duration_hours / 2) + random.randint(1, 5),
                'avg_rating': np.round(np.random.beta(8, 2) * 4 + 1, 2),  # 1-5 rating
                'num_enrollments': int(np.random.pareto(1.5) * 100 + 50)
            })
            course_id += 1

    courses_df = pd.DataFrame(courses[:n_courses])

    # Generate learner profiles
    learners = []
    for learner_id in range(1, n_learners + 1):
        age = int(np.clip(np.random.normal(28, 8), 18, 65))

        # Primary interest area
        primary_interest = random.choice(list(course_categories.keys()))

        # Learning style
        learning_style = random.choice(['Visual', 'Hands-on', 'Theoretical', 'Mixed'])

        # Time availability (hours per week)
        time_available_weekly = np.clip(np.random.gamma(3, 2), 1, 30)

        # Learning goal
        learning_goal = random.choice(['Career Switch', 'Skill Enhancement', 'Personal Interest',
                                      'Certification', 'Promotion'])

        # Experience level in primary area
        experience_level = random.choice(['Beginner', 'Intermediate', 'Advanced'])

        learners.append({
            'learner_id': f"LRN{str(learner_id).zfill(5)}",
            'age': age,
            'primary_interest': primary_interest,
            'learning_style': learning_style,
            'time_available_weekly': np.round(time_available_weekly, 1),
            'learning_goal': learning_goal,
            'experience_level': experience_level,
            'joined_date': (datetime.now() - timedelta(days=random.randint(30, 730))).strftime('%Y-%m-%d')
        })

    learners_df = pd.DataFrame(learners)

    # Generate course enrollments and interactions
    enrollments = []
    enrollment_id = 1

    for _, learner in learners_df.iterrows():
        # Number of courses enrolled (follows power law - most take few, some take many)
        num_enrollments = int(np.clip(np.random.pareto(2) * 3 + 1, 1, 15))

        # Preference for courses in primary interest
        available_courses = courses_df.copy()

        for _ in range(num_enrollments):
            # 70% chance to pick from primary interest, 30% from others
            if random.random() < 0.7:
                course_pool = available_courses[available_courses['category'] == learner['primary_interest']]
            else:
                course_pool = available_courses[available_courses['category'] != learner['primary_interest']]

            if len(course_pool) == 0:
                course_pool = available_courses

            if len(course_pool) == 0:
                continue

            course = course_pool.sample(1).iloc[0]

            # Enrollment date
            enroll_date = datetime.strptime(learner['joined_date'], '%Y-%m-%d') + \
                         timedelta(days=random.randint(0, 180))

            # Completion likelihood based on multiple factors
            difficulty_match = 1.0 if course['difficulty'] == learner['experience_level'] else 0.6
            interest_match = 1.0 if course['category'] == learner['primary_interest'] else 0.7
            time_factor = min(learner['time_available_weekly'] / 10, 1.0)

            completion_prob = np.clip(difficulty_match * interest_match * time_factor * 0.7, 0, 1)
            completion_prob += np.random.uniform(-0.2, 0.2)  # Add noise
            completion_prob = np.clip(completion_prob, 0, 1)

            is_completed = 1 if random.random() < completion_prob else 0

            # Progress percentage
            if is_completed:
                progress_pct = 100
                days_to_complete = int(course['duration_hours'] / learner['time_available_weekly'] * 7 * \
                                      np.random.uniform(1.0, 1.5))
                completion_date = (enroll_date + timedelta(days=days_to_complete)).strftime('%Y-%m-%d')
            else:
                progress_pct = int(np.random.beta(2, 5) * 100)
                days_to_complete = None
                completion_date = None

            # Time spent (hours)
            if is_completed:
                time_spent_hours = course['duration_hours'] * np.random.uniform(0.9, 1.3)
            else:
                time_spent_hours = course['duration_hours'] * (progress_pct / 100) * np.random.uniform(0.5, 1.2)

            # Video watch time percentage
            video_watch_pct = np.clip(progress_pct + np.random.uniform(-15, 15), 0, 100)

            # Quiz scores (if attempted)
            if progress_pct > 20:
                quiz_score_avg = np.clip(np.random.beta(5, 3) * 100, 0, 100)
                num_quiz_attempts = int(progress_pct / 20)
            else:
                quiz_score_avg = None
                num_quiz_attempts = 0

            # Assignment completion
            assignments_completed = int((progress_pct / 100) * course['num_modules'] * 0.8)

            # User rating (if completed)
            if is_completed:
                user_rating = np.round(np.random.beta(7, 2) * 4 + 1, 1)
            else:
                user_rating = None

            enrollments.append({
                'enrollment_id': f"ENR{str(enrollment_id).zfill(6)}",
                'learner_id': learner['learner_id'],
                'course_id': course['course_id'],
                'enroll_date': enroll_date.strftime('%Y-%m-%d'),
                'completion_date': completion_date,
                'is_completed': is_completed,
                'progress_pct': progress_pct,
                'time_spent_hours': np.round(time_spent_hours, 1),
                'video_watch_pct': np.round(video_watch_pct, 1),
                'quiz_score_avg': np.round(quiz_score_avg, 1) if quiz_score_avg else None,
                'num_quiz_attempts': num_quiz_attempts,
                'assignments_completed': assignments_completed,
                'user_rating': user_rating,
                'days_to_complete': days_to_complete
            })

            enrollment_id += 1

            # Remove course from available pool to avoid duplicates
            available_courses = available_courses[available_courses['course_id'] != course['course_id']]

    enrollments_df = pd.DataFrame(enrollments)

    return courses_df, learners_df, enrollments_df


if __name__ == "__main__":
    import os

    # Generate datasets
    courses, learners, enrollments = generate_learning_data(n_learners=1500, n_courses=200)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(output_dir, exist_ok=True)

    courses_path = os.path.join(output_dir, 'courses.csv')
    learners_path = os.path.join(output_dir, 'learners.csv')
    enrollments_path = os.path.join(output_dir, 'enrollments.csv')

    courses.to_csv(courses_path, index=False)
    learners.to_csv(learners_path, index=False)
    enrollments.to_csv(enrollments_path, index=False)

    print(f"\n✓ Datasets generated successfully!")

    print(f"\n📚 Courses Dataset:")
    print(f"  Shape: {courses.shape}")
    print(f"  Saved to: {courses_path}")

    print(f"\n👥 Learners Dataset:")
    print(f"  Shape: {learners.shape}")
    print(f"  Saved to: {learners_path}")

    print(f"\n📊 Enrollments Dataset:")
    print(f"  Shape: {enrollments.shape}")
    print(f"  Saved to: {enrollments_path}")

    print(f"\n📈 Category Distribution:")
    print(courses['category'].value_counts())

    print(f"\n🎓 Completion Rate:")
    completion_rate = enrollments['is_completed'].mean() * 100
    print(f"Overall completion: {completion_rate:.1f}%")

    print(f"\n⏱️ Average Time Investment:")
    print(f"Time spent per enrollment: {enrollments['time_spent_hours'].mean():.1f} hours")
    print(f"Time for completed courses: {enrollments[enrollments['is_completed']==1]['time_spent_hours'].mean():.1f} hours")

    print(f"\n🎯 Learning Goals:")
    print(learners['learning_goal'].value_counts())

    print(f"\n⭐ Average Course Rating:")
    print(f"{courses['avg_rating'].mean():.2f} / 5.0")

    print(f"\n🔢 Enrollments per Learner:")
    enrollments_per_learner = enrollments.groupby('learner_id').size()
    print(f"Average: {enrollments_per_learner.mean():.1f}")
    print(f"Median: {enrollments_per_learner.median():.1f}")
