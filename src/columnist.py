"""PASS 41.1 - The Columnist.

Find one human story inside the court-cleared TCJA substrate. The columnist is
not rewarded for coverage. It is rewarded for selection, narrative pull, and
truthful compression. Every paragraph keeps an evidence ledger.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

SELECTED_FACT_IDS = [
    'rates_window',
    'personal_exemption_zero',
    'salt_cap',
    'child_credit_amount',
    'refundable_cap',
    'child_ssn',
    'qbi_20_percent',
    'qbi_wage_property_limit',
    'corporate_rate',
    'estate_exclusion',
    'oz_definition',
    'oz_nomination',
    'oz_180_days',
    'oz_ten_year',
]

THESIS = (
    "The revealing thing about TCJA is not one tax rate. It is how often a simple public headline "
    "turns into a different rule once the statute's clocks, conditions, and gatekeepers are put back in."
)

VOICE = (
    "Original Bill X-Ray columnist voice: plainspoken, curious, dry when complexity earns it, "
    "nonpartisan, and more interested in revealing structure than displaying expertise."
)

BAN_WORDS = ('corrupt','bribe','scam','fraud','theft','stole','pork')

def wc(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))

def build_column(coverage_path: Path, out_path: Path) -> dict:
    cov = json.loads(coverage_path.read_text(encoding='utf-8'))
    all_facts = {f['fact_id']: f for f in cov.get('facts', [])}
    missing = [fid for fid in SELECTED_FACT_IDS if fid not in all_facts]
    if missing:
        raise ValueError(f"Columnist missing cleared facts: {missing}")
    facts = {fid: all_facts[fid] for fid in SELECTED_FACT_IDS}
    paras = []

    def add(kind: str, text: str, support):
        bad = [w for w in BAN_WORDS if w in text.lower()]
        if bad:
            raise ValueError(f"Unsafe columnist language: {bad}")
        unknown = [fid for fid in support if fid not in facts]
        if unknown:
            raise ValueError(f"Unsupported columnist paragraph: {unknown}")
        paras.append({
            'paragraph_no': len(paras)+1,
            'kind': kind,
            'text': text,
            'support_fact_ids': list(support),
            'word_count': wc(text),
        })

    add('WIT',
        "Congress called it the Tax Cuts and Jobs Act, which has the great advantage of fitting on a bumper sticker. "
        "The law itself is less cooperative. Open it up and the headline tax cut immediately acquires dates, caps, thresholds, identification rules, and government officials with defined roles in parts of the system.",
        ['rates_window','salt_cap','child_credit_amount','child_ssn','oz_nomination'])

    add('SYNTHESIS',
        "That is the useful story hiding in this bill. A tax law is discussed in public as a handful of numbers. "
        "In the statute, those numbers behave more like doors: each one has hinges, a lock, and instructions about who may walk through it. "
        "If you remove the machinery, you have not simplified the law. You have changed its meaning.",
        ['child_credit_amount','refundable_cap','qbi_20_percent','qbi_wage_property_limit'])

    add('SYNTHESIS',
        "Start with time. The individual rate tables in this evidence packet run from 2018 through 2025. The personal exemption is set to zero for a temporary period. "
        "The covered state-and-local-tax deduction is capped at $10,000 during its temporary period. Yet the corporate-rate provision simply sets the federal corporate rate at 21% in the cited section, without that same temporary window. "
        "The statute is therefore carrying more than one clock.",
        ['rates_window','personal_exemption_zero','salt_cap','corporate_rate'])

    add('WIT',
        "Washington can fit a remarkable amount of policy inside the word 'temporary.' A citizen hearing 'the tax law' might reasonably imagine one object with one expiration date. "
        "What Congress actually built is closer to a house where different rooms have different leases.",
        ['rates_window','personal_exemption_zero','salt_cap','corporate_rate'])

    add('SYNTHESIS',
        "The child tax credit shows the same trick in miniature. The headline is wonderfully clean: the credit rises from $1,000 to $2,000 for the temporary period. "
        "But the refundable portion is capped at $1,400 per qualifying child under those rules, and the child must have the required Social Security number on the return. "
        "The $2,000 figure is real. It is simply not the whole sentence.",
        ['child_credit_amount','refundable_cap','child_ssn'])

    add('ANALOGY',
        "That distinction matters because public debate loves nouns: rate, credit, deduction, cut. Statutes live in verbs and conditions: qualifies, expires, phases in, carries forward, must provide. "
        "Bill X-Ray's job is to put the verbs back. Otherwise we are translating a recipe by listing only the ingredients.",
        ['child_credit_amount','refundable_cap','child_ssn','qbi_20_percent','qbi_wage_property_limit','rates_window'])

    add('WIT',
        "The new deduction for many noncorporate businesses provides another example. 'Twenty percent deduction' can be said before a waiter returns with your coffee. "
        "The law then introduces limits tied to W-2 wages and certain business property for some taxpayers. The short version is easy to remember. The conditions are part of the law anyway.",
        ['qbi_20_percent','qbi_wage_property_limit'])

    add('SYNTHESIS',
        "Then the law wanders into territory that barely resembles the kitchen-table image of filing taxes. It doubles the referenced basic estate-and-gift-tax exclusion from $5 million to $10 million before inflation adjustments. "
        "It also creates Qualified Opportunity Zones around designated low-income census tracts. State chief executives nominate the tracts, and the Treasury Secretary certifies and designates them under the statute's timetable.",
        ['estate_exclusion','oz_definition','oz_nomination'])

    add('WIT',
        "That Opportunity Zone provision is where a tax bill quietly starts behaving like a mapmaker. Congress did not choose every neighborhood itself. It wrote the rules for choosing the neighborhoods, then attached tax consequences to money that followed the map.",
        ['oz_definition','oz_nomination','oz_180_days','oz_ten_year'])

    add('FACT',
        "An investor can elect to defer eligible capital gain by putting it into a qualified Opportunity Fund within 180 days of the sale or exchange. For a qualifying investment held at least ten years, the taxpayer can elect to use fair market value as basis when the investment is sold or exchanged.",
        ['oz_180_days','oz_ten_year'])

    add('SYNTHESIS',
        "None of this proves that the law was good, bad, fair, unfair, brilliant, or foolish. Those are judgments. But it does reveal why a citizen trying to form an opinion from a slogan is starting several miles behind the starting line. "
        "The meaningful unit is rarely the headline number by itself. It is the number plus the clock, the conditions, the exceptions, and sometimes the official holding the pencil.",
        ['rates_window','child_credit_amount','child_ssn','qbi_20_percent','qbi_wage_property_limit','oz_nomination'])

    add('SYNTHESIS',
        "That may be the real X-ray. Not 'here are more facts about taxes,' but: here is the skeleton underneath the sentence you were handed. "
        "Once the skeleton is visible, the argument can finally belong to you. Keep the receipts downstairs. Give the citizen the meaning upstairs.",
        ['rates_window','child_credit_amount','qbi_20_percent','corporate_rate','oz_definition'])

    story = '\n\n'.join(p['text'] for p in paras)
    payload = {
        'schema_version': '41.1',
        'bill_id': 'TCJA',
        'title': 'I READ THE BILL',
        'column_title': 'The Tax Cut With More Than One Clock',
        'dek': 'The revealing part of TCJA is what happens after the headline number gets its conditions back.',
        'thesis': THESIS,
        'voice': VOICE,
        'available_fact_count': len(all_facts),
        'selected_fact_count': len(SELECTED_FACT_IDS),
        'selected_fact_ids': SELECTED_FACT_IDS,
        'omitted_fact_count': len(all_facts)-len(SELECTED_FACT_IDS),
        'paragraphs': paras,
        'story': story,
        'word_count': wc(story),
        'release_readiness': 'COLUMN_READY_FOR_RAY_GATE',
        'hook_gate': {
            'rule': 'After the first three paragraphs, a non-tax reader should want paragraph four.',
            'first_three_word_count': sum(p['word_count'] for p in paras[:3]),
        },
        'doctrine': 'Do not tell the reader everything the machine learned. Tell the one true story the evidence reveals.',
        'guardrails': [
            'No paragraph may use a fact outside the court-cleared semantic substrate.',
            'The columnist may omit facts aggressively but may not distort the basic shape of the law.',
            'Wit must reveal structure, not assign motive or guilt.',
            'The column makes no distributional, causal, partisan, or motive claim not supported by the current evidence packet.',
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    return payload

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--coverage', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    p = build_column(a.coverage, a.out)
    print(f"PASS 41.1 COLUMNIST: {p['word_count']} words; {p['selected_fact_count']} of {p['available_fact_count']} facts selected; hook={p['hook_gate']['first_three_word_count']} words; readiness={p['release_readiness']}")

if __name__ == '__main__':
    main()
