# Smart-Contract-Hash-Matcher

Audit assist tool: Given a contract, find all subcontracts defined on it, calculate their sha-256 hash and look for exact matches

Uses python's rich module to render stylized output.

# Example

```console
python3 comparer.py --file TestToken.sol --solc-version 0.8.10

╔════════════════════════════════════════════════════════════════════════════╗
║                        Smart Contract Hasher Finder                        ║
╚════════════════════════════════════════════════════════════════════════════╝

                              Found 7 contracts


IERC20, IERC20Metadata, Context, ERC20, ERC20Burnable, Ownable, MyToken

                           Printing contract hashes

IERC20: 9e46130407dbeab48c601a830fd1792887ef132db58f46c9c16dedfed457aefd
IERC20Metadata: 6f121ffdf67e099229c561d7a55d0a72491e5051defc7de62b6c05a40259d01d
Context: d4b19ac6483ea2dc9627a885d01d6a85bac0e3e9fda0c8dc261061469f89a464
ERC20: c42cf3d9cd5d9fd2f67296f5a414aad0ff5fdb3eafb41802e596162633d9ab69
ERC20Burnable: b426fd9e81662a1e9ff20380d4119807ac8f8a0409aa4a40b91cd66d8771b84c
Ownable: 928e186fea8968d687543881cfe1cf954b9baff990cd5ff88383bad394d5eaa7
MyToken: 7b687d77d47d4aaeaf1170f40e973c13315ccdde9cedbad6da677a4887d301d1
╔════════════════════════════════════════════════════════════════════════════╗
║                              Comparing Hashes                              ║
╚════════════════════════════════════════════════════════════════════════════╝
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Contract Name ┃ Hash        ┃ Match ┃ Found         ┃ Variation ┃ Comments ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━┩
│ IERC20        │ 9e46...aefd │ ✔     │ @openzeppeli… │ False     │ Original │
│ IERC20Metada… │ 6f12...d01d │ ✔     │ @openzeppeli… │ False     │ Original │
│ Context       │ d4b1...a464 │ ✔     │ @openzeppeli… │ False     │ Original │
│ ERC20         │ c42c...ab69 │ ✔     │ @openzeppeli… │ False     │ Original │
│ ERC20Burnable │ b426...b84c │ ✔     │ @openzeppeli… │ False     │ Original │
│ Ownable       │ 928e...eaa7 │ ✔     │ @openzeppeli… │ False     │ Original │
│ MyToken       │ 928e...eaa7 │ ✖     │               │           │          │
└───────────────┴─────────────┴───────┴───────────────┴───────────┴──────────┘
6/7 contracts found

```
