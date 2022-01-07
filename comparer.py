import solcx
import hashlib
import argparse
import json

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, nargs=1)

args = parser.parse_args()
if  args.file == None:
    print('No file in argument --file')
    exit(1)
files = args.file

f = open(files[0], 'r')

console = Console()

intro = '''
# Lauti's Contract Hasher Finder
'''

console.print(Markdown(intro))

ast = solcx.compile_files(files, output_values=['ast'], solc_version='0.8.9')

nodes = ast[list(ast.keys())[0]]['ast']['nodes']

contracts_location = []

#grab contracts and interfaces
for n in nodes:
    if n['nodeType'] in ['interface', 'contract', 'ContractDeclaration', 'ContractDefinition']:
        contracts_location.append(
            {
                'name': n['canonicalName'],
                'type': n['contractKind'],
                'location': n['src']
            }
        )

def calculate_hash(code):
    m = hashlib.sha3_256()
    m.update(code.encode())
    return m.hexdigest()

console.print(Markdown('## Found %d contracts' % len(contracts_location)))
print('\n')

print(', '.join([x['name'] for x in contracts_location]))

#grab source of each contract
codes = []
for c in contracts_location:
    loc = c['location'].split(':')[0:2]
    f.seek(int(loc[0]))
    codes.append(
        {
            'name': c['name'],
            'source': f.read(int(loc[1]))
        }
    )
f.close()

#calculate hashes

console.print(Markdown('## Printing contract hashes'))
print('\n')

hashes = {c['name']:calculate_hash(c['source']) for i,c in enumerate(codes)}

for h in hashes:
    print(h + ':', hashes[h])

#compare hashes

with open('solidity_repos/hashes.json', 'r') as f:
    db = json.loads(f.read())

hash_md = '''
# Comparing Hashes
'''
console.print(Markdown(hash_md))


table = Table()
table.add_column('Contract Name', style='cyan')
table.add_column('Hash')
table.add_column('Match')
table.add_column('Found', style='green')
table.add_column('Variation')
table.add_column('Comments')

hits = 0
for h in hashes:
    if hashes[h] in db:
        hits += 1
        aux_hash = hashes[h]
        found = db[aux_hash]
        table.add_row(h, aux_hash[0:4] + '...' + aux_hash[-4:], '[green]:heavy_check_mark:', found['name'], str(found['variation']), found['comments'])
    else:
        table.add_row(h, aux_hash[0:4] + '...' + aux_hash[-4:], '[red]:heavy_multiplication_x:')

console.print(table)

console.print(str(hits) + '/' + str(len(hashes)) + ' contracts found')
