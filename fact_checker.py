import pandas as pd
import re

class FactChecker:
    def __init__(self, db_path="fact_database.csv"):
        self.db_path = db_path
        self.load_database()

    def load_database(self):
        try:
            self.db = pd.read_csv(self.db_path)
        except Exception as e:
            self.db = pd.DataFrame(columns=["subject", "relation", "object", "source"])

    def add_fact(self, subject, relation, obj, source):
        new_fact = pd.DataFrame([{
            "subject": subject,
            "relation": relation,
            "object": obj,
            "source": source
        }])
        self.db = pd.concat([self.db, new_fact], ignore_index=True)
        self.db.to_csv(self.db_path, index=False)
        self.load_database()

    def normalize(self, text):
        if not isinstance(text, str):
            return ""
        # Lowercase
        text = text.lower()
        # Remove punctuation except numbers
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def get_tokens(self, text):
        text = self.normalize(text)
        stopwords = {"the", "is", "of", "and", "has", "a", "an", "in", "to", "are", "was", "were", "s"}
        tokens = [w for w in text.split() if w not in stopwords]
        return set(tokens)
        
    def extract_numbers(self, text):
        return set(re.findall(r'\d+', text))

    def check_claim(self, claim):
        # Very short claims are already handled by input validation, but let's be safe
        claim_tokens = self.get_tokens(claim)
        if not claim_tokens:
            return "UNVERIFIED", None, None
            
        claim_numbers = self.extract_numbers(claim)

        best_match = None
        best_score = 0
        
        for idx, row in self.db.iterrows():
            subj_tokens = self.get_tokens(row['subject'])
            obj_tokens = self.get_tokens(row['object'])
            
            # Check if subject is mentioned in the claim
            if not subj_tokens:
                continue
                
            # Strict match: ALL subject tokens must be present in the claim
            if subj_tokens.issubset(claim_tokens):
                best_match = row
                break

        if best_match is not None:
            obj_tokens = self.get_tokens(best_match['object'])
            obj_numbers = self.extract_numbers(best_match['object'])
            
            # If claim has numbers, check them carefully
            if claim_numbers:
                if claim_numbers.issubset(obj_numbers) and len(claim_numbers) > 0:
                    return "SUPPORTED", best_match, best_match['source']
                else:
                    return "CONTRADICTED", best_match, best_match['source']
            
            # Otherwise, check non-numeric object tokens
            obj_words = obj_tokens - obj_numbers
            if not obj_words:
                # If object is only numbers but claim has no numbers, it's unverified or contradicted
                return "CONTRADICTED", best_match, best_match['source']
                
            # SMART MATCH: Remove spaces to fix issues like "pawan kalyan" vs "pawankalyan"
            claim_no_spaces = self.normalize(claim).replace(" ", "")
            obj_no_spaces = self.normalize(best_match['object']).replace(" ", "")
            
            if obj_no_spaces in claim_no_spaces or claim_no_spaces in obj_no_spaces:
                return "SUPPORTED", best_match, best_match['source']
                
            # If any significant object word is in the claim, we consider it supported
            # E.g. "modi" or "murmu"
            overlap = obj_words.intersection(claim_tokens)
            if len(overlap) > 0:
                return "SUPPORTED", best_match, best_match['source']
            else:
                return "CONTRADICTED", best_match, best_match['source']

        return "UNVERIFIED", None, None
