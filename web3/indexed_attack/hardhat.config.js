require("@nomiclabs/hardhat-ethers");

module.exports = {
  solidity: "0.6.10",
  networks: {
    hardhat: {
      chainId: 1,
      forking: {
        url: "https://eth-mainnet.alchemyapi.io/v2/<your-key>",
        
        blockNumber: 13417948 // The block before Indexed attack.
        // lastReweigh=1633607810, reweighIndex=23
      },
    }
  }
};