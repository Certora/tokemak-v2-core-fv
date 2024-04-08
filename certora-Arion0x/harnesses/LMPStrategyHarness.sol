// SPDX-License-Identifier: UNLICENSED
// Copyright (c) 2023 Tokemak Foundation. All rights reserved.
pragma solidity 0.8.17;

import "../../src/strategy/LMPStrategy.sol";

contract LMPStrategyHarness is LMPStrategy {
	constructor(
		ISystemRegistry _systemRegistry,
		address _lmpVault,
		LMPStrategyConfig.StrategyConfig memory conf
	) LMPStrategy(_systemRegistry, _lmpVault, conf) {}

	function getDestinationSummaryStatsExternal(
		address destAddress,
		uint256 price,
		RebalanceDirection direction,
		uint256 amount
	) external returns (IStrategy.SummaryStats memory) {
		return getDestinationSummaryStats(destAddress, price, direction, amount);
	}

	function getRebalanceValueStatsExternal(
		IStrategy.RebalanceParams memory params
	) external returns (RebalanceValueStats memory) {
		return getRebalanceValueStats(params);
	}
	function getRebalanceInSummaryStatsExternal(
		IStrategy.RebalanceParams memory params
	)external returns (IStrategy.SummaryStats memory){
		return getRebalanceInSummaryStats(params);
	}

	function getSwapCostOffsetTightenThresholdInViolations() external returns (uint16) {
		return swapCostOffsetTightenThresholdInViolations;
	}

	function calculatePercentageBetweenSpotAndSafe(
		uint256 priceSafe,
		uint256 priceSpot
	) external returns (uint256 percentage) {
		percentage = (((priceSafe * 1.0e18) / priceSpot - 1.0e18) * 10_000) / 1.0e18;
	}
	function castToVault(address dest)external returns (IDestinationVault vault){
		return IDestinationVault(dest);
	}

	// function clearExpiredPauseExternal() external returns (bool result) {
	// 	result = clearExpiredPause();
	// }
}
