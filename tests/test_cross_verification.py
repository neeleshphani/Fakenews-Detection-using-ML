import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

def extract_entities(text):
    # Find multi-word capital phrases first, then single capitalized words
    tokens = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', text)
    # Filter out sentence starters that are not entities
    stopwords = {'the', 'this', 'that', 'with', 'from', 'what', 'when', 'where', 'why', 'who', 'how'}
    return [t for t in tokens if t.lower() not in stopwords and len(t) > 2]

def cross_verify_entities(claim):
    entities = extract_entities(claim)
    if len(entities) >= 2:
        e1, e2 = entities[0], entities[1]
        try:
            s1 = wikipedia.summary(e1, sentences=3, auto_suggest=False).lower()
        except Exception:
            try:
                s1 = wikipedia.summary(e1, sentences=3).lower()
            except Exception:
                s1 = ""
                
        try:
            s2 = wikipedia.summary(e2, sentences=3, auto_suggest=False).lower()
        except Exception:
            try:
                s2 = wikipedia.summary(e2, sentences=3).lower()
            except Exception:
                s2 = ""

        # If both entities exist on Wikipedia
        if s1 and s2:
            e1_in_s2 = e1.lower() in s2
            e2_in_s1 = e2.lower() in s1
            
            if not e1_in_s2 and not e2_in_s1:
                return False, f"Entity mismatch: Live Wikipedia records for '{e1}' do not associate with '{e2}', and '{e2}' records do not associate with '{e1}'.", f"Wikipedia Live Web API ({e1} & {e2})"
            elif e1_in_s2 or e2_in_s1:
                return True, f"Live Wikipedia records confirm the factual relationship between '{e1}' and '{e2}'.", f"Wikipedia Live Web API ({e1})"
                
    return None, None, None

tests = [
    "Google was founded by Bill Gates",
    "Google was founded by Larry Page",
    "Apple CEO is Elon Musk",
    "Tesla CEO is Elon Musk",
    "Narendra Modi is the Prime Minister of Russia",
    "Narendra Modi is the Prime Minister of India",
    "Cristiano Ronaldo plays for Real Madrid",
    "Virat Kohli plays for Real Madrid"
]

for t in tests:
    res, reason, src = cross_verify_entities(t)
    v = "TRUE" if res else "FAKE"
    print(f"[{v:4s}] {t:48s} -> {reason[:80]}...")
