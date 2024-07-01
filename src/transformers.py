from transformers import RobertaConfig, RobertaForSequenceClassification

# Load the configuration from pre-trained or define your own
config = RobertaConfig.from_pretrained('roberta-base', num_labels=your_num_labels)

# Initialize RoBERTa For Sequence Classification with the specified configuration
model = RobertaForSequenceClassification(config)
