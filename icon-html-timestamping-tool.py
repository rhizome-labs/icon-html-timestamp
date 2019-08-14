#RHIZOME ProofOfRecord v0.1 by @DecryptoBL
import click
import datetime
import iconsdk
import requests
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.builder.transaction_builder import (TransactionBuilder, DeployTransactionBuilder, CallTransactionBuilder, MessageTransactionBuilder)
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

#Get URL header
url = input("What URL would you like to timestamp? (e.g. https://rhizomeicx.com) ")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url)

#Filter through common HTTP error codes
if response.status_code == 401:
   	url = input("401 error! Please provide a valid URL. ")
elif response.status_code == 402:
	url = input("403 error! Please provide a valid URL. ")
elif response.status_code == 403:
	url = input("403 error! Please provide a valid URL. ")
elif response.status_code == 404:
	url = input("404 error! Please provide a valid URL. ")
elif response.status_code == 500:
	url = input("500 error! Please provide a valid URL. ")
elif response.status_code == 502:
	url = input("502 error! Please provide a valid URL. ")
elif response.status_code == 502:
	url = input("503 error! Please provide a valid URL. ")
elif response.status_code == 504:
	url = input("504 error! Please provide a valid URL. ")

#Create data and time formatting
date = datetime.datetime.utcnow()
utc_datetime = date.strftime("%Y-%m-%d %H:%M:%S")

#Scrape URL
page = requests.get(url, headers=headers)
html = page.content.decode()

#Prepare ICX transaction message
html_hex = html.encode("utf-8").hex()
header = "This timestamp of " + str(url) + " was taken at " + str(utc_datetime) + " UTC." + "\n\n"
header_hex = header.encode("utf-8").hex()
footer = "\n\nTimestamped with ProofOfRecord v0.1 by RHIZOME - https://bit.ly/2Z4Dd8C"
footer_hex = footer.encode("utf-8").hex()

#Check if user would like to credit RHIZOME below timestamped HTML
if click.confirm("Would you like to credit RHIZOME below your timestamped HTML?", default=True):
    tx_message = header_hex + html_hex + footer_hex
else:
	tx_message = header_hex + html_hex

#Calculate transaction message length
tx_message_length = len(tx_message)
if tx_message_length > 509950:
	print("Sorry, this HTML page is too large to timestamp in an ICX transaction.")
	exit()
elif tx_message_length <= 509950:
	keystore_location = input("What is the file path of your keystore file? ")
	keystore_password = input("What is your keystore password? ")
	keystore_location_str = keystore_location.rstrip()
	keystore_password_str = keystore_password.rstrip()

#Create ICX transaction
wallet = KeyWallet.load(keystore_location_str, keystore_password_str)
transaction = MessageTransactionBuilder()\
	.from_(wallet.get_address())\
	.to("hxd4ed86cb5dafb842701683b8c35b21d28df563c3")\
	.step_limit(100000000)\
	.data("0x" + tx_message)\
	.nid(1)\
	.build()
icon_service = IconService(HTTPProvider("https://wallet.icon.foundation/api/v3"))
signed_transaction = SignedTransaction(transaction, wallet)
tx_hash = icon_service.send_transaction(signed_transaction)

#Print success message with link to transaction on ICON tracker
print("\nSuccess! View your timestamped HTML at the URL below.\nhttps://tracker.icon.foundation/transaction/" + tx_hash + "\n")
