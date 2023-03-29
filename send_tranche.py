import json
from getpass import getpass

from signing_bitshares import (
    bitshares_nodes,
    broker,
    control_panel,
    prototype_order,
    wss_query,
)

WIF = getpass("WIF: ")
control_panel()
rpc_account_id = lambda account_name: wss_query(
    ["database", "lookup_accounts", [account_name, 1]], nodes=bitshares_nodes()
)[0][1]



with open("amt_data.json") as handle:
    data = json.loads(handle.read())
    handle.close()

# data = {"litepresence1": 1, "squidkid-deluxe256": 1}
# data = [{rpc_account_id(k): v for k, v in data.items()}]

user = input("Username: ")

user = [user, rpc_account_id(user)]

for item in data:
    edicts = []

    order = prototype_order()
    order["header"]["wif"] = WIF
    order["header"]["account_name"] = user[0]
    order["header"]["account_id"] = user[1]
    for account_id, amount in item.items():
        if account_id != user[1]:
            edict = {}
            edict["op"] = "transfer"
            edict["account_id"] = account_id
            edict["amount"] = amount
            # edict["memo"] = "Ho Ho Ho"
            edicts.append(edict)
    order["edicts"] = edicts
    input(json.dumps(order["edicts"], indent=4) + "\n\nPress Enter to place above transaction, Ctrl+C or Ctrl+\\ to quit.")
    broker(order)
# print(json.dumps(order, indent=4))

# BOOM!! DONE


# SENT: 538091
# REAMAINS: 461909
#           461909.000045

# expected to remain: 90909.9090909090 * 5 = 454545.454545
# diff: 7363.5455

# ^^ THUS goes to `user85` because `if account_id != user[1]:` skips all transfers "user85 to user85"
