// SPDX-License-Identifier: UNLICENSED
// Copyright (c) 2023 Tokemak Foundation. All rights reserved.
pragma solidity 0.8.17;

import "../../src/strategy/LMPStrategy.sol";
contract LMPStrategyHarness is LMPStrategy{
    using SubSaturateMath for uint256;
    using SubSaturateMath for int256;

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

    function tightenSwapCostOffsetExternal() external {
        tightenSwapCostOffset();
    }

    function calculatePriceReturnsExternal(IDexLSTStats.DexLSTStatsData memory stats) external view returns (int256[] memory){
        return super.calculatePriceReturns(stats);
    }
    function validateRebalanceParamsExternal(IStrategy.RebalanceParams memory params) external view {
        super.validateRebalanceParams(params);
    }

    function getLmpVaultAddress() external view returns (address) {
        return address(lmpVault);
    }

    function getLmpTotalIdle() external view returns (uint256) {
        return lmpVault.totalIdle();
    }

    function verifyRebalanceToIdleExternal(IStrategy.RebalanceParams memory params, uint256 slippage) external {
        verifyRebalanceToIdle(params, slippage);
    }

    function getRebalanceValueStatsExternal(IStrategy.RebalanceParams memory params) external returns (RebalanceValueStats memory) {
        return getRebalanceValueStats(params);
    }

    function verifyLSTPriceGapExternal(IStrategy.RebalanceParams memory params, uint256 tolerance) external returns (bool) {
        return verifyLSTPriceGap(params, tolerance);
    }

    function isTooFarAway(uint256 priceSpot, uint256 priceSafe, uint256 tolerance) external returns (bool) {
        if (((priceSafe * 1.0e18 / priceSpot - 1.0e18) * 10_000) / 1.0e18 > tolerance) {
            return true;
        }
        return false;
    }

    function isScenario2Active() external returns (bool) {
        if (lmpVault.isShutdown()) {
            return true;
        }
        return false;
    }

    function isScenario4Active(IStrategy.RebalanceParams memory params) external returns (bool) {
        if (lmpVault.isDestinationQueuedForRemoval(params.destinationOut)) {
            return true;
        }
        return false;
    }

    function getmaxEmergencyOperationSlippage() external returns (uint256) {
        return maxEmergencyOperationSlippage;
    }

    function getmaxShutdownOperationSlippage() external returns (uint256) {
        return maxShutdownOperationSlippage;
    }

    function getmaxNormalOperationSlippage() external returns (uint256) {
        return maxNormalOperationSlippage;
    }

    function getmaxTrimOperationSlippage() external returns (uint256) {
        return maxTrimOperationSlippage;
    }

    function getlastPausedTimestamp() external returns (uint40) {
        return lastPausedTimestamp;
    }

    function getpauseRebalancePeriodInDays() external returns (uint16) {
        return pauseRebalancePeriodInDays;
    }

    function setParam(
        address destinationIn,
        address tokenIn,
        uint256 amountIn,
        address destinationOut,
        address tokenOut,
        uint256 amountOut
    ) external returns (IStrategy.RebalanceParams memory) {
        IStrategy.RebalanceParams memory params;
        params.destinationIn = destinationIn;
        params.tokenIn = tokenIn;
        params.amountIn = amountIn;
        params.destinationOut = destinationOut;
        params.tokenOut = tokenOut;
        params.amountOut = amountOut;
        return params;
    }

    function setValueStatsSlippage(
        uint256 inPrice,
        uint256 outPrice,
        uint256 inEthValue,
        uint256 outEthValue,
        uint256 swapCost,
        uint256 slippage
    ) external returns (RebalanceValueStats memory) {
        RebalanceValueStats memory stats;
        stats.inPrice = inPrice;
        stats.outPrice = outPrice;
        stats.inEthValue = inEthValue;
        stats.outEthValue = outEthValue;
        stats.swapCost = swapCost;
        stats.slippage = slippage;
        return stats;
    }

    function setRebalanceParams(
        address destinationIn,
        address tokenIn,
        uint256 amountIn,
        address destinationOut,
        address tokenOut,
        uint256 amountOut
    ) external returns (IStrategy.RebalanceParams memory) {
        IStrategy.RebalanceParams memory params;
        params.destinationIn = destinationIn;
        params.tokenIn = tokenIn;
        params.amountIn = amountIn;
        params.destinationOut = destinationOut;
        params.tokenOut = tokenOut;
        params.amountOut = amountOut;
        return params;
    }

    function isLessThanEqualSwapCost(
        IStrategy.RebalanceParams memory params,
        IStrategy.SummaryStats memory outSummary
    ) external returns (bool) {
        uint256 swapOffsetPeriod = swapCostOffsetPeriodInDays();
        RebalanceValueStats memory valueStats = getRebalanceValueStats(params);
        IStrategy.SummaryStats memory inSummary = getRebalanceInSummaryStats(params);
        int256 predictedAnnualizedGain = (inSummary.compositeReturn * convertUintToInt(valueStats.inEthValue))
            .subSaturate(outSummary.compositeReturn * convertUintToInt(valueStats.outEthValue)) / 1e18;

        // slither-disable-end divide-before-multiply
        int256 predictedGainAtOffsetEnd = (predictedAnnualizedGain * convertUintToInt(swapOffsetPeriod) / 365);

        // if the predicted gain in Eth by the end of the swap offset period is less than
        // the swap cost then revert b/c the vault will not offset slippage in sufficient time
        // slither-disable-next-line timestamp
        if (predictedGainAtOffsetEnd <= convertUintToInt(valueStats.swapCost)) {
            return true;
        }

        return false;
    }
    
}
