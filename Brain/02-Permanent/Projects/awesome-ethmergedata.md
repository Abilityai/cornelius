---
created: '2026-01-10'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreib3tlph3yxtkc3plnzz2cmpkafj55qh6o57fvgnslokomdb47bvzm
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
local_path: /Users/jlb/Documents/Projects/Inflection/awesome-ethmergedata
status: Done
---
# awesome-ethmergedata   
# awesome-ethmergedata   
*A list of resources for tracking Ethereum data dashboards and tools for monitoring. We take no responsibility for the accuracy of the data published. Be aware of different biases and definitions used across dashboards.*   
## Intro   
With the Merge going through successfully, Ethereum has changed permanently. If you are not familiar with the details, [here’s a good primer](https://coinmetrics.io/special-insights/ethereum-merge/). The new process for adding transactions to the chain has significant trade-offs with respect to [economics](http://ultrasound.money), [energy usage](https://ethereum.org/en/energy-consumption/), [MEV](https://github.com/flashbots/eth2-research), [censorship](https://notes.ethereum.org/@vbuterin/pbs_censorship_resistance)-[resistance](https://github.com/flashbots/mev-boost/issues/215), security and [centralization](https://noxx.substack.com/p/order-flows-kingmaker-of-the-block).   
The data is crucial to monitor, track and interpret progress of these dimensions. This post intends to provide a coherent library of twitter accounts, dashboards, data tools and other lists. We will do our best to keep it up to date, although this space moves very quickly.   
If you have feedback, additions or questions, please make a pull request! Feel free to [[Twitter.Com/Mountbranch]] on twitter if I'm not fast enough to approve. All help to keep this up-to-date is appreciated.   
## Glossary   
### Types   
There are five types of resources:   
1. **Twitter accounts** to follow to understand the space (excl. accounts of the dashboards), e.g., [[Twitter.Com/Blink_Labs_Xyz]]   
2. **Dashboards** of live data, e.g., [ultrasound.money](http://ultrasound.money)   
3. **Repos** of tools you can use to extract data yourself   
4. **Meta-lists** which are lists in themselves   
5. **Raw-data** which are API's or published raw data   
   
### Coverage   
The resources cover different categories of data. For ease of use, the resources are classified according to what they are focused on.   
**Blocks**: blocks built, proposed and finalized   
**Builder**: proposes blocks to validators, through relays   
**Burn**: Eth reduction of supply through fee burn due to EIP-1559   
**MEV**: Maximal extractable value   
**MEV-Boost**: Intermediate design towards full PBS, proposed by Flashbots   
**Validator**: Consensus participant   
**Relay**: Relays blocks from builders to validators   
**Rewards**: Eth earned of different participants   
**Supply**: Amount of eth in circulation and staked   
## Twitter-accounts   
|                                                                   |                                                                          |                                    |                                                                                    |    Affiliation |
|:------------------------------------------------------------------|:-------------------------------------------------------------------------|:-----------------------------------|:-----------------------------------------------------------------------------------|:---------------|
|        EthStakerBot tweeting high proposer payments to validators | [Link](https://twitter.com/mevproposerbot?s=21&t=xgb8KRm9heGyFERearZuKQ) |                 MEV-boost, Rewards |     In the last week (28.09-05.10) the highest payment to validator was 30.896 ETH |       Personal |
|                                            Tweets big MEV rewards |                                  [Link](https://twitter.com/MevBoostBot) |                       MEV, Rewards |                                      8 ETH paid out in miner rewards in one bundle |              ? |
|                         EF guy and definer of relay monitor specs |                                  [Link](https://twitter.com/ralexstokes) |                   MEV-boost, Relay |            [Nice post](https://twitter.com/ralexstokes/status/1573314707586686976) |             EF |
|                                                     BloXroute COO |                                   [Link](https://twitter.com/eyalmarkov) | Builder, Relay, Rewards, Validator |             [Nice post](https://twitter.com/eyalmarkov/status/1572616363054612486) |      BloXroute |
|                Co-founder of Prysm labs and builder of Eth client |                                 [Link](https://twitter.com/terencechain) |                  Blocks, Validator |               [Nice thing he linked to](https://github.com/rated-network/eth2REKT) | Prysmatic labs |
| Data analysts highlighting  findings on block builders and others |                               [Link](https://twitter.com/blink_labs_xyz) |          Builder, Relay, Validator | [Nice post](https://twitter.com/blink_labs_xyz/status/1572687125136678912/photo/1) |     Blink Labs |

## Dashboards   
|                                                                                                                  |                                                                                                                 |                                               |                                                                                                                                                                                                    |             Affiliation |
|:-----------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|:----------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------|
|                                                                                 Mainnet MEV-Boost relay overview |                                                                      [Link](https://boost-relay.flashbots.net/) |  Blocks, MEV-boost, Relay, Rewards, Validator |                                                                                                                                                                                                    |               Flashbots |
|                                                                    Flashbots MEV-Boost Relay and Builder Metrics |                                                                     [Link](https://transparency.flashbots.net/) | Builder, MEV-boost, Relay, Rewards, Validator | -A cumulative total of 2,823ETH was earned so far by FB Eth validators post merge -FB MEV-Boost validators receive consistently ~10x block rewards vs. others -41% of all validators run MEV-boost |               Flashbots |
|                                                                          MEV explorer by tx hash or block number |                                                                             [Link](https://mev.metablock.dev/1) |                    Blocks, Fees, MEV, Rewards |                                       Not yet open-source, but alternative block explorers help us create new mental models for chains. Leaderboard of top searchers. Done by https://destiner.io/ |               Metablock |
|                                                                                   Beacon chain validator ratings |                                                                              [Link](https://www.rated.network/) |                                     Validator |                                             [Staking facilities](https://www.rated.network/o/Staking%20Facilities) have earned 839ETH and accrued 26ETH penalties as part of the Lido Pool to date |                   Rated |
|                                                                          Open source block explorer for Ethereum |                                                                                   [Link](https://beaconcha.in/) |                             Blocks, Validator |                                                                                                                         Last [slashing](https://beaconcha.in/validators/slashings) was 39 days ago |             Bitfly GmbH |
|                                                                                   Inspect bundle rewards and txs |                                                                   [Link](https://flashbots-explorer.marto.lol/) |                            MEV-boost, Rewards |                                                                                                                                               https://flashbots-explorer.marto.lol/?block=15619978 | Marto from OpenZeppelin |
|                                                                                      Queryable relayer dashboard | [Link](https://datastudio.google.com/u/0/reporting/31ab41de-a800-4b54-b57c-bb0724ec2a5f/page/Gg3?s=tPvjg-qqrC0) |                        Blocks, Relay, Rewards |                                                                                                                                  9 blocks provided by FB relay were ignored in the last day (26/9) |                Personal |
|                                                                                             Zeromev MEV explorer |                                                                                [Link](https://www.zeromev.org/) |                                MEV, MEV-boost |                                                                                                                                      Frontrunning caused $3,462.20 in user losses in the last hour |                 Zeromev |
|                                                                  Dune dashboard from Chainsight Analytics on MEV |                                           [Link](https://dune.com/ChainsightAnalytics/mev-after-ethereum-merge) |                            Builder, MEV-boost |                                                                                                                                          FB block builders have a far superior success rate of 67% |    Chainsight analytics |
|                                                 Tracking https://boost.flashbots.net/ relays and block builders. |                                                                               [Link](https://www.mevboost.org/) |                     Builder, MEV-boost, Relay |                                                                                                                                              83% of all MEV-Boost blocks are relayed via Flashbots |  Independent researcher |
|                                                                                     Flashbots Boost Relay status |                                                   [Link](https://0xpanoramix.github.io/flashbots-boost-status/) |                              MEV-boost, Relay |                                                                                                                                                                   Mainnet uptime was 99.88% so far |                    Kiln |
| Shows how eth is becoming [ultrasound](https://www.youtube.com/watch?v=47Z4ZpBiTwA&t=1770s) and not inflationary |                                                                               [Link](https://ultrasound.money/) |                  Burn, Supply, TVS, Validator |                                                  Supply and burn rates are fundamental economic metrics: -0.62 ETH are being burnt every minute (7d avg.) and the issuance offset is only at 0.54x |              Ultrasound |

## Repos   
|                                                                                                        |                                                     |                                |                                                                                                           | Affiliation |
|:-------------------------------------------------------------------------------------------------------|:----------------------------------------------------|:-------------------------------|:----------------------------------------------------------------------------------------------------------|:------------|
|                                                                               Exploring MEV post-merge |  [Link](https://github.com/flashbots/eth2-research) | Builder, MEV, Relay, Validator | With less than 200k validators, base rewards with MEV are worth more missing the headers not, without MEV |   Flashbots |
|       [MEV](https://ethereum.org/en/developers/docs/mev/)-inspector for Ethereum to illuminate the [🌲💡 | [Link](https://github.com/flashbots/mev-inspect-py) |                            MEV |                                          Need to test myself but was too lazy to spin up a cluster so far |   Flashbots |
|                                   Compares value delivered to proposers vs. bids from MEV-boost relays |  [Link](https://github.com/dvush/check-relay-value) |      MEV-boost, Relay, Rewards |                                                                            Makes MEV earnings transparent |    Personal |

## Meta-list   
|                                                                            |                                                                                   |                |                                                                                                                                                         |      Affiliation |
|:---------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
| Compendium of resources for Ethereum, but also other EVM chains and cosmos |       [Link](https://www.notion.so/Fees-Gas-MEV-3f79599cee774d70999ce69fddcec364) | Fees, Gas, MEV |                                                                                     Some overlap with this database, but with focus on gas fees and MEV | Sovereign Signal |
|                                                     Relay list for Mainnet | [Link](https://research.lido.fi/t/lido-on-ethereum-call-for-relay-providers/2844) |          Relay |                       Open call for relays from Lido. Only Flashbots, Bloxroute, Blocknative, Manifold and Eden responded and are running relays so far |             Lido |
|                                                     Relay list for Mainnet |          [Link](https://github.com/remyroy/ethstaker/blob/main/MEV-relay-list.md) |          Relay | Only 6 mainnet Relays are listed today, of which 2 are run by the same actor. Relays are critical infrastructure and have the power to break the system |        EthStaker |

## Raw-data   
|                                  |                                                                               |                                                         |                                                                         | Affiliation |
|:---------------------------------|:------------------------------------------------------------------------------|:--------------------------------------------------------|:------------------------------------------------------------------------|:------------|
| Full data dump from the FB relay | [Link](https://boost-relay-data-public.s3.us-east-2.amazonaws.com/index.html) | Blocks, Fees, Gas, MEV-boost, Relay, Rewards, Validator | No need to crawl the API anymore, just download raw data in a CSV/JSON! |   Flashbots |

### Thanks to everyone who keeps putting out amazing data-resources!   
