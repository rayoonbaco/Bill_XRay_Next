"""PASS 40.1 - Semantic Coverage Expansion.

This module widens Bill X-Ray's human-meaning substrate without relaxing the
truth gate. It adds a second safe fact lane: direct statutory facts that can be
stated from the enacted text itself without importing unstated history, motive,
distributional effects, or outside estimates.

The resolver is intentionally conservative. Each fact is anchored to exact
source language. If the required anchors are not found in the expected section,
the fact is held rather than emitted.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

SECTION_RE = re.compile(r"^SEC\.\s+([0-9A-Z.-]+)\.\s+(.+?)\s*$")


@dataclass
class CoverageFact:
    fact_id: str
    bill_id: str
    section: str
    heading: str
    category: str
    statement: str
    why_it_matters: str
    source_start_line: int
    source_end_line: int
    evidence_excerpt: str
    confidence: float
    limits: list[str]
    status: str = "COURT_CLEARED_DIRECT"


@dataclass(frozen=True)
class FactSpec:
    fact_id: str
    section: str
    category: str
    anchors: tuple[str, ...]
    statement: str
    why_it_matters: str
    limits: tuple[str, ...] = ()


FACT_SPECS = (
    FactSpec("rates_window", "11001", "individual_tax", ("Modifications for Taxable Years 2018 Through 2025", "10% of taxable income", "37%"),
             "For tax years 2018 through 2025, the bill replaces the individual rate tables with seven brackets ranging from 10% to 37%.",
             "It changes the basic rate schedule used to calculate individual income tax.",
             ("This fact does not say how any particular household's total tax changes." ,)),
    FactSpec("rate_table_indexing", "11001", "delegated_authority", ("For taxable years beginning after December 31, 2018, the Secretary shall prescribe tables",),
             "After 2018, the Treasury Secretary must issue updated versions of the temporary individual tax tables using the law's inflation-adjustment rules.",
             "Congress sets the framework but leaves the annual table calculation to Treasury.",
             ("This does not imply open-ended discretion; the statute specifies how the adjustment is to be made.",)),
    FactSpec("kiddie_tax_special_rule", "11001", "specific_class", ("Special rules for certain children with unearned income", "shall apply in lieu of the rule under subsection (g)(1)"),
             "The bill creates a separate temporary tax-rate method for certain children with unearned income.",
             "A headline rate change does not apply identically to every taxpayer; this is a defined special case.",
             ("The fact does not quantify how many children pay more or less." ,)),
    FactSpec("qbi_20_percent", "11011", "business_tax", ("20 percent of the taxpayer's qualified", "business income"),
             "The bill creates a deduction generally based on 20% of qualified business income for eligible noncorporate business owners, subject to limits elsewhere in the section.",
             "This is one of the law's major new tax rules for pass-through business income.",
             ("Eligibility and the final deductible amount depend on definitions and limits in the section.",)),
    FactSpec("qbi_wage_property_limit", "11011", "business_tax", ("50 percent of the W-2 wages", "25 percent of the W-2 wages", "2.5 percent of the unadjusted basis"),
             "For some taxpayers, the qualified-business-income deduction is limited by formulas tied to W-2 wages and certain business property.",
             "The 20% headline deduction is not an unconditional 20% write-off for every business owner.",
             ("The limitation has income thresholds and phase-in rules." ,)),
    FactSpec("qbi_phase_in", "11011", "business_tax", ("plus $50,000 ($100,000 in the case of a joint return)",),
             "The bill phases in some qualified-business-income limits over a $50,000 income range, or $100,000 for joint returns, above the section's threshold amount.",
             "The effect of the deduction changes as taxable income moves through the phase-in range.",
             ("The base threshold amount is defined elsewhere in the section and may be inflation-adjusted." ,)),
    FactSpec("excess_loss_disallowance", "11012", "business_tax", ("any excess business loss of the taxpayer", "shall not be allowed"),
             "For noncorporate taxpayers in tax years 2018 through 2025, the bill temporarily disallows excess business losses above the section's limit.",
             "It restricts how much business loss can be used immediately against other income.",
             ("This statement does not estimate who is affected or by how much." ,)),
    FactSpec("excess_loss_threshold", "11012", "business_tax", ("$250,000 (200 percent of such",),
             "The excess-business-loss calculation uses a $250,000 amount, doubled for a joint return, before inflation adjustments after 2018.",
             "That dollar threshold determines when the temporary loss limitation starts to matter.",
             ("The threshold is part of a formula, not a flat tax or penalty." ,)),
    FactSpec("loss_carryover", "11012", "business_tax", ("Disallowed loss carryover", "net operating loss carryover to the following taxable year"),
             "A business loss disallowed by this temporary rule is carried into the following year as a net operating loss rather than simply disappearing.",
             "The rule changes timing as well as immediate deductibility.",
             ()),
    FactSpec("child_credit_amount", "11022", "family_tax", ("substituting `$2,000' for `$1,000'",),
             "For tax years 2018 through 2025, the bill increases the child tax credit amount from $1,000 to $2,000.",
             "It directly changes the headline credit amount for qualifying children.",
             ("Eligibility rules still determine whether a taxpayer can claim the credit." ,)),
    FactSpec("child_credit_phaseout", "11022", "family_tax", ("threshold amount shall be $400,000", "$200,000 in any other case"),
             "For the temporary child-credit rules, the income threshold is $400,000 for joint returns and $200,000 for other returns.",
             "The credit's availability changes at substantially different income levels depending on filing status.",
             ("This fact does not calculate the phaseout for any particular taxpayer." ,)),
    FactSpec("other_dependents", "11022", "family_tax", ("increased by $500 for each dependent", "other than a qualifying child"),
             "The bill adds a $500 credit for certain dependents who are not qualifying children for the main child credit.",
             "The family-credit changes extend beyond the headline $2,000 child-credit amount.",
             ("The statute includes exclusions and identification rules." ,)),
    FactSpec("refundable_cap", "11022", "family_tax", ("shall not exceed $1,400",),
             "The temporary rules cap the refundable portion of the child credit at $1,400 per qualifying child, with inflation adjustments after 2018.",
             "A $2,000 credit is not necessarily the same thing as receiving $2,000 as a refund.",
             ()),
    FactSpec("refundable_threshold", "11022", "family_tax", ("substituting", "`$2,500' for `$3,000'"),
             "The bill lowers the earned-income threshold used in the refundable child-credit calculation from $3,000 to $2,500.",
             "It changes when earned income begins to count toward the refundable calculation.",
             ()),
    FactSpec("child_ssn", "11022", "family_tax", ("Social security number required", "No credit shall be allowed"),
             "The bill requires a qualifying child's Social Security number on the tax return for the child credit to be allowed under these rules.",
             "The law adds an identification condition to claiming the credit.",
             ()),
    FactSpec("personal_exemption_zero", "11041", "individual_tax", ("Years when personal exemption amount is zero",),
             "For the temporary period covered by the section, the bill sets the personal exemption amount to zero.",
             "The law changes deductions as well as tax rates and credits.",
             ("Other provisions coordinate around the zero exemption amount; this statement does not calculate the net effect on a household." ,)),
    FactSpec("salt_cap", "11042", "individual_tax", ("shall not exceed $10,000 ($5,000 in the case of a married individual filing a separate return)",),
             "For the temporary period, the bill caps the covered state-and-local-tax deduction at $10,000, or $5,000 for married taxpayers filing separately.",
             "This places a dollar ceiling on a major category of itemized deductions.",
             ("The section contains exceptions, including taxes connected with a trade or business or income-producing activity." ,)),
    FactSpec("mortgage_debt_limit", "11043", "individual_tax", ("`$750,000 ($375,000' for `$1,000,000",),
             "For new acquisition debt covered by the temporary rule, the bill lowers the mortgage-debt ceiling used for the interest deduction from $1,000,000 to $750,000, with half-sized amounts for married filing separately.",
             "It narrows the amount of new home-acquisition debt whose interest can qualify for the deduction.",
             ("The section contains grandfather and transition rules for earlier debt and binding contracts." ,)),
    FactSpec("estate_exclusion", "11061", "estate_tax", ("`$10,000,000' for `$5,000,000'",),
             "The bill doubles the basic estate-and-gift-tax exclusion amount in the referenced rule from $5 million to $10 million before inflation adjustments.",
             "It raises the amount that can fall under the basic exclusion rule.",
             ("This statement does not estimate how many estates are affected." ,)),
    FactSpec("corporate_rate", "13001", "corporate_tax", ("shall be 21 percent of taxable income",),
             "The bill sets the federal corporate income-tax rate in section 11 at 21% of taxable income.",
             "This is a central permanent corporate-tax change in the Act.",
             ("This statement does not calculate a corporation's effective tax rate after other provisions." ,)),
    FactSpec("bonus_expensing_100", "13201", "business_tax", ("after September 27, 2017, and before", "January 1, 2023, 100 percent"),
             "For qualifying property placed in service after September 27, 2017 and before 2023, the bill sets the applicable bonus-depreciation percentage at 100%, followed by a scheduled phase-down.",
             "It allows qualifying investment costs to be deducted much faster during the initial period.",
             ("Different timing rules apply to certain longer-production property and specified plants." ,)),
    FactSpec("interest_limit", "13301", "business_tax", ("30 percent of the adjusted taxable income", "floor plan financing interest"),
             "The bill generally limits the business-interest deduction to business-interest income plus 30% of adjusted taxable income plus floor-plan financing interest.",
             "It places a formula-based ceiling on interest deductions for covered businesses.",
             ("The section contains exemptions and special partnership rules." ,)),
    FactSpec("interest_carryforward", "13301", "business_tax", ("Carryforward of disallowed business interest", "succeeding taxable year"),
             "Business interest disallowed by the new limit can generally be carried forward to a succeeding tax year.",
             "Like the excess-loss rule, this can change timing rather than permanently erase every disallowed deduction.",
             ("Partnerships have additional special rules." ,)),
    FactSpec("oz_definition", "13823", "place_based_tax", ("qualified opportunity zone' means a population", "census tract that is a low-income community"),
             "The bill creates Qualified Opportunity Zones built around designated low-income census tracts.",
             "It creates a new place-based tax framework rather than merely changing an existing rate or deduction.",
             ("Some contiguous tracts that are not themselves low-income communities may also qualify under limited conditions." ,)),
    FactSpec("oz_nomination", "13823", "delegated_authority", ("chief executive officer of the State", "nominates the tract", "Secretary certifies such nomination"),
             "State chief executives nominate Opportunity Zone tracts, and the Treasury Secretary certifies and designates them under the statute's timetable.",
             "The law splits the designation process between state and federal officials.",
             ()),
    FactSpec("oz_25_percent", "13823", "place_based_tax", ("may not exceed 25 percent of the number of low-income communities",),
             "As a general rule, a state may designate no more than 25% of its low-income communities as Opportunity Zones, with a small-state exception in the statute.",
             "Congress limits how broadly the zone designation can be used within a state.",
             ()),
    FactSpec("oz_contiguous", "13823", "place_based_tax", ("median family income of the tract does not", "exceed 125 percent", "Not more than 5 percent"),
             "The law allows a limited number of contiguous tracts that are not low-income communities to be designated if their median family income is no more than 125% of the neighboring qualified low-income tract; these tracts are capped at 5% of a state's designated zones.",
             "The program can extend beyond low-income tracts, but only under explicit proximity, income, and quantity limits.",
             ()),
    FactSpec("oz_duration", "13823", "place_based_tax", ("ending at the close of the", "10th calendar year"),
             "An Opportunity Zone designation lasts through the close of the tenth calendar year beginning on or after designation.",
             "The place designation is long-lived but not indefinite.",
             ()),
    FactSpec("oz_180_days", "13823", "place_based_tax", ("qualified opportunity fund during the 180-day period",),
             "A taxpayer can elect to defer eligible capital gain by investing it in a qualified Opportunity Fund within 180 days of the sale or exchange.",
             "This is the core tax incentive connecting capital gains to the new zones.",
             ("The statute limits eligible transactions and elections." ,)),
    FactSpec("oz_deferral_end", "13823", "place_based_tax", ("earlier of", "December 31, 2026"),
             "Deferred Opportunity Zone gain is brought back into income no later than the earlier of disposing of the investment or December 31, 2026.",
             "The deferral has an explicit endpoint; it is not an indefinite exclusion.",
             ()),
    FactSpec("oz_hold_benefits", "13823", "place_based_tax", ("held for at least 5 years", "10 percent", "held by the taxpayer for at least 7 years", "5 percent"),
             "The Opportunity Zone rules increase basis by 10% of deferred gain after a five-year hold and by another 5% after a seven-year hold.",
             "The statute rewards longer holding periods with additional basis adjustments.",
             ()),
    FactSpec("oz_ten_year", "13823", "place_based_tax", ("investments held for at least 10 years", "fair market value"),
             "For a qualifying Opportunity Zone investment held at least ten years, the taxpayer can elect to use fair market value as basis when the investment is sold or exchanged.",
             "That rule can change how post-investment appreciation is taxed after a long holding period.",
             ("This statement does not calculate the tax savings for any investor." ,)),
    FactSpec("oz_fund_90", "13823", "place_based_tax", ("holds at least 90 percent of its assets", "qualified opportunity zone property"),
             "A qualified Opportunity Fund must hold at least 90% of its assets in qualified Opportunity Zone property, measured under the statute's testing rule.",
             "The tax benefit is tied to an investment vehicle that must actually keep most of its assets in qualifying zone property.",
             ()),
)


def _sections(lines: list[str]) -> dict[str, tuple[str, int, int]]:
    starts=[]
    for i,line in enumerate(lines,1):
        m=SECTION_RE.match(line.strip())
        if m: starts.append((i,m.group(1),m.group(2).rstrip('.')))
    out={}
    for idx,(start,sec,heading) in enumerate(starts):
        end=starts[idx+1][0]-1 if idx+1 < len(starts) else len(lines)
        out[sec]=(heading,start,end)
    return out


def _find_fact(lines: list[str], bill_id: str, sec_info, spec: FactSpec) -> CoverageFact | None:
    heading,start,end=sec_info
    block='\n'.join(lines[start-1:end])
    positions=[]
    spans=[]
    for anchor in spec.anchors:
        # Congressional text wraps aggressively. Match ordinary spaces across line
        # breaks so source formatting cannot turn a true semantic fact into a miss.
        pattern=re.escape(anchor).replace(r'\ ', r'\s+')
        m=re.search(pattern, block, re.I)
        if not m:
            return None
        positions.append(m.start()); spans.append((m.start(),m.end()))
    first=min(x[0] for x in spans); last=max(x[1] for x in spans)
    # Map character offsets to lines and include a little local context.
    prefix=block[:first]
    sline=start + prefix.count('\n')
    eline=start + block[:last].count('\n')
    s=max(start,sline-1); e=min(end,eline+1)
    excerpt=' '.join(x.strip() for x in lines[s-1:e] if x.strip())
    return CoverageFact(spec.fact_id,bill_id,'SEC. '+spec.section,heading,spec.category,spec.statement,
                        spec.why_it_matters,s,e,excerpt,0.97,list(spec.limits))


def build_coverage(source: Path, bill_id: str='TCJA') -> dict:
    lines=source.read_text(encoding='utf-8').splitlines()
    secs=_sections(lines)
    facts=[]; holds=[]
    for spec in FACT_SPECS:
        info=secs.get(spec.section)
        if not info:
            holds.append({'fact_id':spec.fact_id,'reason':'section_not_found'})
            continue
        fact=_find_fact(lines,bill_id,info,spec)
        if fact: facts.append(fact)
        else: holds.append({'fact_id':spec.fact_id,'section':spec.section,'reason':'required_source_anchors_not_found'})
    cats={}
    for f in facts: cats[f.category]=cats.get(f.category,0)+1
    return {
        'schema_version':'40.1','bill_id':bill_id,'doctrine':'direct_statutory_meaning_before_editorial_prose',
        'fact_count':len(facts),'hold_count':len(holds),'category_counts':cats,
        'guardrail':'Direct statutory facts may state what the enacted text itself sets, requires, permits, limits, or creates. They may not infer motive, distributional effect, popularity, fairness, corruption, or real-world outcome without separate evidence.',
        'facts':[asdict(f) for f in facts],'holds':holds,
    }


def main():
    p=argparse.ArgumentParser(); p.add_argument('source'); p.add_argument('--out',required=True); p.add_argument('--bill-id',default='TCJA'); a=p.parse_args()
    payload=build_coverage(Path(a.source),a.bill_id)
    Path(a.out).parent.mkdir(parents=True,exist_ok=True); Path(a.out).write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(f"PASS 40.1: court-cleared {payload['fact_count']} direct statutory facts across {len(payload['category_counts'])} human categories; {payload['hold_count']} held")

if __name__=='__main__': main()
