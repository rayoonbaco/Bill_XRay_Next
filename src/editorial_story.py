"""PASS 41 editorial story composer.

Produces an original Bill X-Ray voice from the Pass 41 editorial packet.
The story is intentionally not an imitation of any named author.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

def wc(s): return len(re.findall(r"\b[\w'-]+\b",s))

def build_story(room_path: Path, out_path: Path) -> dict:
    room=json.loads(room_path.read_text(encoding='utf-8'))
    facts={f['fact_id']:f for f in room['selected_facts']}
    moves={m['move_id']:m for m in room['accepted_editorial_moves']}
    used_facts=set(); used_moves=[]; ledger=[]
    paras=[]
    def fact(fid):
        used_facts.add(fid); s=facts[fid]['statement']; ledger.append({'kind':'FACT','text':s,'support_fact_ids':[fid]}); return s
    def move(mid):
        m=moves[mid]; used_moves.append(mid); ledger.append({'kind':m['kind'],'text':m['text'],'support_fact_ids':m['support_fact_ids']}); return m['text']
    def prose(text, supports, kind='SYNTHESIS'):
        ledger.append({'kind':kind,'text':text,'support_fact_ids':supports}); used_facts.update(supports); return text

    paras.append(prose(
      "Congress called it the Tax Cuts and Jobs Act. That title is tidy. The law is not. It reaches into household tax brackets, child credits, deductions, business income, corporate taxes, estates, borrowing, and investments tied to particular neighborhoods. Bill X-Ray's job is not to pick a team. It is to translate the machinery until a citizen can see what moved.",
      ['rates_window','child_credit_amount','qbi_20_percent','corporate_rate','estate_exclusion','oz_definition']))
    paras.append(move('headline_is_not_machine') + " " + move('temporary_permanent'))

    paras.append(
      fact('rates_window') + " " + fact('personal_exemption_zero') + " " + fact('salt_cap') + " " + fact('mortgage_debt_limit')
    )
    paras.append(prose(
      "Put those together and the household side stops looking like a single tax-cut dial. Congress turned several dials at once. A lower rate can matter, but so can losing an exemption, hitting a deduction cap, or borrowing under a different mortgage-interest ceiling. The statute tells us the rules; this pass does not pretend those rules produce the same result for every family.",
      ['rates_window','personal_exemption_zero','salt_cap','mortgage_debt_limit']))

    paras.append(fact('child_credit_amount') + " " + fact('other_dependents') + " " + fact('refundable_cap') + " " + fact('refundable_threshold') + " " + fact('child_ssn'))
    paras.append(move('headline_luggage') + " " + move('child_credit_picture'))

    paras.append(
      fact('qbi_20_percent') + " " + fact('qbi_wage_property_limit') + " " + fact('excess_loss_disallowance')
    )
    paras.append(move('twenty_percent_asterisk') + " " + move('business_two_hands'))
    paras.append(fact('corporate_rate') + " " + fact('bonus_expensing_100') + " " + fact('interest_limit'))
    paras.append(prose(
      "There is a useful contrast here. The corporate-rate rule is easy to state: 21% of taxable income. The pass-through deduction takes a paragraph before we have even reached every limit. One part of the law reads like a road sign; another reads like the directions for assembling the road sign.",
      ['corporate_rate','qbi_20_percent','qbi_wage_property_limit','qbi_phase_in'],'WIT'))

    paras.append(fact('estate_exclusion'))
    paras.append(prose(
      "That change belongs in the story because it shows how far the law ranges. The same legislation that rewrites everyday family-tax rules also changes the amount shielded by the basic estate-and-gift-tax exclusion.",
      ['estate_exclusion','child_credit_amount','salt_cap']))

    paras.append(fact('oz_definition') + " " + fact('oz_nomination') + " " + fact('oz_25_percent') + " " + fact('oz_contiguous'))
    paras.append(move('oz_map_wit') + " " + move('oz_system'))
    paras.append(fact('oz_180_days') + " " + fact('oz_hold_benefits') + " " + fact('oz_ten_year') + " " + fact('oz_fund_90'))
    paras.append(prose(
      "That is why this provision is more revealing than the phrase 'Opportunity Zone tax break.' Congress created eligibility rules for places, assigned government officials roles in choosing them, required qualifying funds to hold mostly qualifying property, and rewarded investors differently depending on timing. The tax rule is also a small governing system.",
      ['oz_definition','oz_nomination','oz_25_percent','oz_contiguous','oz_fund_90','oz_hold_benefits','oz_ten_year']))

    paras.append(prose(
      "So what is the simplest honest story? TCJA is a broad rewrite of tax rules, not one tax cut. It changes the household calculation in several places at once; expands and conditions family credits; creates a new deduction framework for many noncorporate businesses; sets the corporate rate at 21%; changes deductions and limits for businesses; doubles the referenced estate-and-gift exclusion amount; and creates a place-based investment system called Opportunity Zones. Some of the individual provisions in this evidence packet carry an explicit 2018-through-2025 window. The law therefore cannot be understood responsibly from one percentage, one slogan, or one beneficiary.",
      ['rates_window','personal_exemption_zero','salt_cap','child_credit_amount','qbi_20_percent','corporate_rate','interest_limit','estate_exclusion','oz_definition']))
    paras.append(prose(
      "And that may be the most useful thing Bill X-Ray can do. Congress is entitled to write precise law. Citizens are entitled to understand what that precision adds up to. We can keep the legal machinery downstairs with the receipts. Upstairs, the language ought to sound like somebody explaining what happened.",
      ['rates_window','child_credit_amount','corporate_rate','oz_definition'],'SYNTHESIS'))

    story='\n\n'.join(paras)
    payload={
      'schema_version':'41.0','bill_id':'TCJA','title':'I READ THE BILL','dek':'The Tax Cuts and Jobs Act, translated into a human story.',
      'story':story,'word_count':wc(story),'facts_used_count':len(used_facts),'editorial_moves_used_count':len(set(used_moves)),
      'sentence_ledger':ledger,
      'release_readiness':'EDITORIAL_READY_FOR_RAY_GATE',
      'voice':'Original Bill X-Ray editorial voice: plain, curious, skeptical of complexity, restrained with humor, nonpartisan.',
      'guardrail':'No sentence may gain factual meaning from style alone. Editorial moves require listed semantic support.'
    }
    out_path.parent.mkdir(parents=True,exist_ok=True); out_path.write_text(json.dumps(payload,indent=2),encoding='utf-8'); return payload

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--room',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    p=build_story(a.room,a.out); print(f"PASS 41 STORY: {p['word_count']} words; {p['facts_used_count']} facts; {p['editorial_moves_used_count']} editorial moves; readiness={p['release_readiness']}")
if __name__=='__main__': main()
