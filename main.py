# Outputs alephium miner wallet balances and mining poolto console and html file.
# If you have an api key for your node, this script will not work
# #(WARNING: Most users should use an API key for the node unless you have a secure local environment)

# Requirements:
# redis (pip install redis or if you use pycharm use package manager)

# use "python -m http.server" in the same folder as your script terminal to start http server before running script
# eg cd d:\alephium\server python -m http.server

import redis
from urllib.request import urlopen
import time
import datetime
import json

node_address = "http://192.168.0.28:12973" # alph mining node and port
redis_address = "192.168.0.28" # redis address (no http!!)
redis_port = 6379 # redis port
refresh_rate = 120 # How many seconds between refreshing page

while True:

    # add your 4 mining addresses. below will create urls for fetching balances
    address0 = str("")
    address1 = str("")
    address2 = str("")
    address3 = str("")
    node_url = str(node_address + str("/addresses/"))
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

# get hashrate, blocks found and payouts from redis:
    r = redis.Redis(host= redis_address, port=redis_port, decode_responses=True)
    pool_hashrate = r.get('pool-hashrate')
    blocks_found = r.hgetall('foundBlocks')
    no_blocks_found = len(blocks_found)
    pretty_blocks_found = json.dumps(blocks_found, indent=4)

    # Print balances to console
    now = datetime.datetime.now()
    print(now)
    print("Pool hashrate: ", pool_hashrate , "Mhs")
    print("Number of blocks found (all time): ",no_blocks_found)
    print("--------------------------------------")
    print("Total Balance: ", total_balance / 1000000000000000000)
    print("Total Locked Balance: ", total_balance_locked / 1000000000000000000)
    print("Available Balance: ", (total_balance - total_balance_locked) / 1000000000000000000)
    print("")
    print(address0, ": ", balance0 / 1000000000000000000, "of which ", balance0_locked / 1000000000000000000, " is locked")
    print(address1, ": ", balance1 / 1000000000000000000, "of which ", balance1_locked / 1000000000000000000, " is locked")
    print(address2, ": ", balance2 / 1000000000000000000, "of which ", balance2_locked / 1000000000000000000, " is locked")
    print(address3, ": ", balance3 / 1000000000000000000, "of which ", balance3_locked / 1000000000000000000, " is locked")
    print("--------")#
    print("")
    print("Hash and miner address of blocks found")
    print(pretty_blocks_found)

    # create html file
    Func = open("balance.html", "w")
    print()
    print("--------------------------------------")

    # Adding balances to file
    Func.write(f"Time: {now}<P>"
               f"<b>Pool hashrate</b>: {pool_hashrate}  <br>"
               f"<b>Number of blocks found:</b>  {no_blocks_found}<p>"
               f"<b>Total Mining Wallet Balance:</b> {total_balance / 1000000000000000000} <br>"
               f"<b>Total Locked Balance:</b> {total_balance_locked / 1000000000000000000} <br>"
               f"<b>Total available balance:</b> {(total_balance - total_balance_locked) / 1000000000000000000}<br><hr>"
               f"<b>{balance0 / 1000000000000000000}</b> of which {balance0_locked / 1000000000000000000} is locked: {address0}  <br>"
               f"<b>{balance1 / 1000000000000000000}</b> of which {balance1_locked / 1000000000000000000} is locked: {address1}  <br>"
               f"<b>{balance2 / 1000000000000000000}</b> of which {balance2_locked / 1000000000000000000} is locked: {address2}  <br>"
               f"<b>{balance3 / 1000000000000000000}</b> of which {balance3_locked / 1000000000000000000} is locked: {address3}  <p>"
               f"-----Hash and miner address of blocks found------<br>"
               f"{blocks_found}"
            )

    # Saving html file
    Func.close()

    time.sleep(refresh_rate) # sleep for 2 minutes before checking balances again.
