using BalancerAuraDestinationVault as BalancerDestVault;
using CurveConvexDestinationVault as CurveDestVault;
using SystemRegistry as systemRegistry;

methods {
    /** Summaries **/
    
    // Base
    function _.getPriceInEth(address token) external with (env e) => getPriceInEthCVL expect uint256;
    function _.getBptIndex() external => getBptIndexCVL expect (uint256);
    function _.current() external => NONDET; // can be dispatched if returned values are important
    
    // Vault
    // Summarized instead of linked to help with runtime. 
    // The two state changing functions don't change any relevant state and aren't implemented.
    // The rest of the functions are getters so ghost summary has the same effect as linking.
    function _.addToWithdrawalQueueHead(address) external => NONDET;
    function _.addToWithdrawalQueueTail(address) external => NONDET;
    function _.totalIdle() external => totalIdleCVL expect uint256;
    function _.asset() external => assetCVL expect uint256;
    function _.totalAssets() external => totalAssetsCVL expect uint256;
    function _.isDestinationRegistered(address dest) external => isDestinationRegisteredCVL[dest] expect bool;
    function _.isDestinationQueuedForRemoval(address dest) external => isDestinationQueuedForRemovalCVL[dest] expect bool;
    function _.getDestinationInfo(address dest) external => getDestinationInfoCVL(dest) expect LMPDebt.DestinationInfo;
    // function _.getDaysAgo(uint8 daysAgo) internal => daysAgoCVL expect uint256;

    // ERC20's `decimals` summarized as 6, 8 or 18 (validDecimal), can be changed to ALWAYS(18) for better runtime.
    // This helps with runtime because arbitrary decimal value creates many nonlinear operations.
    function _.decimals() external => ALWAYS(18); // validDecimal expect uint256; // validDecimal is 6, 8 or 18 for a better summary

    // Can help reduce complexity, think carefully about implications before using.
    // May need to think of a more clever way to summarize this.
    function LMPStrategy.getRebalanceValueStats(IStrategy.RebalanceParams memory input) internal returns (LMPStrategy.RebalanceValueStats memory) => getRebalanceValueStatsCVL(input);
    function LMPStrategy.verifyCleanUpOperation(IStrategy.RebalanceParams memory params) internal returns (bool) => ALWAYS(true);
    // function LMPVault.isDestinationQueuedForRemoval(address dest) external returns (bool) => ALWAYS(true);
    // function LMPStrategy.validateRebalanceParams(IStrategy.RebalanceParams memory params) internal => validateRebalanceParamsCVL(params);
    
    /** Dispatchers **/
    // base
    function _.accessController() external => DISPATCHER(true); // needed in constructor, rest is handled by linking
    function _.getStats() external => DISPATCHER(true);
    function _.getValidatedSpotPrice() external => DISPATCHER(true);
    function _.isShutdown() external => DISPATCHER(true);
    function _.getPool() external => DISPATCHER(true);
    function _.getPriceOrZero(address, uint40) external => DISPATCHER(true);
    function _.underlying() external => DISPATCHER(true);
    function _.underlyingTokens() external => DISPATCHER(true);
    function _.debtValue(uint256) external => DISPATCHER(true);
    function _.getSpotPriceInEth(address a, address b) external => getSpotPriceInEthCVL expect uint256;

    // ERC20
    function _.name() external => DISPATCHER(true);
    function _.symbol() external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    /** Envfree **/
    // Base
    function violationTrackingState() external returns (uint8, uint8, uint16) envfree;
    function swapCostOffsetMaxInDays() external returns (uint16) envfree;
    function swapCostOffsetMinInDays() external returns (uint16) envfree;
    // Harnessed
    function getDestinationSummaryStatsExternal(address, uint256, LMPStrategy.RebalanceDirection, uint256) external returns (IStrategy.SummaryStats);
    function getSwapCostOffsetTightenThresholdInViolations() external returns (uint16) envfree;
}

/** Functions **/
// For base summaries
function getRebalanceValueStatsCVL(IStrategy.RebalanceParams input) returns LMPStrategy.RebalanceValueStats {
    env e;
    LMPStrategy.RebalanceValueStats tmp = setValueStatsSlippage(
        e, inPriceCVL, outPriceCVL, inEthValueCVL, outEthValueCVL, swapCostCVL, slippageCVL
    );
    return tmp;
}

// For vault summaries
function getDestinationInfoCVL(address dest) returns LMPDebt.DestinationInfo {
    LMPDebt.DestinationInfo info;
    return info;
}

function currentCVL() returns IDexLSTStats.DexLSTStatsData {
    IDexLSTStats.DexLSTStatsData data;
    return data;
}

/** Ghosts and Hooks **/
// For base summaries
ghost uint256 getBptIndexCVL;
ghost uint256 validDecimal {
    axiom validDecimal == 6 || validDecimal == 8 || validDecimal == 18;
}
// ghost mapping(address => mapping(uint256 => uint256)) getPriceInEthCVL;

// For vault summaries
ghost uint256 totalIdleCVL;
ghost uint256 assetCVL;
ghost uint256 totalAssetsCVL;
ghost uint256 getSpotPriceInEthCVL;
ghost uint256 getPriceInEthCVL;

ghost uint256 inPriceCVL;
ghost uint256 outPriceCVL;
ghost uint256 inEthValueCVL;
ghost uint256 outEthValueCVL;
ghost uint256 swapCostCVL;
ghost uint256 slippageCVL;

ghost mapping(address => bool) isDestinationRegisteredCVL;
ghost mapping(address => bool) isDestinationQueuedForRemovalCVL;

// For properties
ghost uint16 _swapCostOffsetPeriodGhost;

hook Sload uint16 defaultValue _swapCostOffsetPeriod {
    require _swapCostOffsetPeriodGhost == defaultValue;
}

hook Sstore _swapCostOffsetPeriod uint16 defaultValue {
    _swapCostOffsetPeriodGhost = defaultValue;
}

/** Properties **/

// rule revertLessThanEqualSwapCost(
//     IStrategy.RebalanceParams params,
//     IStrategy.SummaryStats outSummary
// ) {
//     env e;
//     require isLessThanEqualSwapCost(e, params, outSummary);

//     bool success;
//     string message;
//     success, message = verifyRebalance@withrevert(e, params, outSummary);

//     assert lastReverted;
// }

rule rebalanceNotAllowedWhenPaused(
    IStrategy.RebalanceParams params,
    IStrategy.SummaryStats outSummary
) {
    env e;
    require paused(e);
    require params.destinationIn != getLmpVaultAddress(e);

    bool success;
    string message;
    success, message = verifyRebalance@withrevert(e, params, outSummary);

    assert lastReverted;
}
