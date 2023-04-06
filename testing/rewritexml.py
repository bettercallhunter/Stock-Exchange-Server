filename = 'transactions3.xml'
# filename = '../randomTransactions.xml'

# Read file content and calculate length
with open(filename, 'r') as f:
    content = f.read()
    length = len(content)

# Update file with length at the beginning
with open(filename, 'w') as f:
    f.write(str(length) + '\n' + content)
