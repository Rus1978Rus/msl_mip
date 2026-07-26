const { expect } = require("chai");
const { ethers } = require("hardhat");
const {
  loadFixture,
} = require("@nomicfoundation/hardhat-toolbox/network-helpers");

const NAME = "MSL Coin";
const SYMBOL = "MSL";
const INITIAL_SUPPLY = ethers.parseUnits("1000000", 18);
const CAP = ethers.parseUnits("10000000", 18);

describe("MSLToken", function () {
  async function deployFixture() {
    const [owner, alice, bob] = await ethers.getSigners();
    const token = await ethers.deployContract("MSLToken", [
      NAME,
      SYMBOL,
      INITIAL_SUPPLY,
      CAP,
      owner.address,
    ]);
    return { token, owner, alice, bob };
  }

  describe("deployment", function () {
    it("sets name, symbol and decimals", async function () {
      const { token } = await loadFixture(deployFixture);
      expect(await token.name()).to.equal(NAME);
      expect(await token.symbol()).to.equal(SYMBOL);
      expect(await token.decimals()).to.equal(18);
    });

    it("mints the initial supply to the owner", async function () {
      const { token, owner } = await loadFixture(deployFixture);
      expect(await token.totalSupply()).to.equal(INITIAL_SUPPLY);
      expect(await token.balanceOf(owner.address)).to.equal(INITIAL_SUPPLY);
    });

    it("exposes the cap", async function () {
      const { token } = await loadFixture(deployFixture);
      expect(await token.cap()).to.equal(CAP);
    });

    it("rejects an initial supply above the cap", async function () {
      const [owner] = await ethers.getSigners();
      const factory = await ethers.getContractFactory("MSLToken");
      await expect(
        ethers.deployContract("MSLToken", [
          NAME,
          SYMBOL,
          CAP + 1n,
          CAP,
          owner.address,
        ])
      ).to.be.revertedWithCustomError(factory, "ERC20ExceededCap");
    });
  });

  describe("transfers", function () {
    it("transfers between accounts", async function () {
      const { token, owner, alice } = await loadFixture(deployFixture);
      const amount = ethers.parseUnits("100", 18);
      await expect(
        token.connect(owner).transfer(alice.address, amount)
      ).to.changeTokenBalances(token, [owner, alice], [-amount, amount]);
    });

    it("reverts on insufficient balance", async function () {
      const { token, alice, bob } = await loadFixture(deployFixture);
      await expect(
        token.connect(alice).transfer(bob.address, 1n)
      ).to.be.revertedWithCustomError(token, "ERC20InsufficientBalance");
    });
  });

  describe("minting", function () {
    it("lets the owner mint up to the cap", async function () {
      const { token, owner, alice } = await loadFixture(deployFixture);
      const amount = CAP - INITIAL_SUPPLY;
      await token.connect(owner).mint(alice.address, amount);
      expect(await token.totalSupply()).to.equal(CAP);
      expect(await token.balanceOf(alice.address)).to.equal(amount);
    });

    it("reverts when minting above the cap", async function () {
      const { token, owner, alice } = await loadFixture(deployFixture);
      const amount = CAP - INITIAL_SUPPLY + 1n;
      await expect(
        token.connect(owner).mint(alice.address, amount)
      ).to.be.revertedWithCustomError(token, "ERC20ExceededCap");
    });

    it("reverts when a non-owner mints", async function () {
      const { token, alice } = await loadFixture(deployFixture);
      await expect(
        token.connect(alice).mint(alice.address, 1n)
      ).to.be.revertedWithCustomError(token, "OwnableUnauthorizedAccount");
    });
  });

  describe("burning", function () {
    it("lets a holder burn their tokens", async function () {
      const { token, owner } = await loadFixture(deployFixture);
      const amount = ethers.parseUnits("1000", 18);
      await token.connect(owner).burn(amount);
      expect(await token.totalSupply()).to.equal(INITIAL_SUPPLY - amount);
    });

    it("frees cap room for future mints", async function () {
      const { token, owner, alice } = await loadFixture(deployFixture);
      await token.connect(owner).mint(alice.address, CAP - INITIAL_SUPPLY);
      await token.connect(alice).burn(ethers.parseUnits("5", 18));
      await token
        .connect(owner)
        .mint(alice.address, ethers.parseUnits("5", 18));
      expect(await token.totalSupply()).to.equal(CAP);
    });
  });

  describe("ownership", function () {
    it("transfers ownership", async function () {
      const { token, owner, alice } = await loadFixture(deployFixture);
      await token.connect(owner).transferOwnership(alice.address);
      expect(await token.owner()).to.equal(alice.address);
      await token.connect(alice).mint(alice.address, 1n);
    });
  });

  describe("permit (ERC-2612)", function () {
    it("approves via signature without a transaction from the holder", async function () {
      const { token, owner, alice } = await loadFixture(deployFixture);
      const amount = ethers.parseUnits("42", 18);
      const deadline = (await ethers.provider.getBlock("latest")).timestamp + 3600;
      const nonce = await token.nonces(owner.address);

      const domain = {
        name: NAME,
        version: "1",
        chainId: (await ethers.provider.getNetwork()).chainId,
        verifyingContract: await token.getAddress(),
      };
      const types = {
        Permit: [
          { name: "owner", type: "address" },
          { name: "spender", type: "address" },
          { name: "value", type: "uint256" },
          { name: "nonce", type: "uint256" },
          { name: "deadline", type: "uint256" },
        ],
      };
      const values = {
        owner: owner.address,
        spender: alice.address,
        value: amount,
        nonce,
        deadline,
      };

      const signature = await owner.signTypedData(domain, types, values);
      const { v, r, s } = ethers.Signature.from(signature);

      await token
        .connect(alice)
        .permit(owner.address, alice.address, amount, deadline, v, r, s);
      expect(await token.allowance(owner.address, alice.address)).to.equal(
        amount
      );
    });
  });
});
