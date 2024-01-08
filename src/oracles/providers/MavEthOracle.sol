// SPDX-License-Identifier: UNLICENSED
// Copyright (c) 2023 Tokemak Foundation. All rights reserved.

pragma solidity 0.8.17;

import { IPool } from "src/interfaces/external/maverick/IPool.sol";
import { IPoolPositionDynamicSlim } from "src/interfaces/external/maverick/IPoolPositionDynamicSlim.sol";
import { Errors } from "src/utils/Errors.sol";
import { IPriceOracle } from "src/interfaces/oracles/IPriceOracle.sol";
import { ISpotPriceOracle } from "src/interfaces/oracles/ISpotPriceOracle.sol";
import { IRootPriceOracle } from "src/interfaces/oracles/IRootPriceOracle.sol";
import { ISystemRegistry } from "src/interfaces/ISystemRegistry.sol";
import { SecurityBase } from "src/security/SecurityBase.sol";
import { SystemComponent } from "src/SystemComponent.sol";
import { IPoolInformation } from "src/interfaces/external/maverick/IPoolInformation.sol";

contract MavEthOracle is SystemComponent, IPriceOracle, SecurityBase, ISpotPriceOracle {
    /// @notice Emitted when new maximum bin width is set.
    event MaxTotalBinWidthSet(uint256 newMaxBinWidth);

    /// @notice Emitted when Maverick PoolInformation contract is set.
    event PoolInformationSet(address poolInformation);

    /// @notice Thrown when the total width of all bins being priced exceeds the max.
    error TotalBinWidthExceedsMax();

    /// @notice Thrown when token is not in pool.
    error InvalidToken();

    // 100 = 1% spacing, 10 = .1% spacing, 1 = .01% spacing etc.
    uint256 public maxTotalBinWidth = 50;

    /// @notice The PoolInformation Maverick contract.
    IPoolInformation public poolInformation;

    constructor(ISystemRegistry _systemRegistry)
        SystemComponent(_systemRegistry)
        SecurityBase(address(_systemRegistry.accessController()))
    {
        Errors.verifyNotZero(address(_systemRegistry.rootPriceOracle()), "priceOracle");
    }

    /**
     * @notice Gives ability to set total bin width to system owner.
     * @param _maxTotalBinWidth New max bin width.
     */
    function setMaxTotalBinWidth(uint256 _maxTotalBinWidth) external onlyOwner {
        Errors.verifyNotZero(_maxTotalBinWidth, "_maxTotalbinWidth");
        maxTotalBinWidth = _maxTotalBinWidth;

        emit MaxTotalBinWidthSet(_maxTotalBinWidth);
    }

    function setPoolInformation(address _poolInformation) external onlyOwner {
        Errors.verifyNotZero(_poolInformation, "_poolInformation");
        poolInformation = IPoolInformation(_poolInformation);

        emit PoolInformationSet(_poolInformation);
    }

    /// @inheritdoc IPriceOracle
    function getPriceInEth(address _boostedPosition) external returns (uint256) {
        // slither-disable-start similar-names
        Errors.verifyNotZero(_boostedPosition, "_boostedPosition");

        IPoolPositionDynamicSlim boostedPosition = IPoolPositionDynamicSlim(_boostedPosition);
        IPool pool = IPool(boostedPosition.pool());

        Errors.verifyNotZero(address(pool), "pool");

        // Check that total width of all bins in position does not exceed what we deem safe.
        if (pool.tickSpacing() * boostedPosition.allBinIds().length > maxTotalBinWidth) {
            revert TotalBinWidthExceedsMax();
        }

        // Get reserves in boosted position.
        (uint256 reserveTokenA, uint256 reserveTokenB) = boostedPosition.getReserves();

        // Get total supply of lp tokens from boosted position.
        uint256 boostedPositionTotalSupply = boostedPosition.totalSupply();

        IRootPriceOracle rootPriceOracle = systemRegistry.rootPriceOracle();

        // Price pool tokens.
        uint256 priceInEthTokenA = rootPriceOracle.getPriceInEth(address(pool.tokenA()));
        uint256 priceInEthTokenB = rootPriceOracle.getPriceInEth(address(pool.tokenB()));

        // Calculate total value of each token in boosted position.
        uint256 totalBoostedPositionValueTokenA = reserveTokenA * priceInEthTokenA;
        uint256 totalBoostedPositionValueTokenB = reserveTokenB * priceInEthTokenB;

        // Return price of lp token in boosted position.
        return (totalBoostedPositionValueTokenA + totalBoostedPositionValueTokenB) / boostedPositionTotalSupply;
        // slither-disable-end similar-names
    }

    /// @inheritdoc ISpotPriceOracle
    /// @dev This function gets price using Maverick's `PoolInformation` contract.
    function getSpotPrice(
        address token,
        address poolAddress,
        address
    ) public returns (uint256 price, address actualQuoteToken) {
        IPool pool = IPool(poolAddress);
        address tokenA = address(pool.tokenA());
        actualQuoteToken = address(pool.tokenB());

        bool tokenAIn = token == tokenA;
        if (!tokenAIn && token != actualQuoteToken) revert InvalidToken();

        price = poolInformation.calculateSwap(
            pool,
            uint128(1e18), // amount
            tokenAIn,
            false, // exactOutput
            0 // sqrtPriceLimit
        );
    }
}
