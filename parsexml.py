import xml.etree.ElementTree as ET

# Create an example XML document
xml_string = '''
<create>
  <account id="123456" balance="1000"/>
  <symbol sym="SPY">
    <account id="123456">100000</account>
  </symbol>
</create>
'''

# Parse the XML document
root = ET.fromstring(xml_string)

# Extract data from the XML document
account_id = root.find('account').get('id')
balance = root.find('account').get('balance')
symbol = root.find('symbol').get('sym')
symbol_account = root.find('symbol/account').text

# Output the extracted data
print(f'Account ID: {account_id}')
print(f'Balance: {balance}')
print(f'Symbol: {symbol}')
print(f'Symbol Account: {symbol_account}')


