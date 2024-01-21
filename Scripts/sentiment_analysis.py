# Scripts/sentiment_analysis.py
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from torch.nn.functional import softmax
import torch

def load_distilbert_model():
    # Load pre-trained DistilBERT model and tokenizer
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    return model, tokenizer

def analyze_sentiment(text, model, tokenizer):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

    # Forward pass through the model
    outputs = model(**inputs)
    
    # Get predicted probabilities for each class (positive, negative)
    probabilities = softmax(outputs.logits, dim=1).detach().numpy()[0]

    # Choose the sentiment label with the highest probability
    sentiment_label = "Positive" if probabilities[1] > probabilities[0] else "Negative"

    return sentiment_label, probabilities

if __name__ == "__main__":
    # Example usage
    model, tokenizer = load_distilbert_model()
    text_to_analyze = "This is a positive example."
    sentiment_label, probabilities = analyze_sentiment(text_to_analyze, model, tokenizer)
    print(f"Sentiment: {sentiment_label}")
    print(f"Probabilities: Positive={probabilities[1]:.4f}, Negative={probabilities[0]:.4f}")
