# Outputs alephium miner wallet balances to console and html file.
# use "python -m http.server" in terminal to start http server before running script. Make sure you start server from the same directory you have the script stored

from urllib.request import urlopen
import time
import datetime
import json

while True: #refreshes balance every 2 minutes

    # define addresses and create urls for fetching balances
    address0 = str("miningaddress 0 goes here")
    address1 = str("miningaddress 1 goes here")
    address2 = str("miningaddress 2 goes here")
    address3 = str("miningaddress 3 goes here")
    node_url = str("http://127.0.0.1:12973/addresses/") # address of your alph node, typically you would run on the same machine.
    balance = str("/balance")
    group0 = (node_url + address0 + balance)
    group1 = (node_url + address1 + balance)
    group2 = (node_url + address2 + balance)
    group3 = (node_url + address3 + balance)

    # fetch balances
    response0 = urlopen(group0)
    response1 = urlopen(group1)
    response2 = urlopen(group2)
    response3 = urlopen(group3)

    # read json from balances
    data_json0 = json.loads(response0.read())
    data_json1 = json.loads(response1.read())
    data_json2 = json.loads(response2.read())
    data_json3 = json.loads(response3.read())

    balance0 = int(data_json0['balance'])
    balance1 = int(data_json1['balance'])
    balance2 = int(data_json2['balance'])
    balance3 = int(data_json3['balance'])
    balance0_locked = int(data_json0['lockedBalance'])
    balance1_locked = int(data_json1['lockedBalance'])
    balance2_locked = int(data_json2['lockedBalance'])
    balance3_locked = int(data_json3['lockedBalance'])
    total_balance = balance0 + balance1 + balance2 + balance3
    total_balance_locked = balance0_locked + balance1_locked + balance2_locked + balance3_locked

    # Print balances to console
    now = datetime.datetime.now()
    print("--------------------------------------")
    print(now)
    print("Total Balance: ", total_balance / 1000000000000000000)
    print("Total Locked Balance: ", total_balance_locked / 1000000000000000000)
    print("Available Balanse: ", (total_balance - total_balance_locked) / 1000000000000000000)
    print("")
    print(address0, ": ", balance0 / 1000000000000000000, "of which ", balance0_locked / 1000000000000000000, " is locked")
    print(address1, ": ", balance1 / 1000000000000000000, "of which ", balance1_locked / 1000000000000000000, " is locked")
    print(address1, ": ", balance2 / 1000000000000000000, "of which ", balance2_locked / 1000000000000000000, " is locked")
    print(address1, ": ", balance3 / 1000000000000000000, "of which ", balance3_locked / 1000000000000000000, " is locked")
    print("")

    # create html file
    Func = open("balance.html", "w")

    # Adding balances to file
    Func.write(f"Time: {now}<P>"
               f"Total Balance: {total_balance / 1000000000000000000} <br>"
               f"Total Locked Balance: {total_balance_locked / 1000000000000000000} <br>"
               f"Total available balance: {(total_balance - total_balance_locked) / 1000000000000000000}<br><hr>"
               f"<b>{balance0 / 1000000000000000000}</b> of which {balance0_locked / 1000000000000000000} is locked: {address0}  <br>"
               f"<b>{balance1 / 1000000000000000000}</b> of which {balance1_locked / 1000000000000000000} is locked: {address1}  <br>"
               f"<b>{balance2 / 1000000000000000000}</b> of which {balance2_locked / 1000000000000000000} is locked: {address2}  <br>"
               f"<b>{balance3 / 1000000000000000000}</b> of which {balance3_locked / 1000000000000000000} is locked: {address3}  <br>"
            )

    # Saving html file
    Func.close()

    time.sleep(120) # sleep for 2 minutes before checking balances again.
