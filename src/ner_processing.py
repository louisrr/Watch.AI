from transformers import RobertaTokenizer, RobertaForTokenClassification, pipeline

def setup_ner_pipeline():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    model = RobertaForTokenClassification.from_pretrained('roberta-base-finetuned-ner').to(device)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, device=0 if device == "cuda" else -1)
    return ner_pipeline

def perform_ner(text):
    ner_pipeline = setup_ner_pipeline()
    ner_results = ner_pipeline(text)
    return ner_results
