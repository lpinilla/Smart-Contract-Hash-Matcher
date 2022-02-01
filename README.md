# Smart-Contract-Hash-Matcher

Audit assist tool: Given a contract, find all subcontracts defined on it, calculate their sha-256 hash and look for exact matches

Uses python's rich module to render stylized output.

# Example

```console
python3 comparer.py -f TestToken.sol -d hashes.json

╔════════════════════════════════════════════════════════════════════════════╗
║                        Smart Contract Hasher Finder                        ║
╚════════════════════════════════════════════════════════════════════════════╝

                           Analyzing TestToken.sol

                              Found 7 contracts

 • IERC20
 • IERC20Metadata
 • Context
 • ERC20
 • ERC20Burnable
 • Ownable
 • MyToken
                            Using version: 0.8.10

IERC20: 9e46130407dbeab48c601a830fd1792887ef132db58f46c9c16dedfed457aefd
IERC20Metadata:
6f121ffdf67e099229c561d7a55d0a72491e5051defc7de62b6c05a40259d01d
Context: 66814478c7b1daddde1a0409dc0c1657882deba3ea30ee89696d83b3103cce84
ERC20: c42cf3d9cd5d9fd2f67296f5a414aad0ff5fdb3eafb41802e596162633d9ab69
ERC20Burnable:
b426fd9e81662a1e9ff20380d4119807ac8f8a0409aa4a40b91cd66d8771b84c
Ownable: 928e186fea8968d687543881cfe1cf954b9baff990cd5ff88383bad394d5eaa7
MyToken: 7b687d77d47d4aaeaf1170f40e973c13315ccdde9cedbad6da677a4887d301d1
╔════════════════════════════════════════════════════════════════════════════╗
║                              Comparing Hashes                              ║
╚════════════════════════════════════════════════════════════════════════════╝
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Contract    ┃ Hash        ┃ Match ┃ Found        ┃ Variation ┃ Comments    ┃
┃ Name        ┃             ┃       ┃              ┃           ┃             ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ IERC20      │ 9e46...aefd │ ✔     │ @openzeppel… │ False     │ Original    │
│ IERC20Meta… │ 6f12...d01d │ ✔     │ @openzeppel… │ False     │ Original    │
│ Context     │ 6681...ce84 │ ✔     │ @openzeppel… │ True      │ Only        │
│             │             │       │              │           │ _msgSender  │
│             │             │       │              │           │ function    │
│ ERC20       │ c42c...ab69 │ ✔     │ @openzeppel… │ False     │ Original    │
│ ERC20Burna… │ b426...b84c │ ✔     │ @openzeppel… │ False     │ Original    │
│ Ownable     │ 928e...eaa7 │ ✔     │ @openzeppel… │ False     │ Original    │
│ MyToken     │ 7b68...01d1 │ ✖     │ -            │ -         │ -           │
└─────────────┴─────────────┴───────┴──────────────┴───────────┴─────────────┘
6/7 contracts found

```
