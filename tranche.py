import json

HONEST = 10_000_000
DIFFERENT = False
PERCENTS = []
PRECISION = 8

assert sum(PERCENTS) <= 1, "Percents total more than 100"


# Take 10%
# HONEST /= 10

# there are now 1.0 Mil coins

#                 __
# TRANCHE = 90909.09

with open("final_data.json") as handle:
    data = json.loads(handle.read())
    handle.close()

groups = list(data.values())

assert len(PERCENTS) == len(groups), "Inequal lengths for PERCENTS and data"

TRANCHES = len(groups)

TRANCHE = HONEST / TRANCHES

groups_amt = []



for idx, group in enumerate(groups):
    if isinstance(group, list):
        groups_amt.append(
            {
                account_id: int(((TRANCHE if not DIFFERENT else PERCENTS[idx]*HONEST) / len(group)) * 10**PRECISION) / 10**PRECISION
                for account_id in group
            }
        )
    elif isinstance(group, dict):
        gsum = sum([int(i.replace(",", "")) for i in group.values()])
        groups_amt.append(
            {
                account_id: int((TRANCHE if not DIFFERENT else PERCENTS[idx]*HONEST) * (int(v.replace(",", "")) / gsum) * 10**PRECISION)
                / 10**PRECISION
                for account_id, v in group.items()
            }
        )

with open("amt_data.json", "w") as handle:
    handle.write(json.dumps(groups_amt, indent=4))
    handle.close()
