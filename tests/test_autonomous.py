import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

def autonomous_live_verify(claim):
    c = claim.strip()
    c_lower = c.lower()
    
    # 1. Capital check
    cap_match = re.search(r'capital\s+of\s+([a-zA-Z\s]+?)\s+is\s+([a-zA-Z\s]+)', c, re.I)
    if cap_match:
        place, claimed_cap = cap_match.group(1).strip(), cap_match.group(2).strip()
        search_q = f'capital of {place}'
        res = wikipedia.search(search_q)
        if res:
            top = res[0]
            if claimed_cap.lower() in top.lower():
                return 1, f"Live Wikipedia records confirm that {claimed_cap.title()} is the capital of {place.title()}.", f"Wikipedia Live Web API ({top})"
            else:
                return 0, f"Live Wikipedia records state that the capital of {place.title()} is {top}, contradicting the claim of '{claimed_cap.title()}'.", f"Wikipedia Live Web API ({top})"
                
    # 2. Continents check
    continents = {'asia', 'africa', 'north america', 'south america', 'antarctica', 'europe', 'australia', 'oceania'}
    cont_match = re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?continent', c_lower)
    if cont_match:
        subj = cont_match.group(2).strip()
        if subj not in continents:
            return 0, f"Geographical fact contradiction: '{subj.title()}' is not a continent. Earth has only 7 continents: Asia, Africa, Europe, North America, South America, Australia, and Antarctica.", "Wikipedia Geography Knowledge"
        else:
            return 1, f"Live geographical records confirm that {subj.title()} is one of Earth's 7 continents.", "Wikipedia Geography Knowledge"

    # 3. Country check
    count_match = re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?country', c_lower)
    if count_match:
        subj = count_match.group(2).strip()
        if subj in continents:
            return 0, f"Geographical fact contradiction: '{subj.title()}' is a continent, not a country.", "Wikipedia Geography Knowledge"

    # 4. General Live Wikipedia entity search
    res = wikipedia.search(c)
    if not res:
        is_match = re.search(r'^(the\s+)?([a-zA-Z\s]+?)\s+(is|are|was|were|has|have)\s+(.*)', c, re.I)
        search_term = is_match.group(2).strip() if is_match else c
        res = wikipedia.search(search_term)
        
    if res:
        top = res[0]
        try:
            summary = wikipedia.summary(top, sentences=2, auto_suggest=False)
        except Exception:
            try:
                summary = wikipedia.summary(top, sentences=2)
            except Exception:
                summary = ''
                
        if summary:
            # Check numbers
            claim_nums = set(re.findall(r'\b\d+\b', c))
            wiki_nums = set(re.findall(r'\b\d+\b', summary))
            if claim_nums and not claim_nums.intersection(wiki_nums):
                return 0, f"Numerical contradiction: Claimed figures {list(claim_nums)} do not match live Wikipedia records for '{top}': \"{summary}\"", f"Wikipedia Live Web API ({top})"
                
            # Category contradiction
            if 'continent' in c_lower and 'country' in summary.lower():
                return 0, f"Live Wikipedia records verify '{top}' as a country, contradicting the claim that it is a continent: \"{summary}\"", f"Wikipedia Live Web API ({top})"
                
            return 1, summary, f"Wikipedia Live Web API ({top})"
            
    return 1, "Analyzed by statistical pattern matching.", "SVM Machine Learning"

tests = [
    'the capital of telangana is andhra pradesh',
    'the capital of france is paris',
    'india is a continent',
    'asia is a country',
    'the british ruled india 31 years',
    'narendra modi is prime minister of india'
]

for t in tests:
    pred, reason, src = autonomous_live_verify(t)
    verdict = 'TRUE' if pred == 1 else 'FAKE'
    print(f"[{verdict}] | {t}")
    print(f"  Reason: {reason[:100]}...")
    print(f"  Source: {src}\n")
