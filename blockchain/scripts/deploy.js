const hre = require("hardhat");

async function main() {
  const SecureMessaging = await hre.ethers.getContractFactory("SecureMessaging");
  const contract = await SecureMessaging.deploy();

  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("SecureMessaging deployed to:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
