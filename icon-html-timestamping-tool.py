import requests
import iconsdk

#Set URL for import
url = input("What URL would you like to timestamp?")

#Set HTTP headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

html = requests.get(url, headers=headers)
html_decode = html.content.decode()
html_hex = html_decode.encode("utf-8").hex()

#Load ICON wallet
from iconsdk.wallet.wallet import KeyWallet
wallet = KeyWallet.load("./iconkeystore", "@icon111")

#Build ICX transaction
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)
from iconsdk.signed_transaction import SignedTransaction
transaction = MessageTransactionBuilder()\
    .from_(wallet.get_address())\
    .to("hxd4ed86cb5dafb842701683b8c35b21d28df563c3")\
    .step_limit(10000000)\
    .data("0x" + html_hex)\
    .nid(1)\
    .nonce(100)\
    .build()

from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
icon_service = IconService(HTTPProvider("https://wallet.icon.foundation/api/v3"))

signed_transaction = SignedTransaction(transaction, wallet)
tx_hash = icon_service.send_transaction(signed_transaction)

print("Tranaction Hash: " + tx_hash)