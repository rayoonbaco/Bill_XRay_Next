from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parent
out=ROOT/'artifacts'/'pass43_generalization_trial.json'
subprocess.check_call([sys.executable,'-m','unittest','tests.test_generalization_trial'],cwd=ROOT)
p=json.loads(out.read_text(encoding='utf-8'))
lines=[]
A=lines.append
A('='*72); A(' BILL X-RAY NEXT - PASS 43 SMOKE CAST'); A(' COLD GENERALIZATION TRIAL'); A('='*72); A('')
A('YOUR DUTIES THIS PASS'); A('  1. Read the cold-trial verdict.'); A('  2. Read the column without asking whether you agree with the policy.'); A('  3. Ask whether this sounds like Bill X-Ray understood a DIFFERENT law.'); A('  4. Check that the engine found a different thesis instead of reusing TCJA clocks/doors.'); A('')
A('WHAT THIS PASS MUST PROVE'); A('  - The Next doctrine can consume a different verified law without bill-specific prose code.'); A('  - The editor discovers topic mix before choosing a thesis.'); A('  - The columnist selects rather than dumps the evidence.'); A('  - External CBO/award context remains context, not statutory truth or causal proof.'); A('')
A(f"TRIAL BILL: {p['title']} ({p['bill_id']})")
A(f"VERIFIED FACTS AVAILABLE: {p['available_verified_facts']}")
A(f"TOPICS DISCOVERED: {len(p['topic_counts'])} -> {', '.join(sorted(p['topic_counts']))}")
A(f"FACTS KEPT BY COLUMNIST: {p['selected_fact_count']}")
A(f"COLUMN WORD COUNT: {p['column_word_count']}")
A(f"MACHINE VERDICT: {p['verdict']}")
A(''); A('--------------------- COLD COLUMN ---------------------'); A(p['column']); A('-------------------------------------------------------'); A('')
A('REALITY CONTEXT'); A(f"  CBO lane: {p['reality_context']['cbo_status']}"); A(f"  USAspending lane: {p['reality_context']['usaspending_status']}"); A(f"  Guardrail: {p['reality_context']['guardrail']}"); A('')
A('HUMAN GENERALIZATION GATE'); A('  Did Bill X-Ray find a coherent story in a different law without being told what story to find?'); A('  If yes, the architecture generalizes enough to move toward the public-product inversion.');
text='\n'.join(lines)+'\n'; (ROOT/'artifacts'/'SMOKE_CAST_PASS_43.txt').write_text(text,encoding='utf-8'); print(text)
if p['verdict']!='GENERALIZES': raise SystemExit(2)
