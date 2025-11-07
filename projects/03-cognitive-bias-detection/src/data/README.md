# Cognitive Bias Detection - Data Notes

## Dataset Status

**Current Approach**: Synthetic data with realistic cognitive bias patterns

### Why Synthetic Data?

Publicly available datasets for cognitive bias detection in text are limited because:
1. Cognitive bias annotation requires expert psychology knowledge
2. Most research datasets are proprietary or require institutional access
3. Real-world bias detection datasets often contain sensitive content

### Alternative Real Data Sources (Requires Manual Setup)

If you want to use real-world data, consider these approaches:

1. **Reddit CMV (Change My View) Dataset**
   - Contains argumentative text that may exhibit confirmation bias
   - Available on: https://www.reddit.com/r/changemyview/

2. **Wikipedia NPOV Edits**
   - Revision history showing bias corrections
   - Available via Wikipedia API

3. **Academic Research Datasets**
   - BiasBuster (EMNLP 2024) - May require contacting authors
   - Contact: Research papers in cognitive bias and NLP

### Current Synthetic Data

The generate_data.py script creates 5,000 text samples exhibiting 7 types of cognitive biases:
- Confirmation bias
- Anchoring bias
- Availability bias
- Sunk cost fallacy
- Hindsight bias
- Bandwagon effect
- Recency bias

This synthetic data is sufficient for:
- Demonstrating NLP classification techniques
- Building and evaluating models
- Portfolio showcase purposes

To generate the data:
```bash
python generate_data.py
```
