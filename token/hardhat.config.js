require("@nomicfoundation/hardhat-toolbox");
const { subtask } = require("hardhat/config");
const {
  TASK_COMPILE_SOLIDITY_GET_SOLC_BUILD,
} = require("hardhat/builtin-tasks/task-names");

// Use the solc compiler bundled with the npm "solc" package instead of
// downloading binaries from binaries.soliditylang.org — keeps compilation
// hermetic and working in restricted-network environments.
subtask(TASK_COMPILE_SOLIDITY_GET_SOLC_BUILD, async (args, hre, runSuper) => {
  const solcPackage = require("solc/package.json");
  if (args.solcVersion === solcPackage.version.split("+")[0]) {
    return {
      compilerPath: require.resolve("solc/soljson.js"),
      isSolcJs: true,
      version: args.solcVersion,
      longVersion: solcPackage.version,
    };
  }
  return runSuper(args);
});

// Real network credentials come from environment variables (never commit them):
//   SEPOLIA_RPC_URL / MAINNET_RPC_URL — RPC endpoint (Alchemy, Infura, ...)
//   PRIVATE_KEY                       — deployer wallet private key
//   ETHERSCAN_API_KEY                 — for contract verification
const { SEPOLIA_RPC_URL, MAINNET_RPC_URL, PRIVATE_KEY, ETHERSCAN_API_KEY } =
  process.env;

const accounts = PRIVATE_KEY ? [PRIVATE_KEY] : [];

module.exports = {
  solidity: {
    version: "0.8.28",
    settings: {
      optimizer: { enabled: true, runs: 200 },
      evmVersion: "cancun",
    },
  },
  networks: {
    sepolia: {
      url: SEPOLIA_RPC_URL || "",
      accounts,
    },
    mainnet: {
      url: MAINNET_RPC_URL || "",
      accounts,
    },
  },
  etherscan: {
    apiKey: ETHERSCAN_API_KEY || "",
  },
};
