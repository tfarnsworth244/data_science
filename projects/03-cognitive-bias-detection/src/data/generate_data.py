"""
Generate synthetic cognitive bias detection dataset.

Creates realistic text samples exhibiting various cognitive biases
to demonstrate NLP text classification and bias detection systems.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# Define cognitive bias types and their characteristics
BIAS_TYPES = {
    'confirmation_bias': {
        'description': 'Tendency to search for, interpret, or recall information that confirms preexisting beliefs',
        'templates': [
            "I knew {outcome} would happen because {evidence}. This just proves what I've always believed about {topic}.",
            "Look at {evidence} - it clearly shows {conclusion}. Anyone who disagrees is just ignoring the facts.",
            "I've always said {belief}, and {evidence} confirms it. I don't need to look at contradictory data.",
            "The data supports my view that {conclusion}. I'm not interested in arguments against it.",
            "This research validates what I already knew: {belief}. Other studies are probably flawed."
        ]
    },
    'anchoring_bias': {
        'description': 'Over-reliance on the first piece of information encountered',
        'templates': [
            "The initial estimate was {anchor}, so I think {final_value} is reasonable even though new data suggests {alternative}.",
            "When I first heard the price was {anchor}, that stuck with me. Now {final_value} seems like a good deal.",
            "My first impression was {anchor}, and I can't shake that feeling even after learning {new_info}.",
            "The original forecast said {anchor}, so anything close to that seems acceptable to me.",
            "I based my decision on the initial figure of {anchor}. Later adjustments don't change my view much."
        ]
    },
    'availability_bias': {
        'description': 'Overestimating likelihood of events based on their mental availability',
        'templates': [
            "I just read about {recent_event}, so I'm very concerned about {risk}. It seems to be happening everywhere.",
            "Since {event} happened recently, I think the probability of {outcome} is much higher than statistics show.",
            "Everyone's talking about {topic} lately, so it must be a major issue that needs immediate attention.",
            "I saw {news} on social media today, which makes me think {conclusion}. It's clearly a widespread problem.",
            "After hearing about {incident}, I'm convinced {outcome} is very likely. The news is full of similar stories."
        ]
    },
    'sunk_cost_fallacy': {
        'description': 'Continuing a behavior due to previously invested resources',
        'templates': [
            "We've already invested {amount} in this project, so we need to continue even though {negative_info}.",
            "I've spent {time_amount} on this, so I can't quit now. That would mean all that effort was wasted.",
            "After putting in {resource}, we have to see it through despite {problem}. We're too far in to stop.",
            "We've committed {investment} to this approach. Changing course now would mean admitting it was wrong.",
            "Given how much {resource} we've already used, we should keep going even if {alternative} makes more sense."
        ]
    },
    'hindsight_bias': {
        'description': 'Believing past events were more predictable than they actually were',
        'templates': [
            "I knew {outcome} would happen all along. The signs were obvious in retrospect.",
            "It was clear that {result} was coming. Anyone could have predicted it based on {factor}.",
            "Looking back, {event} was inevitable. I'm surprised others didn't see it coming.",
            "I always suspected {outcome} would occur. It seems so obvious now that it happened.",
            "Of course {result} happened - all the indicators pointed to it. It was completely predictable."
        ]
    },
    'bandwagon_effect': {
        'description': 'Adopting beliefs because many others hold them',
        'templates': [
            "Everyone is switching to {option}, so it must be the right choice. I should do the same.",
            "Most people believe {belief}, so there's probably something to it. I'll go along with the majority.",
            "All the experts are recommending {action}, so I'll follow their lead. They can't all be wrong.",
            "The trend is clearly toward {direction}. I don't want to be left behind, so I'm on board.",
            "If {number}% of people think {belief}, it's probably correct. I trust the wisdom of crowds."
        ]
    },
    'recency_bias': {
        'description': 'Giving more weight to recent events than historical data',
        'templates': [
            "The last {period} showed {trend}, so I expect that pattern to continue despite historical {data}.",
            "Recent performance indicates {conclusion}. Past data from years ago isn't as relevant anymore.",
            "Based on what happened {timeframe}, I predict {outcome}. Long-term trends don't matter as much.",
            "The latest {results} are most important. Historical averages don't reflect current reality.",
            "I'm focusing on {recent_data} because that's what's happening now. Older data is outdated."
        ]
    },
    'neutral': {
        'description': 'Balanced reasoning without evident cognitive bias',
        'templates': [
            "The data shows {finding}, though we should consider {alternative}. More analysis is needed to draw conclusions.",
            "While {evidence} suggests {conclusion}, there are several confounding factors to examine further.",
            "Initial results indicate {trend}, but we need to validate this with additional data before deciding.",
            "The analysis presents {information}. However, we should seek diverse perspectives before concluding.",
            "Current findings show {result}. We should review contradictory evidence and consider multiple interpretations."
        ]
    }
}

def generate_text_sample(bias_type, context_params):
    """Generate a text sample exhibiting a specific bias."""
    template = random.choice(BIAS_TYPES[bias_type]['templates'])

    # Fill in template with context-specific parameters
    try:
        text = template.format(**context_params)
    except KeyError:
        text = template

    return text

def generate_context_params(bias_type):
    """Generate realistic parameters for text templates."""

    # Common topics for decision-making
    topics = ['technology adoption', 'market trends', 'employee performance', 'investment strategy',
              'product development', 'customer behavior', 'risk management', 'strategic planning']

    outcomes = ['succeed', 'fail', 'improve', 'decline', 'change', 'stabilize']
    beliefs = ['innovation drives success', 'quality matters most', 'customers prefer simplicity',
               'data-driven decisions work best', 'experience beats credentials']

    # Bias-specific parameters
    if bias_type == 'confirmation_bias':
        return {
            'outcome': random.choice(outcomes),
            'evidence': f"the {random.choice(['recent', 'latest', 'new'])} {random.choice(['study', 'report', 'data', 'analysis'])}",
            'topic': random.choice(topics),
            'conclusion': f"{random.choice(['strong', 'clear', 'obvious'])} {random.choice(['correlation', 'pattern', 'trend'])}",
            'belief': random.choice(beliefs)
        }

    elif bias_type == 'anchoring_bias':
        anchor_val = random.randint(50, 500)
        return {
            'anchor': f"${anchor_val}k" if random.random() > 0.5 else f"{anchor_val} units",
            'final_value': f"${int(anchor_val * random.uniform(0.8, 1.2))}k",
            'alternative': f"${int(anchor_val * random.uniform(1.3, 1.8))}k",
            'new_info': random.choice(['updated market data', 'revised estimates', 'new competitive analysis'])
        }

    elif bias_type == 'availability_bias':
        events = ['a data breach', 'a product recall', 'a market crash', 'a viral campaign',
                 'a merger announcement', 'a regulatory change', 'a supply chain disruption']
        return {
            'recent_event': random.choice(events),
            'event': random.choice(events),
            'risk': random.choice(['security threats', 'market volatility', 'reputational damage', 'operational risks']),
            'outcome': random.choice(['business disruption', 'financial loss', 'customer churn', 'competitive disadvantage']),
            'topic': random.choice(topics),
            'conclusion': f"we need to {random.choice(['act immediately', 'invest heavily', 'change strategy', 'pivot quickly'])}",
            'news': random.choice(['a crisis', 'a success story', 'a failure', 'an innovation']),
            'incident': random.choice(events)
        }

    elif bias_type == 'sunk_cost_fallacy':
        return {
            'amount': f"${random.randint(100, 1000)}k",
            'time_amount': f"{random.randint(6, 36)} months",
            'resource': random.choice(['significant resources', 'substantial capital', 'countless hours', 'major effort']),
            'investment': f"${random.randint(100, 500)}k and {random.randint(12, 48)} months",
            'negative_info': random.choice(['results are disappointing', 'metrics are declining', 'the market has shifted',
                                          'competitors have moved ahead', 'costs are escalating']),
            'problem': random.choice(['poor performance', 'technical challenges', 'market resistance', 'budget overruns']),
            'alternative': random.choice(['a new approach', 'cutting losses', 'pivoting strategy', 'trying something different'])
        }

    elif bias_type == 'hindsight_bias':
        return {
            'outcome': random.choice(['the market downturn', 'the product success', 'the merger', 'the reorganization']),
            'result': random.choice(['the company failed', 'sales increased', 'the strategy worked', 'customers left']),
            'event': random.choice(['the acquisition', 'the pivot', 'the launch', 'the expansion']),
            'factor': random.choice(['early indicators', 'market conditions', 'customer feedback', 'competitive moves'])
        }

    elif bias_type == 'bandwagon_effect':
        return {
            'option': random.choice(['cloud services', 'agile methodology', 'AI tools', 'remote work', 'subscription models']),
            'belief': random.choice(beliefs),
            'action': random.choice(['digital transformation', 'sustainability initiatives', 'customer-centric design',
                                    'data monetization', 'ecosystem partnerships']),
            'direction': random.choice(['automation', 'personalization', 'decentralization', 'platform business models']),
            'number': random.randint(60, 85)
        }

    elif bias_type == 'recency_bias':
        return {
            'period': random.choice(['quarter', '6 months', 'year', 'few months']),
            'trend': random.choice(['growth', 'decline', 'volatility', 'stability', 'improvement']),
            'data': random.choice(['patterns', 'averages', 'trends', 'benchmarks']),
            'timeframe': random.choice(['last quarter', 'recently', 'in the past few months', 'this year']),
            'conclusion': random.choice(['continued growth', 'ongoing challenges', 'sustained improvement', 'persistent issues']),
            'results': random.choice(['performance metrics', 'customer feedback', 'sales data', 'engagement numbers']),
            'recent_data': random.choice(['Q4 results', 'latest surveys', 'current KPIs', 'this month\'s data'])
        }

    else:  # neutral
        return {
            'finding': random.choice(['a correlation', 'a trend', 'a pattern', 'an anomaly']),
            'alternative': random.choice(['alternative explanations', 'different perspectives', 'opposing views', 'counterarguments']),
            'evidence': random.choice(['preliminary data', 'initial findings', 'early results', 'first analysis']),
            'conclusion': random.choice(['a positive outcome', 'a causal relationship', 'a significant effect', 'a clear direction']),
            'trend': random.choice(['improvement', 'change', 'stability', 'growth']),
            'information': random.choice(['mixed signals', 'promising indicators', 'concerning patterns', 'useful insights']),
            'result': random.choice(['positive outcomes', 'unexpected findings', 'interesting patterns', 'notable changes'])
        }

def generate_cognitive_bias_data(n_samples=5000):
    """Generate synthetic cognitive bias detection dataset."""

    print(f"Generating cognitive bias dataset with {n_samples} samples...")

    # Bias distribution (including neutral/balanced reasoning)
    bias_types = list(BIAS_TYPES.keys())

    # Weight neutral samples slightly lower to have more bias examples
    weights = [0.15, 0.14, 0.14, 0.13, 0.13, 0.12, 0.10, 0.09]

    data = []

    for sample_id in range(n_samples):
        # Select bias type
        bias_type = np.random.choice(bias_types, p=weights)

        # Generate context parameters
        context = generate_context_params(bias_type)

        # Generate text
        text = generate_text_sample(bias_type, context)

        # Add metadata
        source_types = ['Email', 'Report', 'Meeting Note', 'Decision Memo', 'Survey Response', 'Chat Message']
        departments = ['Strategy', 'Marketing', 'Operations', 'Finance', 'Product', 'HR', 'Sales', 'Engineering']

        # Text features
        word_count = len(text.split())
        char_count = len(text)

        # Confidence score (how strongly the bias is exhibited)
        # Neutral has lower confidence, biased samples have higher confidence
        if bias_type == 'neutral':
            confidence = np.random.beta(2, 3)  # Lower confidence for neutral
        else:
            confidence = np.random.beta(5, 2)  # Higher confidence for biased samples

        data.append({
            'sample_id': f"SAMPLE{str(sample_id + 1).zfill(5)}",
            'text': text,
            'bias_type': bias_type,
            'bias_description': BIAS_TYPES[bias_type]['description'],
            'source_type': random.choice(source_types),
            'department': random.choice(departments),
            'word_count': word_count,
            'char_count': char_count,
            'confidence_score': np.round(confidence, 3),
            'is_biased': 0 if bias_type == 'neutral' else 1,
            'timestamp': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S')
        })

    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":
    import os

    # Generate dataset
    cognitive_df = generate_cognitive_bias_data(n_samples=5000)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'cognitive_bias_samples.csv')
    cognitive_df.to_csv(output_path, index=False)

    print(f"\n✓ Dataset generated successfully!")
    print(f"\nDataset Shape: {cognitive_df.shape}")
    print(f"Saved to: {output_path}")

    print(f"\n📊 Bias Type Distribution:")
    print(cognitive_df['bias_type'].value_counts().sort_values(ascending=False))

    print(f"\n📈 Biased vs Neutral:")
    print(cognitive_df['is_biased'].value_counts())
    print(f"Biased: {cognitive_df['is_biased'].mean() * 100:.1f}%")

    print(f"\n📝 Source Type Distribution:")
    print(cognitive_df['source_type'].value_counts())

    print(f"\n🎯 Sample Statistics:")
    print(f"Avg word count: {cognitive_df['word_count'].mean():.1f}")
    print(f"Avg confidence: {cognitive_df['confidence_score'].mean():.3f}")

    print(f"\n💡 Example Samples:")
    print("\n" + "="*80)
    for bias in ['confirmation_bias', 'anchoring_bias', 'neutral']:
        sample = cognitive_df[cognitive_df['bias_type'] == bias].iloc[0]
        print(f"\n{bias.upper().replace('_', ' ')}:")
        print(f"Text: {sample['text'][:150]}...")
        print(f"Confidence: {sample['confidence_score']:.3f}")
