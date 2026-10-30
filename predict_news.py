import joblib
import sys
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove special characters but KEEP numbers and spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    print("Loading model and vectorizer...")
    try:
        model = joblib.load('models/fake_news_model.pkl')
        vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
    except Exception as e:
        print("Error loading models. Run train_model.py first.")
        sys.exit(1)
        
    print("Models loaded successfully.\n")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            claim = input("Enter news article: ")
            if claim.lower() == 'exit':
                break
            
            cleaned = clean_text(claim)
            
            # Simple validation based on word count/gibberish for demonstration
            # The full app.py has better validation
            if len(cleaned.split()) < 2:
                print("Invalid / Too short\n")
                continue
                
            vec = vectorizer.transform([cleaned])
            pred = model.predict(vec)[0]
            
            if pred == 1:
                print("REAL NEWS\n")
            else:
                print("FAKE NEWS\n")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
