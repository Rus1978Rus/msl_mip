// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {ERC20Capped} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";
import {ERC20Permit} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @title MSLToken — ERC-20 token with capped supply, burn and permit
/// @notice Name, symbol, initial supply, hard cap and owner are set once at
///         deployment via constructor arguments; nothing is hard-coded.
///         The owner can mint new tokens but never above the cap. Any holder
///         can burn their own tokens. ERC-2612 permit enables gasless approvals.
contract MSLToken is ERC20, ERC20Burnable, ERC20Capped, ERC20Permit, Ownable {
    constructor(
        string memory name_,
        string memory symbol_,
        uint256 initialSupply,
        uint256 cap_,
        address owner_
    )
        ERC20(name_, symbol_)
        ERC20Capped(cap_)
        ERC20Permit(name_)
        Ownable(owner_)
    {
        _mint(owner_, initialSupply);
    }

    /// @notice Mint new tokens, owner only. Reverts above the cap.
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    // ERC20Capped enforces the cap inside _update; both parents must be linearized.
    function _update(
        address from,
        address to,
        uint256 value
    ) internal override(ERC20, ERC20Capped) {
        super._update(from, to, value);
    }
}
