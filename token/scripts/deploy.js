const hre = require("hardhat");

// Token parameters — override via environment variables at deploy time.
const NAME = process.env.TOKEN_NAME || "MSL Coin";
const SYMBOL = process.env.TOKEN_SYMBOL || "MSL";
// Whole tokens (18 decimals are applied below).
const INITIAL_SUPPLY = process.env.TOKEN_INITIAL_SUPPLY || "1000000";
const CAP = process.env.TOKEN_CAP || "10000000";

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  const owner = process.env.TOKEN_OWNER || deployer.address;

  const initialSupply = hre.ethers.parseUnits(INITIAL_SUPPLY, 18);
  const cap = hre.ethers.parseUnits(CAP, 18);

  console.log(`Deploying ${NAME} (${SYMBOL}) from ${deployer.address}`);
  console.log(`  initial supply: ${INITIAL_SUPPLY}, cap: ${CAP}, owner: ${owner}`);

  const token = await hre.ethers.deployContract("MSLToken", [
    NAME,
    SYMBOL,
    initialSupply,
    cap,
    owner,
  ]);
  await token.waitForDeployment();

  console.log(`MSLToken deployed to: ${await token.getAddress()}`);
  console.log(
    `Verify with:\n  npx hardhat verify --network ${hre.network.name} ` +
      `${await token.getAddress()} "${NAME}" "${SYMBOL}" ${initialSupply} ${cap} ${owner}`
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
