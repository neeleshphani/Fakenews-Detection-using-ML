import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

OPPOSITES = {
    'herbivore': ['carnivore', 'predator', 'meat-eating', 'apex predator'],
    'carnivore': ['herbivore', 'plant-eating', 'vegetation'],
    'freezes': ['boils', 'evaporates'],
    'boils': ['freezes', 'solidifies', 'ice'],
    'planet': ['star', 'satellite', 'asteroid'],
    'star': ['planet', 'moon'],
    'moon': ['planet', 'star'],
    'cricket': ['football', 'footballer', 'soccer', 'basketball', 'tennis'],
    'football': ['cricket', 'baseball'],
    'bacteria': ['virus', 'viral'],
    'virus': ['bacterial', 'bacteria'],
    'mammal': ['reptile', 'bird', 'fish', 'amphibian'],
    'reptile': ['mammal', 'amphibian', 'bird']
}

def universal_fact_check(claim):
    claim_clean = claim.strip()
    claim_lower = claim_clean.lower()
    
    # 1. Search Wikipedia for the claim itself
    search_res = wikipedia.search(claim_clean)
    if not search_res:
        return None, 'No information found', 'None'
        
    top_page = search_res[0]
    try:
        summary = wikipedia.summary(top_page, sentences=3, auto_suggest=False)
    except Exception:
        try:
            summary = wikipedia.summary(top_page, sentences=3)
        except Exception:
            summary = ''
            
    if not summary:
        return None, 'Summary unavailable', top_page
        
    summ_lower = summary.lower()
    
    # Check A: Opposites & category clashes
    for word, forbidden_words in OPPOSITES.items():
        if re.search(r'\b' + word + r'\b', claim_lower):
            for f in forbidden_words:
                if re.search(r'\b' + f + r'\b', summ_lower):
                    return False, f"Fact contradiction: Claim asserts '{word}', but live Wikipedia records for '{top_page}' state: \"{summary}\"", top_page
                    
    # Check B: Numbers & Years
    claim_nums = set(re.findall(r'\b\d+\b', claim_clean))
    summ_nums = set(re.findall(r'\b\d+\b', summary))
    if claim_nums and not claim_nums.intersection(summ_nums):
        return False, f"Numerical mismatch: Claim numbers {list(claim_nums)} do not match live Wikipedia records for '{top_page}': \"{summary}\"", top_page
        
    # Check C: Key terms missing from official page
    words = [w for w in re.findall(r'\b[A-Za-z]{4,}\b', claim_clean) if w.lower() not in {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'what', 'which', 'about', 'around'}]
    if len(words) >= 3:
        missing = [w for w in words if w.lower() not in summ_lower]
        if len(missing) >= len(words) / 2:
            return False, f"Entity mismatch: Live Wikipedia records for '{top_page}' do not support claimed details {missing}. Found: \"{summary}\"", top_page

    return True, summary, top_page

diverse_test_claims = [
    'lion is a herbivore animal',
    'water freezes at 100 degrees',
    'cristiano ronaldo plays cricket',
    'google was founded by bill gates',
    'mount everest is the highest mountain in the world',
    'the earth revolves around the sun'
]

for c in diverse_test_claims:
    is_true, reason, page = universal_fact_check(c)
    verdict = 'TRUE' if is_true else 'FAKE'
    print(f"[{verdict}] {c}")
    print(f" -> Page: {page}")
    print(f" -> Reason: {reason[:110]}...\n")
