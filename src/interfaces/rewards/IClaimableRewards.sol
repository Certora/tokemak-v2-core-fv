// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;

import { IERC20 } from "openzeppelin-contracts/token/ERC20/IERC20.sol";

interface IClaimableRewards {
    error ClaimRewardsFailed();
    error TokenAddressZero();

    event RewardsClaimed(IERC20[], uint256[]);
}