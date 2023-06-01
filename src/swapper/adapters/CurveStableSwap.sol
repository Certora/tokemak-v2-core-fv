// SPDX-License-Identifier: UNLICENSED
// Copyright (c) 2023 Tokemak Foundation. All rights reserved.
pragma solidity 0.8.17;

import { IERC20, SafeERC20 } from "openzeppelin-contracts/token/ERC20/utils/SafeERC20.sol";

import { Errors } from "src/utils/Errors.sol";
import { ICurveStableSwap } from "src/interfaces/external/curve/ICurveStableSwap.sol";
import { ISyncSwapper } from "src/interfaces/swapper/ISyncSwapper.sol";
import { ISwapRouter } from "src/interfaces/swapper/ISwapRouter.sol";
import { BaseAdapter } from "src/swapper/adapters/BaseAdapter.sol";

contract CurveV2Swap is BaseAdapter, ISyncSwapper {
    using SafeERC20 for IERC20;

    error InvalidIndex();

    constructor(address _router) BaseAdapter(_router) { }

    /// @inheritdoc ISyncSwapper
    function validate(address fromAddress, ISwapRouter.SwapData memory swapData) external view override {
        (int128 sellIndex, int128 buyIndex) = abi.decode(swapData.data, (int128, int128));

        ICurveStableSwap pool = ICurveStableSwap(swapData.pool);

        address sellAddress = pool.coins(_int128ToUint256(sellIndex));
        address buyAddress = pool.coins(_int128ToUint256(buyIndex));

        // verify that the fromAddress and toAddress are in the pool
        if (fromAddress != sellAddress) revert DataMismatch("fromAddress");
        if (swapData.token != buyAddress) revert DataMismatch("toAddress");
    }

    /// @inheritdoc ISyncSwapper
    function swap(
        address poolAddress,
        address sellTokenAddress,
        uint256 sellAmount,
        address,
        uint256 minBuyAmount,
        bytes memory data
    ) external override returns (uint256 actualBuyAmount) {
        (int128 sellIndex, int128 buyIndex) = abi.decode(data, (int128, int128));
        ICurveStableSwap pool = ICurveStableSwap(poolAddress);

        IERC20(sellTokenAddress).safeApprove(poolAddress, sellAmount);

        return pool.exchange(sellIndex, buyIndex, sellAmount, minBuyAmount);
    }

    function _int128ToUint256(int128 value) internal pure returns (uint256 result) {
        if (value < 0) {
            revert InvalidIndex();
        }
        //slither-disable-start assembly
        // solhint-disable-next-line no-inline-assembly
        assembly {
            result := value
        }
        //slither-disable-end assembly
    }
}
