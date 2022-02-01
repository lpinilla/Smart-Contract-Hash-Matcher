import solcx
import hashlib
import argparse
import json
import re
import semantic_version
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', type=str, nargs='*', help='Provide the files to analyze')
parser.add_argument('-d', '--database', type=str, nargs='?', help='Select hash database')
parser.add_argument('-w', '--whitelist-hashes', type=str, nargs=1, help='Comma separated whitelist contract hashes')

default_solidity_version = semantic_version.Version('0.8.10')

def check_arguments():
    args = parser.parse_args()
    if  args.files == None:
        sys.exit('No file in argument --file')
    if args.database == None:
        sys.exit('No database in argument --database')
    return args

def extract_solidity_version(file):
    f = file.read()
    match = re.search('pragma solidity \^?[0-9. ]*;', f)
    pragma = f[match.start():match.end()]
    unlocked = '^' in pragma
    if unlocked:
        return semantic_version.Version(pragma[-6:-1]), unlocked
    return semantic_version.Version(pragma[-7:-1]), unlocked


def setup_solidity_version(version):
    #install if not found
    if version not in solcx.get_installed_solc_versions():
        solcx.install_solc(version)
    solcx.set_solc_version(version)

def compile_file(file_name, file_data, console):
    console.print(Markdown('## Analyzing ' + file_name))
    solc_version, unlocked = extract_solidity_version(file_data)
    if unlocked:
        solc_version = default_solidity_version
    else:
        setup_solidity_version(solc_version)
    return solc_version, solcx.compile_files(file_name, output_values=['ast'], solc_version=solc_version)

def parse_contract(ast, version, console):
    if version.minor >= 7:
        nodes = ast[list(ast.keys())[0]]['ast']['nodes']
    else:
        nodes = ast[list(ast.keys())[0]]['ast']['children']
    contracts_location = []
    #grab contracts and interfaces
    for n in nodes:
        if version.minor >= 7:
            if n['nodeType'] in ['interface', 'contract', 'ContractDeclaration', 'ContractDefinition']:
                contracts_location.append(
                    {
                        'name': n['canonicalName'],
                        'type': n['contractKind'],
                        'location': n['src']
                    }
                )
        else:
            if n['name'] in ['interface', 'contract', 'ContractDeclaration', 'ContractDefinition']:
                contracts_location.append(
                    {
                        'name': n['attributes']['name'],
                        'type': n['attributes']['contractKind'],
                        'location': n['src']
                    }
                )
    console.print(Markdown('## Found %d contracts' % len(contracts_location)))
    console.print(Markdown(''.join(['\n - ' + x['name'] for x in contracts_location])))
    return contracts_location

def grab_contracts(f, contracts_location):
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
    return codes

def calculate_hashes(codes, console):
    console.print(Markdown('## Printing contract hashes'))
    hashes = {c['name']:contract_hash(c['source']) for i,c in enumerate(codes)}
    for h in hashes:
        console.print(h + ':', hashes[h])
    return hashes

def contract_hash(code):
    m = hashlib.sha3_256()
    m.update(code.encode())
    return m.hexdigest()

def add_whitelist_to_database(arg_database, whitelist_hashes):
    if arg_database == None:
        db_file = 'hashes.json'
    else:
        db_file = arg_database
    with open(db_file, 'r') as f:
        db = json.loads(f.read())
    #checking whitelists
    if whitelist_hashes:
        whitelist_obj = {
            'name': 'User-provided whitelist',
            'variation': '-',
            'comments': 'Command line whitelist argument'
        }
        partial = [{h:whitelist_obj} for h in whitelist_hashes[0].split(',')]
        for p in partial:
            db.update(p)
    return db

def compare_and_build_table(hashes, db, console):
    console.print(Markdown('# Comparing Hashes'))
    table = Table()
    table.add_column('Contract Name', style='cyan')
    table.add_column('Hash')
    table.add_column('Match')
    table.add_column('Found', style='green')
    table.add_column('Variation')
    table.add_column('Comments')
    hits = 0
    for h in hashes:
        aux_hash = hashes[h]
        if aux_hash in db:
            hits += 1
            found = db[aux_hash]
            table.add_row(h, aux_hash[0:4] + '...' + aux_hash[-4:], '[green]:heavy_check_mark:', found['name'], str(found['variation']), found['comments'])
        else:
            table.add_row(h, aux_hash[0:4] + '...' + aux_hash[-4:], '[red]:heavy_multiplication_x:', '[red]-', '-', '-')
    console.print(table)
    console.print(str(hits) + '/' + str(len(hashes)) + ' contracts found')

def main():
    args = check_arguments()
    console = Console()
    console.print(Markdown('# Smart Contract Hasher Finder'))
    files = args.files[0].split(',')
    for file in files:
        f = open(file, 'r')
        version, ast = compile_file(file, f, console)
        contract_locations = parse_contract(ast, version, console)
        codes = grab_contracts(f, contract_locations)
        console.print(Markdown('### Using version: ' + str(version.major) + '.' + str(version.minor) + '.' + str(version.patch)))
        hashes = calculate_hashes(codes, console)
        db = add_whitelist_to_database(args.database, args.whitelist_hashes)
        compare_and_build_table(hashes, db, console)

if __name__ == "__main__":
    main()

