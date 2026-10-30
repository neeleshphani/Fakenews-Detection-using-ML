import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

OPPOSITES = {
    'herbivore': ['carnivore', 'predator', 'meat'],
    'carnivores': ['herbivore', 'plants'],
    'freezes': ['boils', 'evaporates'],
    'boils': ['freezes', 'ice', 'solidifies'],
    'planet': ['star', 'satellite', 'moon'],
    'star': ['planet', 'moon'],
    'moon': ['planet', 'star'],
    'cricket': ['football', 'footballer', 'soccer', 'basketball'],
    'football': ['cricket', 'baseball', 'tennis'],
    'bacteria': ['virus', 'viral'],
    'virus': ['bacterial', 'bacteria'],
    'mammal': ['reptile', 'bird', 'fish', 'amphibian'],
    'reptile': ['mammal', 'amphibian', 'bird'],
    'continent': ['country', 'province', 'state', 'city'],
    'country': ['continent', 'city', 'state']
}

CONTINENTS = {'asia', 'africa', 'north america', 'south america', 'antarctica', 'europe', 'australia', 'oceania'}

def verify_claim_universally(claim):
    claim_clean = claim.strip()
    claim_lower = claim_clean.lower()
    
    # Rule 1: Geographical Continents check
    if 'is a continent' in claim_lower or 'is continent' in claim_lower:
        match_cont = re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?continent', claim_lower)
        if match_cont:
            subj = match_cont.group(2).strip()
            if subj not in CONTINENTS:
                return False, f"Geographical fact contradiction: '{subj.title()}' is not a continent. Earth has only 7 continents: Asia, Africa, Europe, North America, South America, Australia, and Antarctica.", "Geographical Knowledge"
            else:
                return True, f"Geographical fact confirmed: '{subj.title()}' is one of Earth's 7 continents.", "Geographical Knowledge"
                
    if 'is a country' in claim_lower or 'is country' in claim_lower:
        match_count = re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?country', claim_lower)
        if match_count:
            subj = match_count.group(2).strip()
            if subj in CONTINENTS:
                return False, f"Geographical fact contradiction: '{subj.title()}' is a continent, not a country.", "Geographical Knowledge"

    # Rule 2: Capital relationship check
    cap_match = re.search(r'capital\s+of\s+([a-zA-Z\s]+?)\s+is\s+([a-zA-Z\s]+)', claim_clean, re.I)
    if cap_match:
        place, claimed_cap = cap_match.group(1).strip(), cap_match.group(2).strip()
        search_res = wikipedia.search(f"capital of {place}")
        if search_res:
            top_c = search_res[0]
            try:
                summ = wikipedia.summary(top_c, sentences=2, auto_suggest=False)
            except Exception:
                summ = wikipedia.summary(top_c, sentences=2)
            if claimed_cap.lower() in top_c.lower() or claimed_cap.lower() in summ.lower():
                return True, f"Live Wikipedia records confirm that '{claimed_cap.title()}' is the capital of {place.title()}.", f"Wikipedia Live Web API ({top_c})"
            else:
                return False, f"Live Wikipedia records state that the capital of {place.title()} is '{top_c}', contradicting the claim of '{claimed_cap.title()}'.", f"Wikipedia Live Web API ({top_c})"

    # Rule 3: Leadership relationship check
    role_match = re.search(r'(prime minister|president|chief minister|chancellor|king|queen)\s+of\s+([a-zA-Z\s]+?)\s+is\s+([a-zA-Z\s]+)', claim_clean, re.I)
    if role_match:
        role, country, person = role_match.group(1).strip(), role_match.group(2).strip(), role_match.group(3).strip()
        res_p = wikipedia.search(person)
        if res_p:
            top_p = res_p[0]
            try:
                summ_p = wikipedia.summary(top_p, sentences=2, auto_suggest=False)
            except Exception:
                summ_p = wikipedia.summary(top_p, sentences=2)
            if country.lower() in summ_p.lower() and role.lower() in summ_p.lower():
                return True, f"Live Wikipedia records confirm that {top_p} is the {role} of {country.title()}: {summ_p}", f"Wikipedia Live Web API ({top_p})"
            else:
                return False, f"Live Wikipedia records state that {top_p} is not the {role} of {country.title()}. True record: {summ_p}", f"Wikipedia Live Web API ({top_p})"

    # Rule 4: Universal Entity Search
    # Extract subject entity: first 2-3 words or nouns before main verb
    verb_match = re.search(r'^(the\s+)?([a-zA-Z\s]+?)\s+(is|are|was|were|has|have|founded|plays|freezes|boils|revolves)\s+(.*)', claim_clean, re.I)
    subject_entity = verb_match.group(2).strip() if verb_match else claim_clean
    predicate_text = verb_match.group(4).strip() if verb_match else ''
    
    # First search for full claim, fallback to subject
    results = wikipedia.search(claim_clean)
    if not results or (results and subject_entity.lower() not in results[0].lower() and len(results[0].split()) > 4):
        results = wikipedia.search(subject_entity)
        
    if not results:
        return None, "No live Wikipedia information found", "None"
        
    top_entity = results[0]
    try:
        summary = wikipedia.summary(top_entity, sentences=3, auto_suggest=False)
    except Exception:
        try:
            summary = wikipedia.summary(top_entity, sentences=3)
        except Exception:
            summary = ""
            
    if not summary:
        return None, "Summary unavailable", top_entity
        
    summ_lower = summary.lower()
    
    # Sub-Check A: Opposites & category clashes
    for word, forbidden_words in OPPOSITES.items():
        if re.search(r'\b' + word + r'\b', claim_lower):
            for f in forbidden_words:
                if re.search(r'\b' + f + r'\b', summ_lower):
                    return False, f"Fact contradiction: Claim asserts '{word}', but live Wikipedia records for '{top_entity}' state: \"{summary}\"", f"Wikipedia Live Web API ({top_entity})"

    # Sub-Check B: Numbers & Dates
    claim_nums = set(re.findall(r'\b\d+\b', claim_clean))
    summ_nums = set(re.findall(r'\b\d+\b', summary))
    if claim_nums and not claim_nums.intersection(summ_nums):
        return False, f"Numerical mismatch: Claim figures {list(claim_nums)} do not match live Wikipedia records for '{top_entity}': \"{summary}\"", f"Wikipedia Live Web API ({top_entity})"

    # Sub-Check C: Named Entity mismatch
    # If the predicate contains a specific named entity (e.g., 'Bill Gates' for Google, 'Cricket' for Ronaldo) that is absent
    pred_entities = re.findall(r'\b[A-Z][a-z]+\b', predicate_text)
    if pred_entities:
        missing_entities = [e for e in pred_entities if e.lower() not in summ_lower]
        if len(missing_entities) == len(pred_entities):
            return False, f"Fact contradiction: Claim associates '{top_entity}' with {missing_entities}, but live Wikipedia records state: \"{summary}\"", f"Wikipedia Live Web API ({top_entity})"

    return True, summary, f"Wikipedia Live Web API ({top_entity})"

test_cases = [
    "water boils at 100 degrees",
    "water freezes at 100 degrees",
    "lions are herbivores",
    "cristiano ronaldo plays cricket",
    "google was founded by bill gates",
    "mount everest is the highest mountain in the world",
    "the capital of france is paris",
    "the capital of germany is munich",
    "the prime minister of russia is modi",
    "the prime minister of india is modi",
    "the british ruled india 31 years"
]

for t in test_cases:
    res, reason, src = verify_claim_universally(t)
    v = "TRUE" if res else "FAKE"
    clean_r = reason.encode('ascii', 'ignore').decode()[:85]
    print(f"[{v:4s}] {t:48s} -> {clean_r}...")
