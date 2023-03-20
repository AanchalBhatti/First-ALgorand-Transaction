# CODE FOR PAYMENT TRXN BY using the information of THE ACCOUNT already created using USER INTERFACE

import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk import transaction


def first_transaction_example( my_address1, my_address2, my_address3, pk1, pk2):
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "gqXFTgP7M54pqYRdPxIm14LBaRGynGMO4BodJRoc"
    headers = {
        "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    # build transaction

    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000

    txn_1 = transaction.PaymentTxn(my_address1, params, my_address3, 100000)
    txn_2 = transaction.PaymentTxn(my_address2, params, my_address1, 200000)

    # get group id and assign it to transactions
    gid = transaction.calculate_group_id([txn_1, txn_2])
    txn_1.group = gid
    txn_2.group = gid

    # sign transactions
    stxn_1 = txn_1.sign(pk1)
    stxn_2 = txn_2.sign(pk2)

    # assemble transaction group
    signed_group = [stxn_1, stxn_2]

    tx_id = algod_client.send_transactions(signed_group)

    # wait for confirmation

    confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print("txID: {}".format(tx_id), " confirmed in round: {}".format(
        confirmed_txn.get("confirmed-round", 0)))

    print('DONE')

add1 = 'BJ67S6NJXXS277JRMHNU6X6GORQS6CS26E3Y3VR5IVUEWHOCDMLKMUBTZE'
add2 = '2T7INOB2KC3IQVPVE6ERXVBI7ID2YLUIKLYOT4L2ZESPMPT3LE2DIXPJJA'
add3 = 'PIDOSB3YFVJPHYNBMMKFMWWYWJ3BW62V2NX3O6SXI5WOG2KJPYFDIVV4AE'
pk1 = mnemonic.to_private_key('quality silver disease pulse jazz chunk bullet limb bounce engage soda faint ignore biology champion stereo master visual gain account permit night load above phrase')
pk2 = mnemonic.to_private_key('able athlete cradle suspect manage entry fat glimpse riot gap ladder behave fuel rescue inherit happy salon current ocean decade thought prison hero ability anxiety')


# replace private_key and my_address with your private key and your address.
first_transaction_example(add1, add2, add3, pk1, pk2)
