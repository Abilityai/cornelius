---
created: '2026-01-10'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreiamayzfj4cyo4366tkkpculrc2wsfjhyptwffmacqu53dbdx2agae
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
local_path: /Users/jlb/Documents/Projects/Crypto/starklings
status: Done
---
# starklings   
 --- 
## Prerequisites   
- [Protostar](https://github.com/software-mansion/protostar) make sure you install it before you start!   
   
## Installation   
Clone the repository to your local machine:   
```
git clone https://github.com/onlydustxyz/starklings.git

```
Then install the tool, run:   
```
curl -L https://raw.githubusercontent.com/onlydustxyz/starklings/master/install.sh | bash

```
## Usage   
Run the tool in watch mode and follow the instructions:   
```
starklings --watch

```
 --- 
## Development   
### Requirements   
- [Python >=3.8 <3.9](https://www.python.org/downloads/)   
   
### Setting up environment   
1. Install Python version management tool: [pyenv](https://github.com/pyenv/pyenv) or [asdf](https://github.com/asdf-vm/asdf)   
2. Install `Python 3.8` using the Python version management tool and activate that version   
3. Clone this repository   
4. Verify the active Python version: `python -V`   
5. Create Python virtual environment in the project directory: `python -m venv env`   
6. Activate environment: `source env/bin/activate`   
7. Upgrade pip: `pip install --upgrade pip`   
8. Install [Poetry](https://python-poetry.org/) — a dependency manager: `pip install poetry`   
9. Install project dependencies: `poetry install`   
 --- 
   
## Inspiration   
- [Protostar](https://github.com/software-mansion/protostar) for all the project tooling and setup, deployment, packaging   
- [Rustlings](https://github.com/rust-lang/rustlings) for the amazing pedagogy and brilliant concept of progressive and interactive tutorial   
