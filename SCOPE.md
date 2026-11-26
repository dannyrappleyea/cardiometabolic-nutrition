# Scope — who this research is for

> **Human-owned.** Agents may propose changes by pull request (for example, after checking a threshold against a newer guideline) but never edit this file on their own.
> **Status: v1 (2026-11-26).** Thresholds were checked in the 2026-11-24 discovery run (`research/_plan/scope-check.yaml`), and its proposed corrections for blood pressure, body size, kidneys, resistant hypertension and severe hypertension were adopted. Rows still marked `unverified` there are design choices (such as the age band) or wait on full guideline text. Each discovery run re-checks this file (`playbooks/01-discover.md`, step 1).

This file defines the population, not the answers. It deliberately names no diets, foods or nutrients.

## 1. The cohort in one sentence

Adults roughly 40–75 with a cardiometabolic risk cluster (raised blood pressure, impaired glucose regulation and atherogenic dyslipidemia, usually with excess weight) who are in primary prevention, may already take medication for these conditions, and want to use diet, grounded in evidence, to reach and hold their clinical targets.

## 2. Zones

Research is written for the **core** cohort. Each topic must say where its conclusions change for the **adjacent** cohort. People **out of scope** are told plainly that this research was not built for them.

| Zone | Meaning | What agents do |
|---|---|---|
| **Core** | Meets §3 and none of §4–5 | Optimize research for them |
| **Adjacent** | Meets §3 but one or more §4 flags apply | Topics flag where advice changes; personal guides carry the caution and send the person to their clinician on that point |
| **Out of scope** | Any §5 exclusion | Personal setup says so, recommends clinician/dietitian care, and builds no guide unless the person explicitly asks for one anyway, in which case every page carries a banner |

## 3. Inclusion (core)

**Age:** 40–75 years. Adult, not pregnant or breastfeeding.

**At least two of the following three domains**, or one domain plus overweight/obesity:

| Domain | Core range | Notes |
|---|---|---|
| **Blood pressure** | Elevated through stage 2: systolic 120–179 and/or diastolic 80–119 mmHg (office or home average), treated or untreated | The range follows the ACC/AHA 2025 categories: elevated 120–129/<80; stage 1 130–139 or 80–89; stage 2 ≥140 or ≥90. Hypertension Canada 2025 also uses 130/80; ESC 2024 and NICE use 140/90, and ESC calls 120–139/70–89 "elevated", so some people called elevated in Europe (systolic below 120, diastolic 70–79) are not core here. Topics name the classification they use |
| **Glycemia** | Prediabetes (A1C 5.7–6.4%, or the fasting/OGTT equivalent) or type 2 diabetes with A1C below ~9.0% | Not using insulin or medicines that commonly cause hypoglycemia (see §5) |
| **Lipids** | LDL-C 100–189 mg/dL, and/or triglycerides 150–499 mg/dL, and/or non-HDL-C ≥130 mg/dL, and/or low HDL-C | Treated or untreated. Includes mixed dyslipidemia |

**Body size:** BMI 25–39.9 kg/m² (or 23–37.4 for people of South Asian, Chinese, other Asian, Middle Eastern, Black African or African-Caribbean family background, per NICE NG246), or a waist above the sex-specific cut-off. Normal-weight people meeting the domain rule are also core.

**Kidneys:** eGFR ≥60 and UACR <30 mg/g with no other known marker of kidney damage (KDIGO 2024: urine sediment abnormalities, persistent hematuria, tubular disorders, abnormal histology or imaging, or a kidney transplant), or not yet tested. "Not yet tested" means kidney status is unknown, not that kidney disease is absent; personal guides then ask the person to find out, because several rules can depend on it.

**Medications:** any combination of medicines commonly prescribed for these conditions, except those in §5. Discovery enumerates which medication classes are common in this cohort; topics cover food–drug interactions for those classes.

## 4. Adjacent flags (in scope with cautions)

- Age 30–39 or 76–79.
- BMI ≥40 (≥37.5 for the groups with lower thresholds in §3).
- eGFR 45–59, or UACR 30–300 mg/g.
- Type 2 diabetes with A1C 9.0% or higher.
- LDL-C ≥190 mg/dL or suspected familial hypercholesterolemia.
- Established cardiovascular disease (prior heart attack, stroke, revascularization, peripheral artery disease): secondary prevention, where targets usually differ.
- Resistant hypertension: blood pressure above the person's treatment goal despite three or more drug classes, one of them a diuretic, at maximally tolerated doses. This includes ESC 2024's narrower definition (office BP ≥140/90 confirmed out of office, after excluding pseudo-resistance such as missed doses or white-coat readings); the broader wording is used because this flag only adds caution.
- Fatty liver disease without cirrhosis.
- Gout, or kidney stones.
- Food allergies, celiac disease, or religious, cultural or ethical dietary rules: handled through the personal profile, not by the research.

## 5. Out of scope (exclusions)

- Under 18, pregnant, breastfeeding, or planning pregnancy.
- Type 1 diabetes, LADA, or any diabetes treated with insulin, sulfonylureas or meglitinides (hypoglycemia risk changes the dietary advice).
- Triglycerides ≥500 mg/dL (a distinct dietary approach applies).
- eGFR <45, dialysis, or kidney transplant.
- Heart failure, cirrhosis, or active cancer treatment.
- Current or past eating disorder.
- Bariatric surgery.
- Severe hypertension (systolic above 180 and/or diastolic above 120 mmHg) at any time without a clinician's plan, or any hypertensive emergency: high blood pressure with symptoms or acute organ damage, whatever the reading (ESC 2024 uses ≥180/110 mmHg with acute organ damage).

## 6. What "evidence-based dietary management" covers

In scope: anything a person eats or drinks and how, when and how much (patterns, foods, food groups, nutrients, beverages, ingredients and additives, supplements as they relate to food, energy and weight, meal timing and structure, cooking, eating out), food–medication interactions, and the clinical targets diet is trying to move. Behavior and physical activity are in scope only where they change dietary advice.

Out of scope: choosing, starting, stopping or dosing medications; diagnosing; exercise programming beyond its interaction with diet.

## 7. Reading level and length

Write for an engaged adult with no science training: explain terms on first use, use absolute numbers alongside relative ones, and keep sentences short. Depth comes from completeness and nuance, not jargon. Length limits are in `METHODS.md` §6.
