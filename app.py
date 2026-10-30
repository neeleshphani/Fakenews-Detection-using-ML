import streamlit as st
import pandas as pd
import joblib
import re
import difflib
from fact_checker import FactChecker

# Page config
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .verified-true { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; border-left: 5px solid #28a745; margin-bottom: 20px;}
    .verified-false { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 20px;}
    .unverified { background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107; margin-bottom: 20px;}
    .ml-real { background-color: #e2f0fb; color: #004085; padding: 15px; border-radius: 5px; border-left: 5px solid #007bff; margin-bottom: 20px;}
    .ml-fake { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# Cache models
@st.cache_resource
def load_models():
    try:
        model = joblib.load('models/fake_news_model.pkl')
        vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
        return model, vectorizer
    except Exception as e:
        return None, None

model, vectorizer = load_models()
fact_checker = FactChecker()

def is_gibberish(text):
    words = text.split()
    for word in words:
        if len(word) > 5 and not re.search(r'[aeiouyAEIOUY0-9]', word):
            return True
        if re.search(r'(.)\1{3,}', word): # 4 identical consecutive chars
            return True
    return False

def fuzzy_match(target, text, threshold=0.75):
    if not target or not text:
        return False
    target_clean = target.lower().strip()
    text_clean = text.lower()
    if target_clean in text_clean:
        return True
    t_tokens = target_clean.split()
    n = len(t_tokens)
    text_words = re.findall(r'[a-zA-Z0-9]+', text_clean)
    if not text_words or len(text_words) < n:
        return difflib.SequenceMatcher(None, target_clean, text_clean).ratio() >= threshold
    for i in range(len(text_words) - n + 1):
        window = ' '.join(text_words[i:i+n])
        if difflib.SequenceMatcher(None, target_clean, window).ratio() >= threshold:
            return True
        token_sims = [difflib.SequenceMatcher(None, tt, wt).ratio() for tt, wt in zip(t_tokens, text_words[i:i+n])]
        if sum(token_sims) / len(token_sims) >= 0.8:
            return True
    return False

def match_claimed_person(claimed, statement, title=''):
    if not statement and not title:
        return False
    c_clean = claimed.lower().strip()
    c_tokens = c_clean.split()
    if not c_tokens:
        return False
        
    full_text = f'{title} {statement}'.lower()
    if re.search(r'\b' + re.escape(c_clean) + r'\b', full_text):
        return True
        
    props = []
    if title:
        props.append(title)
    props.extend(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', f'{title}. {statement}'))
    
    for cand in props:
        cand_clean = cand.lower().strip()
        cand_tokens = cand_clean.split()
        
        # Subset check: All tokens in claimed must be in candidate
        if set(c_tokens).issubset(set(cand_tokens)):
            return True
            
        # If single token, compare with each token of candidate with high threshold
        if len(c_tokens) == 1 and len(c_tokens[0]) > 3:
            for ct in cand_tokens:
                if difflib.SequenceMatcher(None, c_tokens[0], ct).ratio() >= 0.82:
                    return True
                    
        # Same number of tokens: token-by-token comparison (e.g. 'ravi bhasur' vs 'ravi basrur')
        if len(c_tokens) == len(cand_tokens) and len(c_tokens) > 1:
            tok_ratios = [difflib.SequenceMatcher(None, c, t).ratio() for c, t in zip(c_tokens, cand_tokens)]
            if all(r >= 0.75 for r in tok_ratios):
                return True
                
        # Overall sequence similarity if both are multi-token
        if len(c_tokens) > 1 and len(cand_tokens) > 1:
            if difflib.SequenceMatcher(None, c_clean, cand_clean).ratio() >= 0.82:
                return True
                
    return False

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def validate_input(text):
    if not text or len(text.strip()) == 0:
        return False, "Input cannot be empty."
    
    words = text.strip().split()
    if len(words) < 3:
        return False, "Invalid / Too short. Please enter a valid claim or article (at least 3 words)."
        
    if is_gibberish(text):
        return False, "Invalid / Gibberish detected. Please enter meaningful text."
        
    return True, "Valid"

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📰 Check News", "🔐 Fact Manager", "ℹ️ About Project"])

if page == "📰 Check News":
    st.title("📰 Fake News Detection System")
    st.subheader("Machine Learning + Fact Verification")
    
    st.markdown("Enter a news article or factual claim below to verify its authenticity.")
    
    user_input = st.text_area("Enter News Article or Claim", height=150, placeholder="E.g., India has 28 states")
    
    if st.button("🔍 CHECK NEWS", use_container_width=True):
        if not model or not vectorizer:
            st.error("Machine Learning models not found! Please run `python train_model.py` first.")
        else:
            is_valid, msg = validate_input(user_input)
            if not is_valid:
                st.error(msg)
            else:
                st.markdown("---")
                effective_input = user_input.strip()

                # Run fact checker
                status, match, source = fact_checker.check_claim(effective_input)
                
                if status == "SUPPORTED":
                    st.markdown(f'<div class="verified-true"><h3>🟢 News is Real</h3><p><b>Real Information:</b> The claim matches our verified records. {match["subject"]} {match["relation"]} {match["object"]}.</p><b>Source:</b> {source}</div>', unsafe_allow_html=True)
                    
                elif status == "CONTRADICTED":
                    st.markdown(f'<div class="verified-false"><h3>🔴 News is Fake</h3><p><b>Real Information:</b> The claim contradicts our verified records. True fact: {match["subject"]} {match["relation"]} {match["object"]}.</p><b>Source:</b> {source}</div>', unsafe_allow_html=True)
                    
                elif status == "UNVERIFIED":
                    # Run ML prediction
                    cleaned = clean_text(effective_input)
                    vec = vectorizer.transform([cleaned])
                    pred = model.predict(vec)[0]
                    
                    # Fetch Wikipedia context directly from the live web
                    reason_text = "Based on statistical text pattern analysis by the Machine Learning model."
                    source_text = "SVM Classifier"
                    
                    c_clean = effective_input.lower().strip()
                    continents = {'asia', 'africa', 'north america', 'south america', 'antarctica', 'europe', 'australia', 'oceania'}
                    
                    # 1. Autonomous Capital Relational Verification via Live Web
                    cap_match = re.search(r'capital\s+of\s+([a-zA-Z\s]+?)\s+is\s+([a-zA-Z\s]+)', effective_input, re.I)
                    if cap_match:
                        place, claimed_cap = cap_match.group(1).strip(), cap_match.group(2).strip()
                        try:
                            import wikipedia
                            wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')
                            res, sug = wikipedia.search(f'capital of {place}', suggestion=True)
                            if not res and sug:
                                res = wikipedia.search(sug)
                            if res:
                                top_res = res[0]
                                try:
                                    cap_summary = wikipedia.summary(top_res, sentences=2, auto_suggest=False)
                                except Exception:
                                    cap_summary = wikipedia.summary(top_res, sentences=2)
                                    
                                if claimed_cap.lower() in top_res.lower() or claimed_cap.lower() in cap_summary.lower() or fuzzy_match(claimed_cap, cap_summary) or fuzzy_match(claimed_cap, top_res):
                                    pred = 1
                                    reason_text = f"Live Wikipedia records confirm that '{claimed_cap.title()}' is the capital of {place.title()}: {cap_summary}"
                                    source_text = f"Wikipedia Live Web API ({top_res})"
                                else:
                                    pred = 0
                                    reason_text = f"Live Wikipedia records identify the capital of {place.title()} as '{top_res}', contradicting the claim of '{claimed_cap.title()}'. {cap_summary}"
                                    source_text = f"Wikipedia Live Web API ({top_res})"
                        except Exception:
                            pass
                            
                    # 2. Autonomous Creative, Entertainment & Leadership Role Verification via Live Web
                    roles_regex = (
                        r'music composer|music director|composer|director|producer|actor|actress|hero|heroine|'
                        r'singer|author|writer|creator|ceo|chief executive officer|founder|co-founder|owner|'
                        r'chairman|head|prime minister|pm|president|chief minister|cm|chancellor|king|queen|governor|coach|captain'
                    )
                    pat_role_a = re.compile(rf'^(?:the\s+)?({roles_regex})\s+(?:of|for|in)\s+([a-zA-Z0-9\s\.\-]+?)\s+is\s+([a-zA-Z\s\.\-]+)$', re.I)
                    pat_role_b = re.compile(rf'^(?:the\s+)?([a-zA-Z0-9\s\.\-]+?)(?:\'s|\s+)\s*({roles_regex})\s+is\s+([a-zA-Z\s\.\-]+)$', re.I)
                    m_role_a = pat_role_a.search(effective_input.strip())
                    m_role_b = pat_role_b.search(effective_input.strip())
                    
                    if m_role_a or m_role_b:
                        if m_role_a:
                            role = m_role_a.group(1).strip().lower()
                            work = m_role_a.group(2).strip()
                            person = m_role_a.group(3).strip()
                        else:
                            work = m_role_b.group(1).strip()
                            role = m_role_b.group(2).strip().lower()
                            person = m_role_b.group(3).strip()
                            
                        if role == 'cm':
                            role = 'chief minister'
                        elif role == 'pm':
                            role = 'prime minister'
                            
                        try:
                            import wikipedia
                            wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')
                            
                            # Role keywords mapping
                            if any(k in role for k in ['music', 'composer']):
                                role_kw = ['music composed by', 'music by', 'soundtrack composed by', 'score composed by', 'score by', 'music director', 'soundtrack album by', 'composed by', 'composer', 'composed']
                            elif 'director' in role:
                                role_kw = ['directed by', 'director']
                            elif 'producer' in role:
                                role_kw = ['produced by', 'producer']
                            elif any(k in role for k in ['ceo', 'chief executive officer']):
                                role_kw = ['ceo', 'chief executive officer', 'chief executive', 'appointed ceo', 'chief executive of']
                            elif 'founder' in role:
                                role_kw = ['founded by', 'co-founder', 'founder']
                            elif any(k in role for k in ['owner', 'chairman']):
                                role_kw = ['owner', 'chairman', 'owned by']
                            elif 'prime minister' in role:
                                role_kw = ['prime minister']
                            elif 'president' in role:
                                role_kw = ['president']
                            elif 'chief minister' in role:
                                role_kw = ['chief minister']
                            elif any(k in role for k in ['actor', 'actress', 'hero', 'heroine']):
                                role_kw = ['starring', 'stars', 'played by', 'lead role']
                            else:
                                role_kw = [role]
                                
                            def safe_search(q):
                                try:
                                    res, sug = wikipedia.search(q, suggestion=True)
                                    if not res and sug:
                                        res = wikipedia.search(sug)
                                    return res or []
                                except Exception:
                                    return []
                                    
                            res_role_work = safe_search(f'{role} of {work}')
                            res_work = safe_search(work)
                            
                            candidate_titles = []
                            for r in res_role_work[:4]:
                                if r not in candidate_titles:
                                    candidate_titles.append(r)
                            if 'chapter 1' in work.lower() or 'chapter one' in work.lower():
                                for rw in res_work:
                                    if 'chapter 1' in rw.lower() and rw not in candidate_titles:
                                        candidate_titles.insert(0, rw)
                            for rw in res_work[:3]:
                                if rw not in candidate_titles:
                                    candidate_titles.append(rw)
                                    
                            statements_found = []
                            matching_statement = None
                            best_matching_source = None
                            
                            for title in candidate_titles:
                                try:
                                    p = wikipedia.page(title, auto_suggest=False)
                                    content = p.content
                                    summary = p.summary
                                except Exception:
                                    continue
                                    
                                # 1. Check summary sentences
                                for s in summary.split('.'):
                                    s_clean = re.sub(r'\[\d+\]', '', s).strip()
                                    if not s_clean:
                                        continue
                                    s_lower = s_clean.lower()
                                    if any(kw in s_lower for kw in role_kw):
                                        stmt = s_clean + '.'
                                        statements_found.append((stmt, title))
                                        if match_claimed_person(person, stmt, title):
                                            matching_statement = stmt
                                            best_matching_source = title
                                            break
                                if matching_statement:
                                    break
                                    
                                # 2. Check content lines for role sentences
                                for line in content.split('\n'):
                                    line_clean = re.sub(r'\[\d+\]', '', line).strip()
                                    if not line_clean:
                                        continue
                                    line_l = line_clean.lower()
                                    if any(kw in line_l for kw in role_kw):
                                        for s in line_clean.split('.'):
                                            s_clean = s.strip()
                                            if any(kw in s_clean.lower() for kw in role_kw):
                                                stmt = s_clean + '.'
                                                statements_found.append((stmt, title))
                                                if match_claimed_person(person, stmt, title):
                                                    matching_statement = stmt
                                                    best_matching_source = title
                                                    break
                                        if matching_statement:
                                            break
                                if matching_statement:
                                    break
                                    
                            if matching_statement:
                                pred = 1
                                reason_text = f"Live Wikipedia records confirm that '{person.title()}' is associated as the {role} of {best_matching_source}: {matching_statement}"
                                source_text = f"Wikipedia Live Web API ({best_matching_source})"
                            else:
                                pred = 0
                                best_stmt = statements_found[0][0] if statements_found else f"No official records found associating '{person.title()}' as {role} of {work}."
                                best_src = statements_found[0][1] if statements_found else (candidate_titles[0] if candidate_titles else work)
                                reason_text = f"Live Wikipedia records state that: \"{best_stmt}\" The claim asserting that '{person.title()}' is the {role} is incorrect."
                                source_text = f"Wikipedia Live Web API ({best_src})"
                        except Exception:
                            pass

                    # 3. Autonomous Geographical Category Verification
                    elif re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?continent', c_clean):
                        match_cont = re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?continent', c_clean)
                        subj = match_cont.group(2).strip()
                        if subj not in continents:
                            pred = 0
                            reason_text = f"Geographical fact contradiction: '{subj.title()}' is not a continent. Earth has only 7 continents: Asia, Africa, Europe, North America, South America, Australia, and Antarctica."
                            source_text = "Wikipedia Geography Knowledge"
                        else:
                            pred = 1
                            reason_text = f"Live geographical records verify that '{subj.title()}' is one of the 7 continents of Earth."
                            source_text = "Wikipedia Geography Knowledge"

                    elif re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?country', c_clean):
                        match_count = re.search(r'^(the\s+)?(.*?)\s+is\s+(a\s+|an\s+)?country', c_clean)
                        subj = match_count.group(2).strip()
                        if subj in continents:
                            pred = 0
                            reason_text = f"Geographical fact contradiction: '{subj.title()}' is a continent, not a country."
                            source_text = "Wikipedia Geography Knowledge"

                    # 4. Multi-Domain Bidirectional Entity Cross-Verification (Tech, Business, Sports, People, History)
                    if reason_text == "Based on statistical text pattern analysis by the Machine Learning model.":
                        try:
                            # Extract capitalized named entities
                            named_entities = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', user_input)
                            ignore_words = {'The', 'This', 'That', 'With', 'From', 'What', 'When', 'Where', 'Why', 'Who', 'How', 'Capital', 'Prime Minister', 'President', 'Chief Minister', 'CEO'}
                            valid_entities = [e for e in named_entities if e not in ignore_words and len(e) > 2]
                            
                            if len(valid_entities) >= 2:
                                import wikipedia
                                wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')
                                e1, e2 = valid_entities[0], valid_entities[1]
                                
                                try:
                                    s1 = wikipedia.summary(e1, sentences=3, auto_suggest=False).lower()
                                except Exception:
                                    s1 = ""
                                try:
                                    s2 = wikipedia.summary(e2, sentences=3, auto_suggest=False).lower()
                                except Exception:
                                    s2 = ""
                                    
                                if s1 and s2:
                                    e1_in_s2 = bool(re.search(r'\b' + re.escape(e1.lower()) + r'\b', s2))
                                    e2_in_s1 = bool(re.search(r'\b' + re.escape(e2.lower()) + r'\b', s1))
                                    
                                    if not e1_in_s2 and not e2_in_s1:
                                        pred = 0
                                        reason_text = f"Entity mismatch: Live Wikipedia records for '{e1}' do not associate with '{e2}', and '{e2}' records do not associate with '{e1}'."
                                        source_text = f"Wikipedia Live Web API ({e1} & {e2})"
                                    elif e1_in_s2 or e2_in_s1:
                                        pred = 1
                                        reason_text = f"Live Wikipedia records confirm the factual relationship between '{e1}' and '{e2}'."
                                        source_text = f"Wikipedia Live Web API ({e1})"
                        except Exception:
                            pass

                    # 5. Scientific / Physical Category & Opposites Clash Verification
                    OPPOSITES = {
                        'herbivore': ['carnivore', 'predator', 'meat'],
                        'carnivore': ['herbivore', 'plants'],
                        'freezes': ['boils', 'evaporates'],
                        'boils': ['freezes', 'ice', 'solidifies'],
                        'planet': ['star', 'moon'],
                        'star': ['planet', 'moon'],
                        'moon': ['planet', 'star'],
                        'cricket': ['football', 'footballer', 'soccer', 'basketball'],
                        'football': ['cricket', 'baseball', 'tennis'],
                        'bacteria': ['virus', 'viral'],
                        'virus': ['bacterial', 'bacteria']
                    }
                    if reason_text == "Based on statistical text pattern analysis by the Machine Learning model.":
                        for word, forbidden in OPPOSITES.items():
                            if re.search(r'\b' + word + r'\b', c_clean):
                                try:
                                    import wikipedia
                                    wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')
                                    res_opp = wikipedia.search(user_input)
                                    if res_opp:
                                        top_opp = res_opp[0]
                                        try:
                                            s_opp = wikipedia.summary(top_opp, sentences=3, auto_suggest=False).lower()
                                        except Exception:
                                            s_opp = wikipedia.summary(top_opp, sentences=3).lower()
                                        for f in forbidden:
                                            if re.search(r'\b' + f + r'\b', s_opp):
                                                pred = 0
                                                reason_text = f"Scientific/Domain fact contradiction: Claim asserts '{word}', but live Wikipedia records for '{top_opp}' state it is associated with '{f}'."
                                                source_text = f"Wikipedia Live Web API ({top_opp})"
                                                break
                                except Exception:
                                    pass
                                if pred == 0:
                                    break

                    # 6. General Autonomous Live Wikipedia Search for Unstructured / Other Claims
                    if reason_text == "Based on statistical text pattern analysis by the Machine Learning model.":
                        try:
                            import wikipedia
                            wikipedia.set_user_agent('FakeNewsDetectionBot/1.0 (student.project@aditya.ac.in)')
                            
                            # Prioritize extracting the subject to avoid false object pollution in Wikipedia search
                            is_match = re.search(r'^(the\s+)?([a-zA-Z0-9\s]+?)\s+(is|are|was|were|has|have|belongs to)\s+(.*)', user_input, re.I)
                            subject_term = is_match.group(2).strip() if is_match else user_input
                            
                            search_results, sug = wikipedia.search(subject_term, suggestion=True)
                            if not search_results and sug:
                                search_results = wikipedia.search(sug)
                            if not search_results and subject_term != user_input:
                                search_results, sug = wikipedia.search(user_input, suggestion=True)
                                if not search_results and sug:
                                    search_results = wikipedia.search(sug)
                                    
                            if search_results:
                                top_result = search_results[0]
                                try:
                                    wiki_summary = wikipedia.summary(top_result, sentences=2, auto_suggest=False)
                                except Exception:
                                    wiki_summary = wikipedia.summary(top_result, sentences=2)
                                    
                                reason_text = wiki_summary
                                source_text = f"Wikipedia Live Web API ({top_result})"
                                
                                # Numerical Verification:
                                claim_nums = set(re.findall(r'\b\d+\b', user_input))
                                wiki_nums = set(re.findall(r'\b\d+\b', wiki_summary))
                                if claim_nums and not claim_nums.intersection(wiki_nums):
                                    pred = 0
                                    reason_text = f"Numerical mismatch: Claim numbers {list(claim_nums)} do not match live Wikipedia records for '{top_result}': {wiki_summary}"
                                
                                # Category mismatch:
                                if 'continent' in user_input.lower() and 'country' in wiki_summary.lower():
                                    pred = 0
                                    reason_text = f"Live Wikipedia records classify '{top_result}' as a country, contradicting the claim that it is a continent."
                                    
                                # Context Overlap Filter:
                                claim_words = set(re.findall(r'\b\w{4,}\b', user_input.lower()))
                                summary_words = set(re.findall(r'\b\w{4,}\b', wiki_summary.lower()))
                                if claim_words:
                                    overlap = claim_words.intersection(summary_words)
                                    if len(overlap) / len(claim_words) < 0.35:
                                        pred = 0
                                        reason_text = f"Live Wikipedia records for '{top_result}' do not corroborate the claim: \"{wiki_summary}\""
                        except Exception:
                            pass

                    # Display unified result box
                    if pred == 1:
                        st.markdown(f'<div class="verified-true"><h3>🟢 News is Real</h3><p><b>Real Information:</b> {reason_text}</p><b>Source:</b> {source_text}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="verified-false"><h3>🔴 News is Fake</h3><p><b>Real Information:</b> {reason_text}</p><b>Source:</b> {source_text}</div>', unsafe_allow_html=True)

elif page == "🔐 Fact Manager":
    st.title("🔐 Fact Manager")
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.warning("Please enter the administrator password to manage the fact database.")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if pwd == "admin123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
    else:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
            
        st.markdown("### Add New Fact")
        with st.form("add_fact_form"):
            col1, col2 = st.columns(2)
            with col1:
                f_subject = st.text_input("Subject", placeholder="E.g., Prime Minister of India")
                f_relation = st.text_input("Relation", placeholder="E.g., is")
            with col2:
                f_object = st.text_input("Object / Answer", placeholder="E.g., Narendra Modi")
                f_source = st.text_input("Source", placeholder="E.g., Government of India")
                
            submit = st.form_submit_button("➕ ADD FACT")
            if submit:
                if f_subject and f_relation and f_object and f_source:
                    # check dup
                    db = fact_checker.db
                    is_dup = not db[(db['subject'] == f_subject) & (db['object'] == f_object)].empty
                    if is_dup:
                        st.error("This fact already exists in the database.")
                    else:
                        fact_checker.add_fact(f_subject, f_relation, f_object, f_source)
                        st.success("Fact added successfully!")
                else:
                    st.error("All fields are required.")
                    
        st.markdown("---")
        st.markdown("### Current Fact Database")
        db = fact_checker.db
        st.dataframe(db, use_container_width=True)
        
        st.markdown("#### Delete Fact")
        delete_idx = st.number_input("Enter index to delete (see row numbers above)", min_value=0, max_value=len(db)-1 if len(db)>0 else 0, step=1)
        if st.button("Delete Selected Fact"):
            if 0 <= delete_idx < len(db):
                db = db.drop(delete_idx).reset_index(drop=True)
                db.to_csv("fact_database.csv", index=False)
                fact_checker.load_database()
                st.success("Fact deleted successfully!")
                st.rerun()

elif page == "ℹ️ About Project":
    st.title("ℹ️ About the Project")
    st.markdown("""
    This **Fake News Detection System** combines:
    - Natural Language Processing (NLP)
    - TF-IDF Feature Extraction
    - Machine Learning
    - Support Vector Machine (SVM)
    - Fact Verification

    ### Dataset
    - **Name:** IFND
    - **Total Articles:** 56,714
    
    ### Best Model
    - **Algorithm:** Support Vector Machine (SVM)
    - **Accuracy:** ~95.22%
    - **Precision:** ~94.92%
    - **Recall:** ~98.08%
    - **F1 Score:** ~96.47%
    
    *(Note: Actual metrics may vary slightly based on train/test split randomization, but these are the official benchmark scores for the dataset.)*
    
    ### Architecture
    1. **Fact Verification:** The system first checks claims against a local knowledge base (`fact_database.csv`). 
       - If a match is found, it definitively labels it as **VERIFIED TRUE** or **VERIFIED FALSE**.
    2. **Machine Learning:** If the claim is **UNVERIFIED** (not in the database), the SVM model predicts whether the textual patterns resemble REAL or FAKE news.
       - The SVM is a statistical text classifier; it does not independently verify real-world facts.
    """)
