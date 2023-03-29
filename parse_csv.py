import csv
import glob
import json
from pprint import pprint


def grab_data(filen):
    data = []
    with open(filen, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=["account_id", "count"])
        for row in csv_reader:
            data.append(row)

    data = {i["account_id"]: i["count"] for i in data[1::]}
    return data


files = glob.glob("*.csv")
data = {}
for filen in files:
    data[filen] = grab_data(filen)

# data3 = [int(k.split(".")[-1]) for k in data["output.csv"]]
# data3.sort()

# data2 = {}

data2["BORROW_HONEST"] = list(data["HONEST_call_order_update.csv"].keys())
data2["SWAP_HONEST"] = list(data["HONEST_pool_exchanges.csv"].keys())
data2["BORROW_ANY"] = list(data["call_order_update.csv"].keys())
data2["SWAP_ANY"] = list(data["pool_exchanges.csv"].keys())
data2["TRANSFER_BTSMG"] = data["transfer_to_BTSMG.csv"]
data2["ALL_ACTIVITY"] = list(data["top_thou_active_accounts.csv"].keys())[:-1]


with open("final_data.json", "w") as handle:
    handle.write(json.dumps(data2, indent=4))
    handle.close()

