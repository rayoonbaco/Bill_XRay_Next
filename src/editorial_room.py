"""PASS 41 - Editorial Intelligence Room.

Transforms the broad, court-cleared semantic substrate into a smaller editorial
packet. Style is allowed only after support is attached. Every editorial move
has a provenance class and supporting fact ids.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

FACT_LANES = {
    'opening_shape': ['rates_window','personal_exemption_zero','salt_cap','mortgage_debt_limit'],
    'families': ['child_credit_amount','child_credit_phaseout','other_dependents','refundable_cap','refundable_threshold','child_ssn'],
    'business': ['qbi_20_percent','qbi_wage_property_limit','qbi_phase_in','excess_loss_disallowance','corporate_rate','bonus_expensing_100','interest_limit','estate_exclusion'],
    'opportunity_zones': ['oz_definition','oz_nomination','oz_25_percent','oz_contiguous','oz_180_days','oz_deferral_end','oz_hold_benefits','oz_ten_year','oz_fund_90'],
}

MOVES = [
  {
    'move_id':'headline_is_not_machine','kind':'SYNTHESIS',
    'support_fact_ids':['rates_window','personal_exemption_zero','salt_cap','mortgage_debt_limit'],
    'text':'The law changes rates, deductions, exemptions, and limits at the same time, so no single headline number describes what it does to every household.'
  },
  {
    'move_id':'headline_luggage','kind':'WIT',
    'support_fact_ids':['child_credit_amount','child_credit_phaseout','refundable_cap','refundable_threshold','child_ssn'],
    'text':'In tax law, a headline number rarely travels alone; it arrives with luggage.'
  },
  {
    'move_id':'child_credit_picture','kind':'ANALOGY',
    'support_fact_ids':['child_credit_amount','child_credit_phaseout','other_dependents','refundable_cap','refundable_threshold','child_ssn'],
    'text':'The $2,000 child-credit headline is the sign over the door. The thresholds, refundability rules, dependent rules, and identification requirement are the rooms inside the building.'
  },
  {
    'move_id':'business_two_hands','kind':'SYNTHESIS',
    'support_fact_ids':['qbi_20_percent','excess_loss_disallowance','corporate_rate','bonus_expensing_100','interest_limit'],
    'text':'On the business side, Congress uses both hands: one creates or accelerates deductions, while the other limits when some losses and interest can be deducted.'
  },
  {
    'move_id':'twenty_percent_asterisk','kind':'WIT',
    'support_fact_ids':['qbi_20_percent','qbi_wage_property_limit','qbi_phase_in'],
    'text':'The phrase “20% deduction” is wonderfully short. Congress needed considerably more machinery to decide when that sentence is actually true.'
  },
  {
    'move_id':'oz_system','kind':'SYNTHESIS',
    'support_fact_ids':['oz_definition','oz_nomination','oz_25_percent','oz_contiguous','oz_180_days','oz_hold_benefits','oz_ten_year','oz_fund_90'],
    'text':'Opportunity Zones are not merely a tax percentage attached to a map; the law builds a place-selection system and then ties investment timing and tax treatment to it.'
  },
  {
    'move_id':'oz_map_wit','kind':'WIT',
    'support_fact_ids':['oz_nomination','oz_25_percent','oz_contiguous'],
    'text':'Congress did not draw the map itself. It wrote rules for who gets to hold the pencil.'
  },
  {
    'move_id':'temporary_permanent','kind':'SYNTHESIS',
    'support_fact_ids':['rates_window','personal_exemption_zero','salt_cap','child_credit_amount','corporate_rate'],
    'text':'A central feature of the law is timing: many individual provisions in this packet are explicitly temporary through 2025, while the corporate-rate provision is stated without that same temporary window in the cited section.'
  },
]

BAN_WORDS = ('corrupt','bribe','scam','fraud','steal','theft','pork')

def build_room(coverage_path: Path, out_path: Path) -> dict:
    cov=json.loads(coverage_path.read_text(encoding='utf-8'))
    facts={f['fact_id']:f for f in cov.get('facts',[])}
    selected=[]
    for lane, ids in FACT_LANES.items():
        for fid in ids:
            if fid in facts:
                selected.append({'lane':lane, **facts[fid]})
    accepted=[]; rejected=[]
    for m in MOVES:
        missing=[fid for fid in m['support_fact_ids'] if fid not in facts]
        dangerous=any(w in m['text'].lower() for w in BAN_WORDS)
        item={**m,'missing_support':missing,'accepted':not missing and not dangerous}
        (accepted if item['accepted'] else rejected).append(item)
    packet={
      'schema_version':'41.0','bill_id':'TCJA','selected_fact_count':len(selected),
      'selected_facts':selected,'accepted_editorial_moves':accepted,'rejected_editorial_moves':rejected,
      'editorial_move_count':len(accepted),
      'doctrine':'Style may illuminate proved meaning. Style may not create new facts.',
      'roles':[
        'Editor-in-Chief','Humanist','Investigative Editor','Minimalist','Analogy Writer','Satirist','Skeptic','Citation Referee'
      ],
      'guardrails':[
        'Every factual claim must come from court-cleared semantic coverage.',
        'Every synthesis, analogy, or joke must list the facts it interprets.',
        'Humor targets complexity or structure, not people or parties.',
        'No motive, corruption, distributional winner/loser, or causal claim is inferred without evidence.',
        'The editor may omit facts; omission for clarity is not permission to distort the overall shape.'
      ]
    }
    out_path.parent.mkdir(parents=True,exist_ok=True)
    out_path.write_text(json.dumps(packet,indent=2),encoding='utf-8')
    return packet

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--coverage',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
    p=build_room(a.coverage,a.out)
    print(f"PASS 41 ROOM: selected {p['selected_fact_count']} facts; accepted {p['editorial_move_count']} editorial moves; rejected {len(p['rejected_editorial_moves'])}")
if __name__=='__main__': main()
