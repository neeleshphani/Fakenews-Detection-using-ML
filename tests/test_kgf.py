import wikipedia, re

wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')

def check_creative_or_official_role(claim):
    m = re.search(r'(music composer|music director|composer|director|producer|actor|hero|singer|author|writer|ceo|founder|owner|chairman|prime minister|president|chief minister)\s+of\s+([a-zA-Z0-9\s]+?)\s+is\s+([a-zA-Z\s]+)', claim, re.I)
    if not m:
        return None, None, None
        
    role = m.group(1).strip()
    work = m.group(2).strip()
    person = m.group(3).strip()
    
    # 1. Search Wikipedia for the work/entity
    res = wikipedia.search(work)
    if not res:
        return None, None, None
    top_work = res[0]
    
    try:
        p = wikipedia.page(top_work, auto_suggest=False)
        content = p.content
        summary = p.summary
    except Exception:
        return None, None, None
        
    content_lower = content.lower()
    person_lower = person.lower()
    
    true_statement = None
    for line in content.split('\n'):
        line_l = line.lower()
        if any(term in line_l for term in ['composed', 'music by', 'directed by', 'produced by', 'written by', 'score by']):
            if len(line) > 15:
                clean_line = re.sub(r'\[\d+\]', '', line).strip()
                true_statement = clean_line.split('.')[0] + '.'
                break
                
    if person_lower in content_lower and any(r_word in content_lower for r_word in role.lower().split()):
        return 1, f"Live Wikipedia records confirm that '{person.title()}' is the {role} of {top_work}: {true_statement or summary[:150]}", f"Wikipedia Live Web API ({top_work})"
    else:
        if true_statement:
            reason = f"Live Wikipedia records state that: {true_statement} The claim asserting '{person.title()}' as the {role} is incorrect."
        else:
            reason = f"Live Wikipedia records for {top_work} do not credit '{person.title()}' as the {role}. Real information: {summary[:150]}"
        return 0, reason, f"Wikipedia Live Web API ({top_work})"

pred, reason, src = check_creative_or_official_role('the music composer of kgf chapter one is anirudh')
verdict = 'REAL' if pred == 1 else 'FAKE'
print('Verdict:', verdict)
print('Reason:', reason.encode('ascii', 'ignore').decode())
print('Source:', src)
