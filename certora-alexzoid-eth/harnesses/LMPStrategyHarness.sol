// SPDX-License-Identifier: UNLICENSED
// Copyright (c) 2023 Tokemak Foundation. All rights reserved.
pragma solidity 0.8.17;

import "../../src/strategy/LMPStrategy.sol";
contract LMPStrategyHarness is LMPStrategy{
    constructor(
        ISystemRegistry _systemRegistry,
        address _lmpVault,
        LMPStrategyConfig.StrategyConfig memory conf
    ) LMPStrategy(_systemRegistry, _lmpVault, conf) {}
    
    function getDestinationSummaryStatsExternal(address destAddress, uint256 price, RebalanceDirection direction, uint256 amount) external returns (IStrategy.SummaryStats memory){
        return getDestinationSummaryStats(destAddress, price, direction, amount);
    }

    function getSwapCostOffsetTightenThresholdInViolations() external returns (uint16){
        return swapCostOffsetTightenThresholdInViolations;
    }

    function getRebalanceValueStatsVars(LMPStrategy.RebalanceValueStats memory stats) external returns (uint256, uint256, uint256, uint256, uint256, uint256) {
        return (stats.inPrice, stats.outPrice, stats.inEthValue, stats.outEthValue, stats.swapCost, stats.slippage);
    }

    function getRebalanceValueStatsHarness(IStrategy.RebalanceParams memory params) external returns (uint256, uint256, uint256, uint256, uint256, uint256) {
        LMPStrategy.RebalanceValueStats memory stats = getRebalanceValueStats(params);
        return (stats.inPrice, stats.outPrice, stats.inEthValue, stats.outEthValue, stats.swapCost, stats.slippage);
    }

    function verifyTrimOperationHarness(IStrategy.RebalanceParams memory params, uint256 trimAmount) external returns (bool) {
        return verifyTrimOperation(params, trimAmount);
    }

    function ensureNotStaleDataHarness(string memory name, uint256 dataTimestamp) external view {
        ensureNotStaleData(name, dataTimestamp);
    }

    function verifyCleanUpOperationHarness(IStrategy.RebalanceParams memory params) external view returns (bool) {
        return verifyCleanUpOperation(params);
    }

    function getDestinationTrimAmountHarness(IDestinationVault dest) external returns (uint256) {
        return getDestinationTrimAmount(dest);
    }
} 