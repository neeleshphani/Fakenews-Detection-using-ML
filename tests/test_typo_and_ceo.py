import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

query = 'the ceo of jio stduios is phani'

# Word-level typo correction
words = query.split()
corrected_words = []
has_typo = False

for w in words:
    # Check if word is misspelled
    clean_w = re.sub(r'[^\w]', '', w)
    if len(clean_w) >= 4 and clean_w.lower() not in {'about', 'their', 'there', 'which', 'where', 'these', 'those', 'state', 'india', 'russia'}:
        r, s = wikipedia.search(clean_w, suggestion=True)
        if s and s.lower() != clean_w.lower() and len(r) == 0:
            corrected_words.append(s)
            has_typo = True
        else:
            corrected_words.append(w)
    else:
        corrected_words.append(w)

effective_input = ' '.join(corrected_words) if has_typo else query

print('Original Query:', query)
print('Has Typo?', has_typo)
print('Effective Input:', effective_input)

# Check CEO / Leadership
ceo_match = re.search(r'(ceo|chief executive officer|founder|owner|director|chairman|head|prime minister|president|chief minister)\s+of\s+([a-zA-Z\s]+?)\s+is\s+([a-zA-Z\s]+)', effective_input, re.I)
if ceo_match:
    role = ceo_match.group(1).strip()
    org = ceo_match.group(2).strip()
    person = ceo_match.group(3).strip()
    
    res_org = wikipedia.search(org)
    if res_org:
        top_org = res_org[0]
        try:
            summ = wikipedia.summary(top_org, sentences=2, auto_suggest=False)
        except Exception:
            summ = wikipedia.summary(top_org, sentences=2)
            
        if person.lower() in summ.lower():
            verdict = 'REAL'
            real_info = f"Live Wikipedia records confirm that '{person.title()}' is associated with {top_org}: {summ}"
        else:
            verdict = 'FAKE'
            real_info = f"Live Wikipedia records state that '{person.title()}' is not the {role} of {top_org}. True records for {top_org}: \"{summ}\""
            
        source = f"Wikipedia Live Web API ({top_org})"
        print('Verdict:', verdict)
        print('Real Info:', real_info)
        print('Source:', source)
