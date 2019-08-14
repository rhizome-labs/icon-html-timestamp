import binascii
import datetime
import iconsdk
import random
import requests
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.builder.transaction_builder import (TransactionBuilder, DeployTransactionBuilder, CallTransactionBuilder, MessageTransactionBuilder)
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

#Get ICONex wallet variables
keystore_location = input("What is the file path of your keystore file? ")
keystore_password = input("What is your keystore password? ")

#keystore_location = "/Users/iconkeystore "
#keystore_password = "@icon111"

keystore_location_str = keystore_location.rstrip()
keystore_password_str = keystore_password.rstrip()

#print(keystore_location)
#print(keystore_location_str)

#Create data and time formatting
date = datetime.datetime.utcnow()
utc_datetime = date.strftime("%Y-%m-%d %H:%M:%S")

#Set URL to scrape
url = input("What URL would you like to timestamp? (e.g. https://rhizomeicx.com) ")

#Set HTML headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#Scrape URL
page = requests.get(url, headers=headers)
html = page.content.decode()
info = "This timestamp of " + str(url) + " was taken at " + str(utc_datetime) + " UTC." + "\n\n" 
html_hex = html.encode("utf-8").hex()
info_hex = info.encode("utf-8").hex()
tx_message = info_hex + html_hex
tx_message_length = len(tx_message)

#Create ICX transaction
if tx_message_length > 509950:
	print("This HTML page is too large to timestamp in an ICX transaction.")
elif tx_message_length <= 509950:
	#print("This is a valid ICX transaction!")
	wallet = KeyWallet.load(keystore_location_str, keystore_password_str)
	#@icon111
	#Build ICX transaction
	transaction = MessageTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("hxd4ed86cb5dafb842701683b8c35b21d28df563c3")\
    .step_limit(100000000)\
    .data("0x" + tx_message)\
    .nid(1)\
    .nonce(random.randint(1,9999))\
    .build()
	icon_service = IconService(HTTPProvider("https://wallet.icon.foundation/api/v3"))
	signed_transaction = SignedTransaction(transaction, wallet)
	tx_hash = icon_service.send_transaction(signed_transaction)

#Print ICX transaction hash
print("Tranaction Hash: " + tx_hash)
