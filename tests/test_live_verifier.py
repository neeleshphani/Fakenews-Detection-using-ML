import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

def extract_subject(claim):
    claim = claim.strip()
    cap_match = re.search(r'capital\s+of\s+([a-zA-Z\s]+?)\s+is\s+([a-zA-Z\s]+)', claim, re.I)
    if cap_match:
        return cap_match.group(1).strip(), 'capital', cap_match.group(2).strip()
    is_match = re.search(r'^(the\s+)?([a-zA-Z\s]+?)\s+(is|are|was|were)\s+(a\s+|an\s+)?([a-zA-Z0-9\s]+)', claim, re.I)
    if is_match:
        return is_match.group(2).strip(), 'is', is_match.group(5).strip()
    return claim, 'general', ''

def verify_against_live_wikipedia(claim):
    subject, rel, predicate = extract_subject(claim)
    
    # 1. Search Wikipedia for subject
    search_q = subject if subject != claim else claim
    results = wikipedia.search(search_q)
    if not results:
        return None, "No Wikipedia article found", "None"
        
    top_title = results[0]
    try:
        summary = wikipedia.summary(top_title, sentences=2, auto_suggest=False)
    except Exception:
        try:
            summary = wikipedia.summary(top_title, sentences=2)
        except Exception:
            return None, "Unable to extract summary", top_title

    summary_lower = summary.lower()
    claim_lower = claim.lower()
    
    # Check 1: Numbers/dates contradiction
    claim_nums = set(re.findall(r'\b\d+\b', claim))
    summ_nums = set(re.findall(r'\b\d+\b', summary))
    if claim_nums and not claim_nums.intersection(summ_nums):
        return False, f"Numerical mismatch: Claim numbers {list(claim_nums)} do not match live Wikipedia records for '{top_title}': \"{summary}\"", top_title
        
    # Check 2: Category contradiction (e.g. continent vs country)
    if 'continent' in claim_lower and 'country' in summary_lower:
        return False, f"Wikipedia verifies '{top_title}' as a country, contradicting the claim that it is a continent: \"{summary}\"", top_title
    if 'country' in claim_lower and 'continent' in summary_lower:
        return False, f"Wikipedia verifies '{top_title}' as a continent, contradicting the claim that it is a country: \"{summary}\"", top_title

    # Check 3: Capital mismatch
    if rel == 'capital':
        if predicate.lower() in summary_lower:
            return True, summary, top_title
        else:
            return False, f"Live Wikipedia records for '{top_title}' do not match claimed capital '{predicate}': \"{summary}\"", top_title

    # Check 4: General keyword support
    pred_words = set(re.findall(r'\b\w{4,}\b', predicate.lower() if predicate else claim_lower))
    summary_words = set(re.findall(r'\b\w{4,}\b', summary_lower))
    if pred_words:
        overlap = pred_words.intersection(summary_words)
        if len(overlap) / len(pred_words) >= 0.4:
            return True, summary, top_title
        else:
            return False, f"Claimed assertion is unsupported by live Wikipedia records for '{top_title}': \"{summary}\"", top_title
            
    return True, summary, top_title

test_claims = [
    'india is a continent',
    'asia is a country',
    'the capital of telangana is andhra pradesh',
    'the capital of france is paris',
    'the british ruled india 31 years',
    'narendra modi is prime minister of india'
]

for c in test_claims:
    is_true, reason, title = verify_against_live_wikipedia(c)
    verdict = "TRUE" if is_true else "FAKE"
    print(f"[{verdict}] {c}")
    print(f" -> Reason: {reason[:120]}...")
    print(f" -> Source: Wikipedia ({title})\n")
