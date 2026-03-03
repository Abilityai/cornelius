---
created: '2024-04-10'
updated: '2026-03-03'
tags:
- anytype-import
- note
type: permanent
source_type: note
anytype_id: bafyreif7c5s5gf3i22doa3y4j7ccbbltr2m5ymnmzuibc2aqaw6yf4y45q
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
---
# ZKSummit   
   
## Talk - Justin Drake, ZKASIC   
- ZKASICs are about reducing latency, should be in check with slot finality on L2s/rollups   
- three use cases:   
    1. "within blow atomic cross-chain transactions requires real-time proving; 12s slot {1s proving latency+11s synchrony window for execution)   
    2. Light validators that can run on the edge, clients will snarkify (zkGeth/zkreth/…)   
    3. EVM-in-EVM precompiles - native rollups   
- Builders are incentivized to do faster and faster proving, more txs/more blocks/bigger blocks so more MEV   
- ZKASIC builders - Accseal, cysic, fabric   
- POW miners coming in to the game (bitmain and co)   
- Auradine, Ingonyama, suprenational → not working on asics now, but might in the future   
   
   
Accseal chip:    
- 12nm node, die area 100mm2   
- MSM/NTT/vADD vMUL   
- up to 384 bits   
- Somewhat programmable   
- Test board - lower cost than Cysic/Ingonyama/ZPrize GPUU   
   
   
Fabric is the most ambitious   
   
Cysic can do MSM BN254 at 195ms for deg 30   
 --- 
## Talk - Jim Posen (Ulvetanna) on Binius   
HW co-design rather than HW design and SW design separately - holistic view of system   
   
Why binary fields:   
- Efficient arithmetic   
- Efficient arithmetization   
   
   
Binius:   
- Arithmetization of towers of binary fields   
- multilinear poly IOP based on hyperplonk   
- Eliminated embedding overhead on BRakedown and FRI commitments   
   
   
   
# Insights   
- Two days:    
    1. ZKSummit around general zero-knowledge    
    2. ZKAccelerate (hosted by Ingonyama) around how to speed up ZKPs   
- Relatively small number of people, but with relatively new faces. Distinctly different crowd from other blockchain conferences, way more focused and technical discussions   
- A lot of corporate research and engineering advances improving the practicality of usage of snarks   
- Only blockchain related settings and companies   
- Almost no privacy-focused applications or talks, probably due to the uncertainty in Europe related to Tornado Cash and Alexey Pertsev   
   
   
## **Interesting conversations**   
- Elad:   
    - He's been pushing for this space for 10y but haven't found anything worth investing in yet besides ZAMA
    -

## Related
- [[Future of computing]] - ZK hardware as the next computing S-curve
