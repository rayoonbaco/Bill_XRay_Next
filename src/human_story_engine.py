"""Human Story Engine for Bill X-Ray Next.

PASS 40 proved the writer can refuse to bluff when its evidence packet is thin.
PASS 40.1 adds a broader direct-statutory semantic packet. The writer still may
use only court-cleared facts and explicitly labeled unresolved questions.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path


def _clean_statement(s: str) -> str:
    s=s.replace('Credit amount','the child tax credit')
    s=s.replace('Increase in basic exclusion amount','the basic estate and gift tax exclusion amount')
    return s


def _words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b",text))


def _legacy_story(court: dict) -> tuple[str,list[str],list[str]]:
    supported=[o for o in court.get('opinions',[]) if o.get('allowed_public_statement')]
    questions=[o for o in court.get('opinions',[]) if o.get('verdict')=='QUESTION_ONLY' and o.get('allowed_public_question')]
    facts=[_clean_statement(o['allowed_public_statement']) for o in supported]
    paras=["Congress wrote a very large tax law. Bill X-Ray is trying something harder than shortening it: reconstruct what changed, prove each statement, and only then explain it in ordinary language."]
    if facts: paras.append(f"So far, the evidence court lets us say {len(facts)} things plainly. " + " ".join(facts))
    paras.append("That is not yet the story of the Tax Cuts and Jobs Act. It is the part of the story we have earned the right to tell without pretending that a legal phrase explains its own consequence.")
    qs=[q['allowed_public_question'] for q in questions[:4]]
    if qs:
        paras.append("The more interesting questions are still under examination: " + "; ".join(qs) + ". Those are questions, not conclusions.")
    return "\n\n".join(paras), facts, qs


def _fact_map(coverage: dict) -> dict[str,dict]:
    return {f['fact_id']:f for f in coverage.get('facts',[])}


def _join_statements(fm: dict, ids: list[str]) -> str:
    return " ".join(fm[i]['statement'] for i in ids if i in fm)


def _expanded_story(court: dict, coverage: dict) -> tuple[str,list[str],list[str]]:
    fm=_fact_map(coverage)
    used=[]
    def lane(ids):
        used.extend([i for i in ids if i in fm]); return _join_statements(fm,ids)

    paras=[]
    paras.append(
        "The Tax Cuts and Jobs Act is not one tax change hiding inside a giant document. It changes the rules for individual rates, families, business owners, corporations, estates, borrowing, and investment in selected communities. Once the legal instructions are reconstructed, the shape of the law starts to look much more ordinary: Congress changed a lot of tax levers at the same time, and many of those levers do not move in the same direction or last for the same amount of time."
    )
    paras.append(lane(['rates_window','personal_exemption_zero','salt_cap','mortgage_debt_limit']))
    paras.append(
        "That is why saying simply that the bill 'cut taxes' does not describe the machinery very well. The rate table is only one piece. The same law also changes deductions and limits, so the result for a particular household depends on which of those rules actually touch that household. Bill X-Ray is not yet claiming who won or lost overall; that requires more than reading a rate table."
    )
    paras.append(lane(['child_credit_amount','child_credit_phaseout','other_dependents','refundable_cap','refundable_threshold','child_ssn']))
    paras.append(
        "The family section is a good example of why the original congressional language is so easy to misunderstand. A headline can say '$2,000 child credit,' while the statute immediately surrounds that number with phaseout thresholds, a separate credit for other dependents, a cap on the refundable portion, an earned-income threshold, and an identification requirement. Those are not footnotes to the meaning. They are part of the meaning."
    )
    paras.append(lane(['qbi_20_percent','qbi_wage_property_limit','qbi_phase_in','excess_loss_disallowance','excess_loss_threshold','loss_carryover']))
    paras.append(lane(['corporate_rate','bonus_expensing_100','interest_limit','interest_carryforward','estate_exclusion']))
    paras.append(
        "The business side therefore has two very different kinds of changes living beside each other. Some rules create or accelerate deductions. Others limit when losses or interest can be deducted. And the corporate rate is stated directly at 21%. Reading only one of those provisions would give a badly incomplete picture of what Congress actually changed."
    )
    paras.append(lane(['oz_definition','oz_nomination','oz_25_percent','oz_contiguous','oz_duration','oz_180_days','oz_deferral_end','oz_hold_benefits','oz_ten_year','oz_fund_90']))
    paras.append(
        "Opportunity Zones are especially revealing because the provision is not merely a tax percentage. Congress created a map-making process, gave state and federal officials defined roles in selecting places, set limits on which tracts can qualify, and then attached capital-gain timing rules to investments routed through qualifying funds. That is a policy system hiding inside tax-code language."
    )

    questions=[]; seen=set()
    for o in court.get('opinions',[]):
        q=o.get('allowed_public_question')
        if o.get('verdict')=='QUESTION_ONLY' and q and o.get('category') not in seen:
            questions.append(q); seen.add(o.get('category'))
        if len(questions)>=3: break
    if questions:
        paras.append("There are still things Bill X-Ray will not pretend to know. " + " ".join("One open question is: " + q for q in questions))
    paras.append(
        "This is finally enough material to tell a real first story about the law, but it is not yet the finished editorial. The next step is not to add confidence or jokes. It is to let the editorial team decide which of these proved facts actually define the law, which are merely technical, which contradictions or oddities deserve attention, and where humor clarifies rather than distracts. The evidence has finally become broad enough that the writer can choose."
    )
    facts=[fm[i]['statement'] for i in used]
    return "\n\n".join(p for p in paras if p.strip()),facts,questions


def build_story(court_path: Path, out_path: Path, coverage_path: Path|None=None) -> dict:
    court=json.loads(court_path.read_text(encoding='utf-8'))
    coverage=json.loads(coverage_path.read_text(encoding='utf-8')) if coverage_path else None
    if coverage and coverage.get('fact_count',0)>=20:
        story,facts,questions=_expanded_story(court,coverage)
        version='40.1'; readiness='STORY_READY_FOR_HUMAN_GATE'
        diagnosis='Semantic coverage is broad enough for a real explanatory TCJA draft. Editorial selection and voice are now the bottleneck.'
    else:
        story,facts,questions=_legacy_story(court)
        version='40.0'; readiness='NOT_FINAL_EDITORIAL'
        diagnosis='Truth Court is working, but the current evidence packet is too thin for a genuinely explanatory TCJA essay.'
    payload={
      'schema_version':version,'bill_id':court.get('bill_id','TCJA'),'title':'I READ THE BILL',
      'dek':'Here is what the law actually changes, in human language.', 'story':story,
      'word_count':_words(story),'supported_fact_count':len(facts),'question_count_used':len(questions),
      'source_opinion_count':court.get('opinion_count',0),'doctrine':'court_cleared_human_story_only',
      'guardrail':'The story may connect and simplify court-cleared facts and label unresolved questions. It may not invent motive, consequences, beneficiaries, distributional effects, corruption, or humor.',
      'release_readiness':readiness,'diagnosis':diagnosis,'facts_used':facts,
    }
    out_path.parent.mkdir(parents=True,exist_ok=True); out_path.write_text(json.dumps(payload,indent=2),encoding='utf-8'); return payload


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--court',type=Path,required=True); ap.add_argument('--coverage',type=Path); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    p=build_story(a.court,a.out,a.coverage)
    print(f"PASS {p['schema_version']}: wrote {p['word_count']} words from {p['supported_fact_count']} court-cleared facts; readiness={p['release_readiness']}")
    return 0
if __name__=='__main__': raise SystemExit(main())
