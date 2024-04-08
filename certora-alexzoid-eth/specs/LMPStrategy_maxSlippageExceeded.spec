using BalancerAuraDestinationVault as _BalancerDestVault;
using CurveConvexDestinationVault as _CurveDestVault;
using SystemRegistry as _SystemRegistry;
using ERC20A as _ERC20A;
using ERC20B as _ERC20B;

/////////////////// METHODS ///////////////////////

methods {
    
    // LMPStrategyHarness
    function getDestinationSummaryStatsExternal(address, uint256, LMPStrategy.RebalanceDirection, uint256) 
        external returns (IStrategy.SummaryStats);
    function getSwapCostOffsetTightenThresholdInViolations() external returns (uint16) envfree;
    function getRebalanceValueStatsHarness(IStrategy.RebalanceParams params) external returns (LMPStrategy.RebalanceValueStats);
    // Immutable
    function lmpVault() external returns (address) envfree;
    function pauseRebalancePeriodInDays() external returns (uint16) envfree;
    function maxPremium() external returns (int256) envfree;
    function maxDiscount() external returns (int256) envfree;
    function staleDataToleranceInSeconds() external returns (uint40) envfree;
    function swapCostOffsetInitInDays() external returns (uint16) envfree;
    function swapCostOffsetTightenThresholdInViolations() external returns (uint16) envfree;
    function swapCostOffsetTightenStepInDays() external returns (uint16) envfree;
    function swapCostOffsetRelaxThresholdInDays() external returns (uint16) envfree;
    function swapCostOffsetRelaxStepInDays() external returns (uint16) envfree;
    function swapCostOffsetMaxInDays() external returns (uint16) envfree;
    function swapCostOffsetMinInDays() external returns (uint16) envfree;
    function navLookback1InDays() external returns (uint8) envfree;
    function navLookback2InDays() external returns (uint8) envfree;
    function navLookback3InDays() external returns (uint8) envfree;
    function maxNormalOperationSlippage() external returns (uint256) envfree;
    function maxTrimOperationSlippage() external returns (uint256) envfree;
    function maxEmergencyOperationSlippage() external returns (uint256) envfree;
    function maxShutdownOperationSlippage() external returns (uint256) envfree;
    function maxAllowedDiscount() external returns (int256) envfree;
    function weightBase() external returns (uint256) envfree;
    function weightFee() external returns (uint256) envfree;
    function weightIncentive() external returns (uint256) envfree;
    function weightSlashing() external returns (uint256) envfree;
    function weightPriceDiscountExit() external returns (int256) envfree;
    function weightPriceDiscountEnter() external returns (int256) envfree;
    function weightPricePremium() external returns (int256) envfree;
    function lstPriceGapTolerance() external returns (uint256) envfree;
    // State Variables
    function lastPausedTimestamp() external returns (uint40) envfree;
    function lastAddTimestampByDestination(address destination) external returns (uint40) envfree;
    function violationTrackingState() external returns (uint8, uint8, uint16) envfree;
    //function navTrackingState() external returns (uint8, uint8, uint40, uint256[]) envfree;
    function lastRebalanceTimestamp() external returns (uint40) envfree;
    // Functions 
    function verifyRebalance(IStrategy.RebalanceParams params, IStrategy.SummaryStats outSummary) 
        external returns (bool, string);
    function getRebalanceOutSummaryStats(IStrategy.RebalanceParams rebalanceParams) 
        external returns (IStrategy.SummaryStats);
    function navUpdate(uint256 navPerShare) external;
    function rebalanceSuccessfullyExecuted(IStrategy.RebalanceParams params) external;
    function swapCostOffsetPeriodInDays() external returns (uint16);
    function paused() external returns (bool);
    
    // ILMPVault
    // Summarized instead of linked to help with runtime. 
    // The two state changing functions don't change any relevant state and aren't implemented.
    // The rest of the functions are getters so ghost summary has the same effect as linking.
    function _.addToWithdrawalQueueHead(address) external => NONDET;
    function _.addToWithdrawalQueueTail(address) external => NONDET;
    function _.totalIdle() external => totalIdleCVL expect uint256;
    function _.asset() external => assetCVL expect address;
    function _.totalAssets() external => totalAssetsCVL expect uint256;
    function _.isDestinationRegistered(address dest) external => isDestinationRegisteredCVL[dest] expect bool;
    function _.isDestinationQueuedForRemoval(address dest) external => isDestinationQueuedForRemovalCVL[dest] expect bool;
    function _.getDestinationInfo(address dest) external => getDestinationInfoCVL(calledContract, dest) expect LMPDebt.DestinationInfo;

    // ILMPVault / IDestinationVault
    function _.isShutdown() external => isShutdownCVL(calledContract) expect bool ALL;

    // IDestinationVault
    function _.getStats() external => DISPATCHER(true);
    function _.getValidatedSpotPrice() external => DISPATCHER(true);
    function _.getPool() external => DISPATCHER(true);
    function _.underlying() external => DISPATCHER(true);
    function _.underlyingTokens() external => DISPATCHER(true);
    function _.debtValue(uint256) external => DISPATCHER(true);

    // IRootPriceOracle
    function _.getPriceInEth(address token) external with (env e) 
        => getPriceInEthCVL[token][e.block.timestamp] expect (uint256);
    function _.getSpotPriceInEth(address, address) external => DISPATCHER(true);

    // IDexLSTStats
    function _.current() external => NONDET; // can be dispatched if returned values are important

    // IBalancerComposableStablePool
    function _.getBptIndex() external => ghostGetBptIndexCVL expect (uint256);

    // ISystemRegistry
    function _.accessController() external => DISPATCHER(true); // needed in constructor, rest is handled by linking

    // IIncentivesPricingStats
    function _.getPriceOrZero(address, uint40) external => DISPATCHER(true);

    // ERC20
    function _.name() external => DISPATCHER(true);
    function _.symbol() external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);
    // ERC20's `decimals` summarized as 6, 8 or 18 (ghostValidDecimal), can be changed to ALWAYS(18) for better runtime.
    // This helps with runtime because arbitrary decimal value creates many nonlinear operations.
    function _.decimals() external => ALWAYS(18); // ghostValidDecimal expect uint256; // ghostValidDecimal is 6, 8 or 18 for a better summary
}

///////////////// DEFINITIONS /////////////////////

definition SECONDS_IN_1_DAY() returns mathint = 60 * 60 * 24;

definition MAX_NAV_TRACKING() returns uint8 = require_uint8(91);

definition DISCOUNT_THRESHOLD_ONE() returns mathint = 3 * 10^5; // 3% 1e7 precision, discount required to consider trimming
definition DISCOUNT_DAYS_THRESHOLD() returns mathint = 7; // number of last 10 days that it was >= discountThreshold
definition DISCOUNT_THRESHOLD_TWO() returns mathint = 5 * 10^5; // 5% 1e7 precision, discount required to completely exit

definition ONLY_LMPVAULT_FUNCTIONS(method f) returns bool =
    f.selector == sig:navUpdate(uint256).selector
    || f.selector == sig:rebalanceSuccessfullyExecuted(IStrategy.RebalanceParams).selector;

///////////////// GHOSTS & HOOKS //////////////////

//
// LMPStrategy
//

ghost uint256 ghostGetBptIndexCVL;
ghost uint256 ghostValidDecimal {
    axiom ghostValidDecimal == 6 || ghostValidDecimal == 8 || ghostValidDecimal == 18;
}

ghost mathint ghostTmpCurrentDebt;
ghost mathint ghostTmpDestValueAfterRebalance;
ghost mathint ghostTmpTrimAmount;
ghost mathint ghostTmpLmpAssetsAfterRebalance;

//
// Ghost copy of `LMPStrategy._swapCostOffsetPeriod`
//

ghost uint16 ghostSwapCostOffsetPeriod;

hook Sload uint16 val _swapCostOffsetPeriod {
    require(ghostSwapCostOffsetPeriod == val);
}

hook Sstore _swapCostOffsetPeriod uint16 val {
    ghostSwapCostOffsetPeriod = val;
}

//
// ILMPVault
//

ghost uint256 totalIdleCVL;
ghost address assetCVL;
ghost uint256 totalAssetsCVL;
ghost mapping(address => bool) isDestinationRegisteredCVL;
ghost mapping(address => bool) isDestinationQueuedForRemovalCVL;
ghost bool ghostIsShutdown_LMPVault;

ghost mapping(address => mathint) ghostLMPVaultDestinationInfo_currentDebt;
ghost mapping(address => mathint) ghostLMPVaultDestinationInfo_lastReport;
ghost mapping(address => mathint) ghostLMPVaultDestinationInfo_ownedShares;
ghost mapping(address => mathint) ghostLMPVaultDestinationInfo_debtBasis;

//
// IDestinationVault
//

ghost bool ghostIsShutdown_DestinationVault;

//
// IRootPriceOracle summaries
//

ghost mapping(address => mapping(uint256 => uint256)) getPriceInEthCVL;

////////////////// FUNCTIONS //////////////////////

//
// LMPStrategy
//

// LMPStrategyConfig.validate()
function configValidated() returns bool {
    
    return (swapCostOffsetInitInDays() >= swapCostOffsetMinInDays())
    && (swapCostOffsetInitInDays() <= swapCostOffsetMaxInDays())
    
    && (swapCostOffsetMaxInDays() > swapCostOffsetMinInDays())

    && (navLookback1InDays() < MAX_NAV_TRACKING())
    && (navLookback2InDays() < MAX_NAV_TRACKING())
    && (navLookback3InDays() <= MAX_NAV_TRACKING())

    && (navLookback1InDays() < navLookback2InDays())
    && (navLookback2InDays() < navLookback3InDays())

    && (maxPremium() <= require_int256(10 ^ 18))

    && (maxDiscount() <= require_int256(10 ^ 18))

    && (maxShutdownOperationSlippage() != 0)
    && (maxEmergencyOperationSlippage() != 0)
    && (maxTrimOperationSlippage() != 0)
    && (maxNormalOperationSlippage() != 0)
    && (navLookback1InDays() != 0);
}

function envSafeAssumptions(env e) {
    require(e.block.timestamp > 0 && e.block.timestamp < max_uint40);
}

// State after constructor initialized
function initConstructor(env e) {

    envSafeAssumptions(e);
    
    require(lmpVault() != 0);
    require(configValidated());
    require(lastRebalanceTimestamp() >= require_uint40(e.block.timestamp));
}

//
// ILMPVault
//

function getDestinationInfoCVL(address called, address dest) returns LMPDebt.DestinationInfo {
    LMPDebt.DestinationInfo info;
    if(called == lmpVault()) {
        ghostLMPVaultDestinationInfo_currentDebt[dest] = info.currentDebt;
        ghostLMPVaultDestinationInfo_lastReport[dest] = info.lastReport;
        ghostLMPVaultDestinationInfo_ownedShares[dest] = info.ownedShares;
        ghostLMPVaultDestinationInfo_debtBasis[dest] = info.debtBasis;
    }

    return info;
}

function currentCVL() returns IDexLSTStats.DexLSTStatsData {
    IDexLSTStats.DexLSTStatsData data;
    return data;
}

function isShutdownCVL(address called) returns bool {
    if(called == lmpVault()) {
        return ghostIsShutdown_LMPVault;
    } else {
        return ghostIsShutdown_DestinationVault;
    }
}

///////////////// PROPERTIES //////////////////////

// Ensure that we're not exceeding top-level max slippage
rule verifyRebalance_maxSlippageExceeded(env e, IStrategy.RebalanceParams params, IStrategy.SummaryStats outSummary) {

    initConstructor(e);

    // Skip verifyRebalanceToIdle() branch
    require(_BalancerDestVault != lmpVault());
    require(params.tokenIn == _ERC20A);
    require(params.tokenOut == _ERC20B);
    require(params.destinationIn == _BalancerDestVault);
    require(params.destinationOut == lmpVault());
    require(lmpVault() != _BalancerDestVault);

    mathint inPrice;
    mathint outPrice;
    mathint inEthValue;
    mathint outEthValue;
    mathint swapCost;
    mathint slippage;
    inPrice, outPrice, inEthValue, outEthValue, swapCost, slippage 
        = getRebalanceValueStatsHarness(e, params);

    bool success;
    string message; 
    success, message = verifyRebalance@withrevert(e, params, outSummary);
    bool reverted = lastReverted;

    assert(slippage > to_mathint(maxNormalOperationSlippage()) => reverted);
}
