using BalancerAuraDestinationVault as BalancerDestVault;
using CurveConvexDestinationVault as CurveDestVault;
using SystemRegistry as systemRegistry;
using LMPVault as _lmpVault;



methods {
    /** Summaries **/
    
    // Base
    function _.getPriceInEth(address token) external with (env e) => getPriceInEthCVL[token][e.block.timestamp] expect (uint256);
    function _.getSpotPriceInEth(address token, address pool) external => getSpotPriceInEthCVL[token][pool] expect (uint256);
    function _.getBptIndex() external => getBptIndexCVL expect (uint256);
    function _.current() external => DISPATCHER(true); // can be dispatched if returned values are important
    
    // Vault
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
    // function _.getDestinationInfo(address dest) external => getDestinationInfoCVL(dest) expect LMPDebt.DestinationInfo;
    function _.getDestinationInfo(address dest) external => CONSTANT;

    // ERC20's `decimals` summarized as 6, 8 or 18 (validDecimal), can be changed to ALWAYS(18) for better runtime.
    // This helps with runtime because arbitrary decimal value creates many nonlinear operations.
    function _.decimals() external => ALWAYS(18); // validDecimal expect uint256; // validDecimal is 6, 8 or 18 for a better summary

    // Can help reduce complexity, think carefully about implications before using.
    // May need to think of a more clever way to summarize this.
    // function LMPStrategy.getRebalanceValueStats(IStrategy.RebalanceParams memory input) internal returns (LMPStrategy.RebalanceValueStats memory) => getRebalanceValueStatsCVL(input);
    
    /** Dispatchers **/
    // base
    function _.accessController() external => DISPATCHER(true); // needed in constructor, rest is handled by linking
    function _.getStats() external => DISPATCHER(true);
    function _.getValidatedSpotPrice() external => DISPATCHER(true);
    function _.getPool() external => DISPATCHER(true);
    function _.getPriceOrZero(address, uint40) external => DISPATCHER(true);
    function _.underlying() external => DISPATCHER(true);
    function _.underlyingTokens() external => DISPATCHER(true);
    function _.debtValue(uint256) external => DISPATCHER(true);
    function _.isShutdown() external => DISPATCHER(true);

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
    function getRebalanceValueStatsExternal(IStrategy.RebalanceParams) external returns (LMPStrategy.RebalanceValueStats);
    function getRebalanceInSummaryStatsExternal(IStrategy.RebalanceParams)external returns (IStrategy.SummaryStats);
    function getSwapCostOffsetTightenThresholdInViolations() external returns (uint16) envfree;
    function calculatePercentageBetweenSpotAndSafe(uint256,uint256)external returns (uint256) envfree;
    // function castToVault(address dest)external returns (LMPStrategy.IDestinationVault) envfree;
    // function clearExpiredPauseExternal()external returns (bool) envfree;

    //library

    
    
}



definition FUNCTIONS_CHANGE_THE_STATE(method f) returns bool =
    f.selector == sig:navUpdate(uint256).selector
    || f.selector == sig:rebalanceSuccessfullyExecuted(IStrategy.RebalanceParams).selector;

definition FUNCTIONS_NEED_TO_CLEAR_EXPIRED_PAUSE(method f) returns bool =
    f.selector == sig:navUpdate(uint256).selector
    || f.selector == sig:rebalanceSuccessfullyExecuted(IStrategy.RebalanceParams).selector;

definition VIEW_PURE_FUNCTIONS(method f) returns bool =
    f.isView || f.isPure;

definition VIOLATIONS_INIT() returns bool =
violationsGhost == 0 && violationCountGhost == 0 && violationLenGhost == 0; 

definition VIOLATIONS_REACHABLE_STATE() returns bool =
violationsGhost == 7 && violationCountGhost == 3 && violationLenGhost == 4;

definition MAX_NAV_TRACKING() returns uint8 = 91 ;

/** Functions **/
// For base summaries
function getRebalanceValueStatsCVL(IStrategy.RebalanceParams input) returns LMPStrategy.RebalanceValueStats {
    LMPStrategy.RebalanceValueStats tmp;
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

function callerIsLMP(address caller) returns bool {
    return caller == _lmpVault ;
}


/** Ghosts and Hooks **/
// For base summaries
ghost uint256 getBptIndexCVL;
ghost uint256 validDecimal {
    axiom validDecimal == 6 || validDecimal == 8 || validDecimal == 18;
}
ghost mapping(address => mapping(uint256 => uint256)) getPriceInEthCVL;
ghost mapping(address => mapping(address => uint256)) getSpotPriceInEthCVL;

// For vault summaries
ghost uint256 totalIdleCVL;
ghost address assetCVL;
ghost uint256 totalAssetsCVL;
ghost bool    isShutdownCVL;

ghost mapping(address => bool) isDestinationRegisteredCVL;
ghost mapping(address => bool) isDestinationQueuedForRemovalCVL;

// For properties
ghost uint16 _swapCostOffsetPeriodGhost;
ghost uint40 lastRebalanceTimestampGhost;
ghost uint256 maxSlippageCVL;
ghost mapping(address => uint40) lastAddTimestampByDestinationGhost {
    init_state axiom forall address f. lastAddTimestampByDestinationGhost[f]==0;
}
ghost uint8  violationCountGhost{
    init_state axiom violationCountGhost == 0;
}
ghost uint8  violationLenGhost{
    init_state axiom violationLenGhost == 0;
}
ghost uint16 violationsGhost{
    init_state axiom violationsGhost == 0;
}

hook Sload uint16 defaultValue _swapCostOffsetPeriod {
    require _swapCostOffsetPeriodGhost == defaultValue;
}

hook Sstore _swapCostOffsetPeriod uint16 defaultValue {
    _swapCostOffsetPeriodGhost = defaultValue;
}

hook Sload uint40 RebalanceTimeVal currentContract.lastRebalanceTimestamp {
    require lastRebalanceTimestampGhost == RebalanceTimeVal;
}

hook Sstore currentContract.lastRebalanceTimestamp uint40 RebalanceTimeVal {
    lastRebalanceTimestampGhost = RebalanceTimeVal;
}

hook Sload uint40 lastAddVal currentContract.lastAddTimestampByDestination[KEY address a] {
    require lastAddTimestampByDestinationGhost[a] == lastAddVal;
}

hook Sstore currentContract.lastAddTimestampByDestination [KEY address a] uint40 lastAddVal {
    lastAddTimestampByDestinationGhost[a] = lastAddVal;
}

hook Sload uint8 violationCountVal currentContract.violationTrackingState.violationCount {
    require violationCountGhost == violationCountVal ;
}
hook Sstore currentContract.violationTrackingState.violationCount uint8 violationCountVal {
    violationCountGhost = violationCountVal ;
}

hook Sload uint8 violationLenVal currentContract.violationTrackingState.len {
    require violationLenGhost == violationLenVal ;
}
hook Sstore currentContract.violationTrackingState.len uint8 violationLenVal {
    violationLenGhost = violationLenVal ;
}

hook Sload uint16 violationsVal currentContract.violationTrackingState.violations {
    require violationsGhost == violationsVal ;
}
hook Sstore currentContract.violationTrackingState.violations uint16 violationsVal {
    violationsGhost = violationsVal ;
}





/** Properties **/

use builtin rule sanity;

// Offset period must be between swapCostOffsetMaxInDays and swapCostOffsetMinInDays.
invariant offsetIsInBetween()
    _swapCostOffsetPeriodGhost <= swapCostOffsetMaxInDays() && _swapCostOffsetPeriodGhost >= swapCostOffsetMinInDays();

// invariant violation()
//     violationCountGhost <= violationLenGhost{
//         preserved {
//            require violationsGhost != 0;
//         }
//     }

// invariant violationsShouldntBeZeroIfThereIsViolation()
//     violationsGhost == 0 => (violationCountGhost == 0);



rule destinationShouldBeRegisteredOrQueued(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    require params.destinationIn != _lmpVault;
    require params.destinationOut != _lmpVault;
    verifyRebalance@withrevert(e,params,summary);
    assert (!isDestinationRegisteredCVL[params.destinationIn] && !isDestinationQueuedForRemovalCVL[params.destinationIn]) => lastReverted;
    assert (!isDestinationRegisteredCVL[params.destinationOut] && !isDestinationQueuedForRemovalCVL[params.destinationOut]) => lastReverted;
}

rule lmpVaultShoutDown(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    verifyRebalance@withrevert(e,params,summary);
    assert !lastReverted => (!_lmpVault.isShutdown(e) || params.destinationIn ==_lmpVault) ;
}

rule rebalanceWithTheSameDestination(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    verifyRebalance@withrevert(e,params,summary);
    assert params.destinationIn == params.destinationOut => lastReverted;
}

rule tokenInOutShouldMatchTheBaseAssetWhenIdle(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    address lmpAsset = _lmpVault.asset(e);
    address destIn  = params.destinationIn;
    address destOut = params.destinationOut;
    verifyRebalance@withrevert(e,params,summary);
    assert destIn  == _lmpVault && params.tokenIn  != assetCVL => lastReverted;
    assert destOut == _lmpVault && params.tokenOut != assetCVL => lastReverted;
    assert destOut == _lmpVault && params.amountOut > totalIdleCVL => lastReverted;
    // assert destIn  != _lmpVault && params.tokenIn  != destIn.underlying(e) => lastReverted;
    // assert destOut != _lmpVault && params.tokenOut != destOut.underlying(e) => lastReverted;
    // assert destOut != _lmpVault && params.amountOut > destOut.balanceOf(e,_lmpVault) => lastReverted;
}

rule tokenInOutShouldMatchTheBaseAssetNotIdle(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    address destIn  = params.destinationIn;
    address destOut = params.destinationOut;
    require destIn  == BalancerDestVault;
    require destOut == CurveDestVault;
    address inUnderlying  = BalancerDestVault.underlying(e);
    address outUnderlying = CurveDestVault.underlying(e);
    uint256 outBalanceOf  = CurveDestVault.balanceOf(e,_lmpVault);
    verifyRebalance@withrevert(e,params,summary);
    assert  params.tokenIn  != inUnderlying => lastReverted;
    assert  params.tokenOut != outUnderlying => lastReverted;
    assert  params.amountOut > outBalanceOf => lastReverted;
}

// rule RebalanceValueStatsIntegrityEthValueNotIdle(env e){
//     IStrategy.RebalanceParams params;
//     LMPStrategy.RebalanceValueStats stats;
//     address destIn  = params.destinationIn;
//     address destOut = params.destinationOut;
//     require destIn  == BalancerDestVault;
//     require destOut == CurveDestVault;
//     stats = getRebalanceValueStatsExternal(e,params);
//     assert destOut != _lmpVault => stats.outEthValue == assert_uint256((params.amountOut * CurveDestVault.getValidatedSpotPrice(e)) / CVLPow(10,18));
//     assert destIn  != _lmpVault => stats.inEthValue  == assert_uint256((params.amountIn  * BalancerDestVault.getValidatedSpotPrice(e)) / CVLPow(10,18));
// }

rule RebalanceValueStatsIntegrityEthIdle(env e){
    IStrategy.RebalanceParams params;
    LMPStrategy.RebalanceValueStats stats;
    address destIn  = params.destinationIn;
    address destOut = params.destinationOut;
    stats = getRebalanceValueStatsExternal(e,params);
    assert destOut == _lmpVault => stats.outEthValue == params.amountOut;
    assert destIn  == _lmpVault => stats.inEthValue  == params.amountIn;
}

    rule p0_mutation(env e){
    IStrategy.RebalanceParams params;
    LMPStrategy.RebalanceValueStats stats;
    require params.destinationOut == _lmpVault;
    stats = getRebalanceValueStatsExternal(e,params);
    assert stats.outEthValue == params.amountOut;
    }

rule RebalanceValueStatsIntegrityNotIdle(env e){
    IStrategy.RebalanceParams params;
    LMPStrategy.RebalanceValueStats stats;
    address destIn  = params.destinationIn;
    address destOut = params.destinationOut;
    stats = getRebalanceValueStatsExternal(e,params);
    assert  destOut !=_lmpVault => (stats.outPrice == (CurveDestVault.getValidatedSpotPrice(e))) || stats.outPrice == BalancerDestVault.getValidatedSpotPrice(e);
    assert  destIn  !=_lmpVault => (stats.inPrice  == (BalancerDestVault.getValidatedSpotPrice(e))) || stats.inPrice  == CurveDestVault.getValidatedSpotPrice(e) ;

}

// rule RebalanceValueStatsIntegrityIdlePrice(env e){
//     IStrategy.RebalanceParams params;
//     LMPStrategy.RebalanceValueStats stats;
//     address destIn  = params.destinationIn;
//     address destOut = params.destinationOut;
//     stats = getRebalanceValueStatsExternal(e,params);
//     assert  destOut ==_lmpVault => stats.outPrice == CVLPow(10,18);
//     assert  destIn  ==_lmpVault => stats.inPrice  == CVLPow(10,18);
// }

rule slippageCheck(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    LMPStrategy.RebalanceValueStats stats;
    uint256 maxNormalSlippage = maxNormalOperationSlippage(e);
    require params.destinationIn != _lmpVault;
    stats = getRebalanceValueStatsExternal(e,params);
    verifyRebalance@withrevert(e,params,summary);
    assert stats.slippage > maxNormalSlippage => lastReverted;
}



// `violationTrackingState.violationCount` must not be increased by more than 1
rule cantJumpTwoViolationsAtOnce(env e, method f) {
    uint16 numOfViolationsBefore;
    numOfViolationsBefore,_,_ = violationTrackingState();

    calldataarg args;
    f(e, args);

    uint16 numOfViolationsAfter;
    numOfViolationsAfter,_,_ = violationTrackingState();

    assert numOfViolationsAfter - numOfViolationsBefore <= 1;
}



rule onlyLMPCanChangeLastRebalanceTimestamp(env e, method f, calldataarg args){

    uint40 timeBefore = lastRebalanceTimestampGhost;

    f(e, args);

    uint40 timeAfter = lastRebalanceTimestampGhost;

    assert((timeAfter != timeBefore) => callerIsLMP(e.msg.sender));
}

rule integrityOfVerifyRebalance(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    bool successResult;
    successResult,_= verifyRebalance(e,params,summary);
    assert successResult == true ;

}

rule idleWhilePausing(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    require paused(e);
    verifyRebalance@withrevert(e,params,summary);
    satisfy !lastReverted;
}
rule RebalanceWhilePausing(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    require params.destinationIn != _lmpVault;
    require paused(e);
    verifyRebalance@withrevert(e,params,summary);
    assert lastReverted;
}

rule p2_mutation(env e){
    IStrategy.RebalanceParams params;
    IStrategy.SummaryStats summary;
    require params.destinationIn == _lmpVault;
    verifyRebalance@withrevert(e,params,summary);
    satisfy !lastReverted;
}
// rule p1_mutation(env e){
//     IStrategy.RebalanceParams params;
//     IStrategy.SummaryStats summary;
//     uint256 priceInEth = getPriceInEthCVL[_][_];
//     uint256 spotPriceInEth = getSpotPriceInEthCVL[_][_] ;
//     require params.destinationOut != _lmpVault;
//     require to_mathint(spotPriceInEth) > 0;
//     require to_mathint(priceInEth) > 0;
//     require to_mathint(priceInEth) > to_mathint(spotPriceInEth);
//     uint256 percentage_safe_spot = calculatePercentageBetweenSpotAndSafe(priceInEth,spotPriceInEth);
//     require percentage_safe_spot !=0;
//     uint256 tolerance = lstPriceGapTolerance(e);
//     verifyRebalance@withrevert(e,params,summary);

//     assert !lastReverted => percentage_safe_spot >  tolerance ;
// }

rule navUpdateIntegrity(env e){
    uint256 navPerShare;
    uint8 navTrackingLenBefore;
    navTrackingLenBefore ,_,_ = navTrackingState(e);
    require navTrackingLenBefore < MAX_NAV_TRACKING() ;
    navUpdate(e,navPerShare);
    uint8 navTrackingLenAfter;
    navTrackingLenAfter,_,_ = navTrackingState(e);
    assert navTrackingLenAfter ==  assert_uint8(to_mathint(navTrackingLenBefore + 1)) ;
}

rule clearExpiredPauseIntegrity(env e,method f,calldataarg args){
    uint40 _lastPausedTimeStamp = lastPausedTimestamp(e);
    require _lastPausedTimeStamp != 0 ;
    f(e,args);
    uint40 lastPausedTimeStamp_ = lastPausedTimestamp(e);
    assert  lastPausedTimeStamp_ == 0 =>  FUNCTIONS_NEED_TO_CLEAR_EXPIRED_PAUSE(f);
}

rule onlyNavUpdateCanPause(env e,method f, calldataarg args){
    uint40 _lastPausedTimeStamp = lastPausedTimestamp(e);
    require _lastPausedTimeStamp == 0 ;
    f(e,args);
    uint40 lastPausedTimeStamp_ = lastPausedTimestamp(e);
    assert  lastPausedTimeStamp_ != 0 =>  f.selector == sig:navUpdate(uint256).selector;
    assert  lastPausedTimeStamp_ != 0  => assert_uint256(lastPausedTimeStamp_) == e.block.timestamp;
}

rule whenToPauseStrategy(env e, method f, calldataarg args){
    uint40 _lastPausedTimeStamp = lastPausedTimestamp(e);
    require _lastPausedTimeStamp == 0;
    bool pausedState = paused(e);
    f(e,args);
    uint40 lastPausedTimeStamp_ = lastPausedTimestamp(e);
    assert lastPausedTimeStamp_ !=0 =>  (!pausedState &&  violationLenGhost > navLookback3InDays(e));
}

rule dontUpdatingRebalanceTimestampForIdle(env e){
    IStrategy.RebalanceParams params;
    uint40 _lastRebalanceTimestamp = lastRebalanceTimestampGhost;
    rebalanceSuccessfullyExecuted(e,params);
    uint40 lastRebalanceTimestamp_ = lastRebalanceTimestampGhost;
    assert ((lastRebalanceTimestamp_ != _lastRebalanceTimestamp) => (params.destinationIn != _lmpVault));
    // assert lastRebalanceTimestamp_ != _lastRebalanceTimestamp => assert_uint256(lastRebalanceTimestamp_) == e.block.timestamp;
    assert lastRebalanceTimestamp_ != _lastRebalanceTimestamp => lastAddTimestampByDestinationGhost[params.destinationIn] == lastRebalanceTimestamp_ ;
}

rule violationsResetIntegrity(env e){
    IStrategy.RebalanceParams params;
    require params.destinationIn == _lmpVault;
    require violationLenGhost !=0;
    uint8 violationLenBefore = violationLenGhost;   
    uint8 violationCountBefore = violationCountGhost;
    uint16 tightenSwapOffset = swapCostOffsetTightenThresholdInViolations(e);
    rebalanceSuccessfullyExecuted(e,params);
    uint8 violationLenAfter = violationLenGhost;
    assert violationLenAfter == 0 => (violationLenBefore == 10 && assert_uint16(violationCountBefore) >= tightenSwapOffset);
}

rule violationsInsertion(env e){
    IStrategy.RebalanceParams params;
    uint8 violationLenBefore = violationLenGhost;
    rebalanceSuccessfullyExecuted(e,params);
    uint8 violationLenAfter = violationLenGhost;
    assert (violationLenAfter > violationLenBefore) => (params.destinationOut != _lmpVault && params.destinationIn != _lmpVault);
}


rule violationsCountIntegrity(env e){
    IStrategy.RebalanceParams params;
    uint8 violationCountBefore = violationCountGhost;
    uint40 swapCostOffset= assert_uint40(swapCostOffsetPeriodInDays(e) * 86400 );
    rebalanceSuccessfullyExecuted(e,params);
    uint8 violationCountAfter = violationCountGhost;
    assert (violationCountAfter > violationCountBefore) => assert_uint40(lastRebalanceTimestampGhost - lastAddTimestampByDestinationGhost[params.destinationOut]) < swapCostOffset;
}


rule swapCostOffsetPeriodInDaysIntegrity(env e){
    uint40 lastPausedTimestamp = lastPausedTimestamp(e);
    bool pausedState = paused(e);
    uint16 swapCostOffset = swapCostOffsetPeriodInDays(e);
    assert lastPausedTimestamp > 0 && !pausedState => swapCostOffset == swapCostOffsetMinInDays(e);  
}

rule swapCostOffsetPeriodWithoutRelax(env e){
    uint40 lastPausedTimestamp = lastPausedTimestamp(e);
    require paused(e);
    uint40 relaxOffset = swapCostOffsetRelaxThresholdInDays(e);
    uint40 swapCostOffsetPeriod = _swapCostOffsetPeriodGhost;
    uint16 swapCostOffset = swapCostOffsetPeriodInDays(e);
    assert (relaxOffset == 0 && assert_uint40(swapCostOffsetMaxInDays(e)) > swapCostOffsetPeriod) => swapCostOffset == _swapCostOffsetPeriodGhost;  
}

rule maxSwapCostOffset(env e){
    uint16 maxOffset = swapCostOffsetMaxInDays(e);
    require swapCostOffsetMinInDays() <= maxOffset;
    uint16 swapCostOffset = swapCostOffsetPeriodInDays(e);
    assert swapCostOffset <= maxOffset;  
}

