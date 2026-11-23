# 12 — Questions, recipes and restaurant checks (personal)

Read `personal/profile.md`, `personal/AGENTS.local.md` and `personal/guide/` first. All three tasks apply the guide's rules, the profile and AGENTS.md §3.

| Task | Default output | Writes files? |
|---|---|---|
| Question | Answer in conversation | No |
| Recipe modification | Modified recipe in conversation | Only on request → `personal/recipes/` |
| Restaurant check | Verdict and order in conversation | Only on request → `personal/restaurants/` |

**Saving rule:** results stay in the conversation unless the person asks to save them ("save this", "add it to my recipes"). One short offer is fine when they call something a favorite.

**Check saved results first:** look in `personal/recipes/README.md` or `personal/restaurants/README.md` and build on an existing entry.

## Questions

1. Answer from the guide and the topics, and stay consistent with them. If the honest answer contradicts a current rule, say so.
2. Cite the topic file by name when it covers the question. Otherwise use Tier 1–3 sources (METHODS §2), name them, and state confidence.
3. **Gaps:** when no topic covers a question that bears on a rule, say so in one line and offer to draft an upstream request (`13-propose-upstream.md`). Don't edit `research/`.
4. Match length to the question.

## Recipes

1. Use `personal/guide/recipe-prompt.md` (targets, swap rules, output format). It must stay a self-contained prompt that works in any AI, so it's rebuilt with the guide.
2. Nutrition figures are estimates: say so, and suggest logging the final version in the person's tracking app if they use one.
3. **Saving:** `personal/recipes/<dish-name>.md` from `personal/recipes/_template.md`; add a row to `personal/recipes/README.md`. Write ingredients and steps in your own words and link the original rather than copying it.

## Restaurants

1. **Numbers:** the restaurant's official nutrition information first. With none, estimate from comparable dishes, give ranges, label them "estimate", and err toward the less favorable end.
2. **Judge the meal as ordered** against the guide's per-meal targets and rules and the profile.
3. **Verdict:** 🟢 fits as ordered · 🟡 fits with the listed changes · 🟠 occasional/flex meal · 🔴 skip.
4. **Output:** verdict; the order with modifications; estimated nutrition; one line on adjusting the rest of the day. For 🟠 or 🔴, name the best alternative on the same menu.
5. **Saving:** `personal/restaurants/<restaurant-name>.md` from the template, one section per favored meal; update the README. Re-check menu data older than 12 months.
