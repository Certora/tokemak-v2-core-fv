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

use builtin rule sanity;

// Offset period must be between swapCostOffsetMaxInDays and swapCostOffsetMinInDays.
invariant offsetIsInBetween()
    ghostSwapCostOffsetPeriod <= swapCostOffsetMaxInDays() && ghostSwapCostOffsetPeriod >= swapCostOffsetMinInDays() {
    preserved with(env e) {
        initConstructor(e);
    }
}

// lastPausedTimestamp() always less or equal block timestamp
invariant lastPausedTimestampLEqBlockTimestamp(env e) lastPausedTimestamp() <= require_uint40(e.block.timestamp);

// For any registered destination must not be in the future relative to the current block timestamp
invariant lastAddTimestampByDestination_notInTheFuture(env e, address destination) 
    lastAddTimestampByDestination(destination) <= require_uint40(e.block.timestamp) {
    preserved with (env eInv) {
        require(require_uint40(e.block.timestamp) == require_uint40(eInv.block.timestamp));
        envSafeAssumptions(e);
    }
}

// Constructor
invariant constructorInitialized(env eInv) lmpVault() != 0 
        && configValidated() 
        && ghostSwapCostOffsetPeriod == swapCostOffsetInitInDays()
    filtered { f -> f.selector == 0 } {
    preserved with (env eFunc) {
        envSafeAssumptions(eFunc);
        require(false);
    }
}

// `violationTrackingState.violationCount` must not be increased by more than 1
rule cantJumpTwoViolationsAtOnce(env e, method f) {

    initConstructor(e);

    uint16 numOfViolationsBefore;
    numOfViolationsBefore,_,_ = violationTrackingState();

    calldataarg args;
    f(e, args);

    uint16 numOfViolationsAfter;
    numOfViolationsAfter,_,_ = violationTrackingState();

    assert numOfViolationsAfter - numOfViolationsBefore <= 1;
}

// Only LMPVault can execute specific functions
rule onlyLMPVault(env e, method f, calldataarg args) 
    filtered { f -> ONLY_LMPVAULT_FUNCTIONS(f) } {

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(e.msg.sender != lmpVault() => reverted);
}

// lastPausedTimestamp() variable transition
rule lastPausedTimestampTransition(env e, method f, calldataarg args) 
    filtered { f -> f.selector == sig:navUpdate(uint256).selector 
        || f.selector == sig:rebalanceSuccessfullyExecuted(IStrategy.RebalanceParams).selector } {

    uint40 before = lastPausedTimestamp();

    f(e, args);

    uint40 after = lastPausedTimestamp();

    assert(before != after => after == 0 || after == require_uint40(e.block.timestamp));
}

// Params should be validated in verifyRebalance() (destinationIn and destinationOut are not equal to LmpVault)
rule verifyRebalanceParamsValidate_destinationInNeqLmpVault(env e, IStrategy.RebalanceParams params, IStrategy.SummaryStats outSummary) {

    initConstructor(e);

    require(lmpVault() != params.destinationIn);
    require(params.destinationIn == _BalancerDestVault);

    bool validParams = params.tokenIn == _BalancerDestVault.underlying(e);

    verifyRebalance@withrevert(e, params, outSummary);
    bool reverted = lastReverted;

    assert(!validParams => reverted);
}

rule verifyRebalanceParamsValidate_destinationOutNeqLmpVault(env e, IStrategy.RebalanceParams params, IStrategy.SummaryStats outSummary) {

    initConstructor(e);

    require(lmpVault() != params.destinationOut);
    require(params.destinationOut == _BalancerDestVault);

    bool validParams = params.tokenOut == _BalancerDestVault.underlying(e) 
        && params.amountOut <= _BalancerDestVault.balanceOf(e, lmpVault());

    verifyRebalance@withrevert(e, params, outSummary);
    bool reverted = lastReverted;

    assert(!validParams => reverted);
}

// lastRebalanceTimestamp() variable transition
rule lastRebalanceTimestampTransition(env e, method f, calldataarg args) 
    filtered { f -> f.selector == sig:rebalanceSuccessfullyExecuted(IStrategy.RebalanceParams).selector } {

    uint40 before = lastRebalanceTimestamp();

    f(e, args);

    uint40 after = lastRebalanceTimestamp();

    assert(before != after => after == require_uint40(e.block.timestamp));
}

// verifyRebalance() reverted when paused
rule verifyRebalanceNotPaused(env e, IStrategy.RebalanceParams params, IStrategy.SummaryStats outSummary) {

    initConstructor(e);
    requireInvariant lastPausedTimestampLEqBlockTimestamp(e);
    require(pauseRebalancePeriodInDays() != 0);

    // Rebalances back to idle are allowed even when a strategy is paused
    require(params.destinationIn != lmpVault());

    bool paused = lastPausedTimestamp() != 0 
        ? (to_mathint(require_uint40(e.block.timestamp) - lastPausedTimestamp()) 
            <= to_mathint(pauseRebalancePeriodInDays() * SECONDS_IN_1_DAY()))
        : false;
 
    verifyRebalance@withrevert(e, params, outSummary);
    bool reverted = lastReverted;

    assert(paused => reverted);
}

// navUpdate() clears pause state
rule navUpdate_clearPauseState(env e, calldataarg args) {

    uint16 swapCostOffsetPeriodBefore = ghostSwapCostOffsetPeriod;

    bool isExpiredPauseState = lastPausedTimestamp() > 0 && !paused(e);

    navUpdate(e, args);

    uint16 swapCostOffsetPeriodAfter = ghostSwapCostOffsetPeriod;

    assert(!isExpiredPauseState 
        ? swapCostOffsetPeriodBefore == swapCostOffsetPeriodAfter
        : swapCostOffsetPeriodAfter == swapCostOffsetMinInDays() && lastPausedTimestamp() == 0
        );
}

// IStrategy.RebalanceParams

function initRebalanceParamsCVL(env e, IStrategy.RebalanceParams params) {

    // Require validateRebalanceParams() check passed
    require(validRebalanceParamsCVL(e, params));

    require(params.tokenIn == _ERC20A);
    require(params.tokenOut == _ERC20B);
    require(params.destinationIn == lmpVault() || params.destinationIn == _BalancerDestVault);
    require(params.destinationOut == lmpVault() || params.destinationOut == _BalancerDestVault);
    require(lmpVault() != _BalancerDestVault);
}

function initRebalanceToIdleParamsCVL(env e, IStrategy.RebalanceParams params) {

    // Require validateRebalanceParams() check passed
    require(validRebalanceParamsCVL(e, params));

    // params.destinationIn == address(lmpVault)
    require(params.tokenIn == _ERC20A);
    require(params.tokenOut == _ERC20B);
    require(params.destinationIn == lmpVault());
    require(params.destinationOut == _BalancerDestVault);
    require(lmpVault() != _ERC20A && lmpVault() != _ERC20B && lmpVault() != _BalancerDestVault);
}

// ClearExpirePause sets _swapCostOffsetPeriod, so skip when possible to avoid double write
rule rebalanceSuccessfullyExecuted_updatesSwapCostOffsetPeriod(env e, calldataarg args) {

    initConstructor(e);

    bool isExpiredPauseState = lastPausedTimestamp() > 0 && !paused(e);

    uint16 swapCostOffsetPeriodBefore = ghostSwapCostOffsetPeriod;

    rebalanceSuccessfullyExecuted(e, args);

    uint16 swapCostOffsetPeriodAfter = ghostSwapCostOffsetPeriod;

    assert(!isExpiredPauseState => swapCostOffsetPeriodAfter == swapCostOffsetPeriodInDays(e));
}

// validateRebalanceParams()

function validRebalanceParamsCVL(env e, IStrategy.RebalanceParams params) returns bool {
    bool notZero = params.destinationIn != 0 && params.tokenIn != 0 && params.amountIn != 0 && params.destinationOut != 0 && params.tokenOut != 0 && params.amountOut != 0;
    bool dstInRegistered = (params.destinationIn == lmpVault() || isDestinationRegisteredCVL[params.destinationIn] || isDestinationQueuedForRemovalCVL[params.destinationIn]);
    bool dstOutRegistered = (params.destinationOut == lmpVault() || isDestinationRegisteredCVL[params.destinationOut] || isDestinationQueuedForRemovalCVL[params.destinationOut]);
    bool correctShutdown = ghostIsShutdown_LMPVault 
        => params.destinationIn == lmpVault();
    bool destinationNotEq = params.destinationIn != params.destinationOut;
    bool correctTokenIn = params.destinationIn == lmpVault() 
        => params.tokenIn == assetCVL;
    bool correctTokenOut = params.destinationOut == lmpVault() 
        => (params.tokenOut == assetCVL && params.amountOut <= totalIdleCVL);

    return notZero && dstInRegistered && dstOutRegistered && correctShutdown && destinationNotEq && correctTokenIn && correctTokenOut;
}

rule verifyRebalanceParamsValidated(env e, IStrategy.RebalanceParams params, IStrategy.SummaryStats outSummary) {

    initConstructor(e);

    bool validParams = validRebalanceParamsCVL(e, params);

    verifyRebalance@withrevert(e, params, outSummary);
    bool reverted = lastReverted;

    assert(!validParams => reverted);
}

// verifyRebalanceToIdle()

function verifyRebalanceToIdleCVL(env e, bool reverted, IStrategy.RebalanceParams params) returns mathint {
    
    // Scenario 1: the destination has been shutdown -- done when a fast exit is required
    mathint retSlippage1 = 0;
    if(ghostIsShutdown_DestinationVault) {
        retSlippage1 = to_mathint(maxEmergencyOperationSlippage());
    } 

    // Scenario 2: the LMPVault has been shutdown
    mathint retSlippage2 = retSlippage1;
    if (ghostIsShutdown_LMPVault && to_mathint(maxShutdownOperationSlippage()) > retSlippage1) {
        retSlippage2 = to_mathint(maxShutdownOperationSlippage());
    } 

    // Scenario 3: position is a dust position and should be trimmed
    mathint retSlippage3 = retSlippage2;
    if (verifyCleanUpOperationCLV(e, reverted, params) && to_mathint(maxNormalOperationSlippage()) > retSlippage2) {
        retSlippage3 = to_mathint(maxNormalOperationSlippage());
    }

    // Scenario 4: the destination has been moved out of the LMPs active destinations
    mathint retSlippage4 = retSlippage3;
    if (isDestinationQueuedForRemovalCVL[params.destinationOut] && to_mathint(maxNormalOperationSlippage()) > retSlippage3) {
        retSlippage4 = to_mathint(maxNormalOperationSlippage());
    }

    // Scenario 5: the destination needs to be trimmed because it violated a constraint
    mathint retSlippage5 = retSlippage4;
    if (to_mathint(maxTrimOperationSlippage()) > retSlippage4) {
        ghostTmpTrimAmount = getDestinationTrimAmountHarness(e, params.destinationOut); // Not CVL used
        if (ghostTmpTrimAmount < 10^18 && verifyTrimOperationCVL(e, reverted, params, ghostTmpTrimAmount)) {
            retSlippage5 = to_mathint(maxTrimOperationSlippage());
        }
    }

    return retSlippage5;
}

// getRebalanceValueStats()

function getRebalanceValueStatsCVL(env e, IStrategy.RebalanceParams params) 
    returns (mathint, mathint, mathint, mathint, mathint, mathint) {

    mathint inPrice;
    mathint outPrice;
    mathint inEthValue;
    mathint outEthValue;
    mathint swapCost;
    mathint slippage;

    if(params.destinationOut != lmpVault()) {
        outPrice = _BalancerDestVault.getValidatedSpotPrice(e);
    } else {
        outPrice = 10 ^ _ERC20B.decimals(e);
    }

    if(params.destinationIn != lmpVault()) {
        inPrice = _BalancerDestVault.getValidatedSpotPrice(e);
    } else {
        inPrice = 10 ^ _ERC20A.decimals(e);
    }

    if(params.destinationOut != lmpVault()) {
        outEthValue = outPrice * params.amountOut / 10 ^ _ERC20B.decimals(e);
    } else {
        outEthValue = params.amountOut;
    }

    if(params.destinationIn != lmpVault()) {
        inEthValue = inPrice * params.amountIn / 10 ^ _ERC20A.decimals(e);
    } else {
        inEthValue = params.amountIn;
    }

    swapCost = subSaturateUint256CVL(outEthValue, inEthValue);
    slippage = outEthValue == 0 ? 0 : swapCost * 10^18 / outEthValue;

    return (inPrice, outPrice, inEthValue, outEthValue, swapCost, slippage);
}

rule getRebalanceValueStatsIntegrity(env e, IStrategy.RebalanceParams params) {

    initConstructor(e);
    initRebalanceParamsCVL(e, params);

    mathint inPrice;
    mathint outPrice;
    mathint inEthValue;
    mathint outEthValue;
    mathint swapCost;
    mathint slippage;
    inPrice, outPrice, inEthValue, outEthValue, swapCost, slippage 
        = getRebalanceValueStatsHarness(e, params);
    
    mathint inPriceCVL;
    mathint outPriceCVL;
    mathint inEthValueCVL;
    mathint outEthValueCVL;
    mathint swapCostCVL;
    mathint slippageCVL;
    inPriceCVL, outPriceCVL, inEthValueCVL, outEthValueCVL, swapCostCVL, slippageCVL 
        = getRebalanceValueStatsCVL(e, params);

    assert(inPriceCVL == inPrice);
    assert(outPriceCVL == outPrice);
    assert(inEthValueCVL == inEthValue);
    assert(outEthValueCVL == outEthValue);
    assert(swapCostCVL == swapCost);
    assert(slippageCVL == slippage);
}

// ensureNotStaleData()

function ensureNotStaleDataCVL(env e, bool reverted, mathint timestamp) {
    assert(to_mathint(e.block.timestamp) < timestamp => reverted);
    assert(to_mathint(e.block.timestamp) - timestamp > to_mathint(staleDataToleranceInSeconds()) => reverted);
}

rule ensureNotStaleDataIntegrity(env e, string name, uint256 dataTimestamp) {

    ensureNotStaleDataHarness@withrevert(e, name, dataTimestamp);
    bool reverted = lastReverted;

    ensureNotStaleDataCVL(e, reverted, dataTimestamp);
}

// verifyCleanUpOperation()

function verifyCleanUpOperationCLV(env e, bool reverted, IStrategy.RebalanceParams params) returns bool {

    require(ghostTmpCurrentDebt == 0);

    // ensureNotStaleData
    ensureNotStaleDataCVL(e, reverted, ghostLMPVaultDestinationInfo_lastReport[params.destinationOut]);

    // adjust the current debt based on the currently owned shares
    if(ghostLMPVaultDestinationInfo_ownedShares[params.destinationOut] != 0) {
        ghostTmpCurrentDebt = (ghostLMPVaultDestinationInfo_currentDebt[params.destinationOut] 
            * to_mathint(_BalancerDestVault.balanceOf(e, lmpVault()))) 
                / ghostLMPVaultDestinationInfo_ownedShares[params.destinationOut];
    }

    // If the current position is < 2% of total assets, trim to idle is allowed
    if(ghostTmpCurrentDebt * 10^18 < (totalAssetsCVL * 10^18) / 50) {
        return true;
    }

    return false;
}

rule verifyCleanUpOperationIntegrity(env e, IStrategy.RebalanceParams params) {

    initRebalanceToIdleParamsCVL(e, params);

    bool result = verifyCleanUpOperationHarness@withrevert(e, params);
    bool reverted = lastReverted;

    bool resultCVL = verifyCleanUpOperationCLV(e, reverted, params);

    assert(!reverted => result == resultCVL);
}

// verifyTrimOperation() 

function verifyTrimOperationCVL(env e, bool reverted, IStrategy.RebalanceParams params, mathint trimAmount) returns bool {

    if(trimAmount == 0) {
        return true;
    }

    // revert if information is too old
    ensureNotStaleDataCVL(e, reverted, ghostLMPVaultDestinationInfo_lastReport[params.destinationOut]);

    // adjust the current debt based on the currently owned shares
    if(ghostLMPVaultDestinationInfo_ownedShares[params.destinationOut] == 0) {
        ghostTmpCurrentDebt = 0;
    } else {
        ghostTmpCurrentDebt = 
            (ghostLMPVaultDestinationInfo_currentDebt[params.destinationOut] 
                * to_mathint(_BalancerDestVault.balanceOf(e, lmpVault()))) 
            / ghostLMPVaultDestinationInfo_ownedShares[params.destinationOut];
    }

    // calculate the total value of the lmpVault after the rebalance is made
    ghostTmpDestValueAfterRebalance = to_mathint(_BalancerDestVault.debtValue(e, require_uint256(_BalancerDestVault.balanceOf(e, lmpVault()) - params.amountOut)));
    ghostTmpLmpAssetsAfterRebalance = 
        to_mathint(totalAssetsCVL) 
        + to_mathint(params.amountIn) 
        + ghostTmpDestValueAfterRebalance
        - ghostTmpCurrentDebt;

    if(ghostTmpLmpAssetsAfterRebalance > 0) {
        return (ghostTmpDestValueAfterRebalance * 10^18) / ghostTmpLmpAssetsAfterRebalance >= trimAmount;
    } else {
        return true;
    }
}

rule verifyTrimOperationIntegrity(env e, IStrategy.RebalanceParams params, uint256 trimAmount) {
    
    initRebalanceToIdleParamsCVL(e, params);

    bool result = verifyTrimOperationHarness@withrevert(e, params, trimAmount);
    bool reverted = lastReverted;

    bool resultCVL = verifyTrimOperationCVL(e, reverted, params, trimAmount);

    assert(!reverted => result == resultCVL);
}

// subSaturate()
function subSaturateUint256CVL(mathint a, mathint b) returns mathint {
    if (b >= a) return 0;
    return a - b;
}