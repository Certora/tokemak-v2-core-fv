# **Tokemak Audit Competition on Hats.finance** 

## Table of contents

- [**Overview**](#overview)
    - [**Competition Details**](#competition-details)
    - [**About Tokemak**](#about-tokemak)
    - [**About Hats Finance**](#about-hats-finance)
    - [**About Certora**](#about-certora)
    - [**Scope of Audit**](#scope-of-audit)
- [**Low Severity Issues (8)**](#low-severity-issues)
  - [**L-01**](#l-01-event-not-emitted-as-indicated-in-navtrackinginsert-code-commentary)
  - [**L-02**](#l-02-issue-with-checking-past-nav-in-pool-swaps-code-contradicting-documentation)
  - [**L-03**](#l-03-issue-with-underlying-token-decimals-in-getrebalancevaluestats-function)
  - [**L-04**](#l-04-potential-precision-loss-in-lmpstrategy-returnexprice-calculation)
  - [**L-05**](#l-05-issue-with-eip-2612-deadline-compliance-in-lmpstrategy-solidity-file)
  - [**L-06**](#l-06-inconsistency-in-parameters-and-absence-of-constraints-in-validate-function)
  - [**L-07**](#l-07-lmpstrategyconfigvalidate-inconsistently-checks-for-max_nav_tracking)
  - [**L-08**](#l-08-precision-loss-in-verifylstpricegap-due-to-integer-division-in-tokemak)
- [**Mutations**](#mutations)
  - [**LMPStrategy**](#lmpstrategy)
- [**Notable Properties**](#notable-properties)
  - [**LMPStrategy**](#lmpstrategy-1)
- [**Disclaimer**](#disclaimer)

# Overview

This report encapsulates the findings from the Tokemak audit competition hosted on Hats.finance, where the community identified bugs and verified code properties to ensure the security and correctness of the system. Notably, the audit's effectiveness was further tested by introducing high-severity bugs (mutations) post-competition, assessing the resilience of the verified properties against these mutations. Detailed descriptions of these mutations, alongside top specifications identified during the contest, are provided to illustrate the audit's depth. For an in-depth analysis, including specific properties and the impact of mutations, refer to the final results here.  The final results, accessible [here](https://docs.google.com/spreadsheets/d/10qRTmvjmNyVbIyy3lG-OTMKL5KUK_RGV5MOaOjSs4jQ/edit#gid=1970712821), provide a performance overview, showcasing which participant detected each mutation. For direct access to the contributions, the [contest repository](https://github.com/certora/Tokemak-v2-core-fv) includes the top participants' work.

## Competition Details

- Duration: Feb 26 to Mar 11 2024
- Maximum Reward: $20,000
- Findings: 8 Low
- Submissions: 25
- Total Payout: $20,000 distributed among 20 participants.


## About Tokemak

Tokemak v2's Autopilot redefines liquidity provisioning by automatically optimizing Ethereum allocations across selected DEXs and stable-pools for enhanced portfolio performance. It utilizes a Composite Return Metric for dynamic optimization and an Adaptive Rebalance Constraint to ensure rebalances are cost-effective. This system facilitates auto-compounding of rewards and reduces gas costs, adjusting to market shifts to optimize liquidity returns efficiently. Autopilot's design aims for secure, optimized liquidity management in the evolving DeFi landscape. 


## About Hats Finance

Hats Finance builds autonomous security infrastructure for integration with major DeFi protocols to secure users' assets. Hats Audit Competitions revolutionize web3 project security through decentralized, competition-based bug hunting, rewarding only auditors who identify vulnerabilities. This approach efficiently uses budgets by paying for results, and attracts top talent by prioritizing the first submitter of a vulnerability, setting a new standard in decentralized web3 security.


## About Certora

Certora is a Web3 security company that provides industry-leading formal verification tools and smart contract audits. Certora’s flagship security product, Certora Prover, is a unique SaaS product which locates hard-to-find bugs in smart contracts or mathematically proves their absence. A formal verification contest is a competition where members of the community mathematically validate the accuracy of smart contracts, in return for a reward offered by the sponsor based on the participants' findings and property coverage.


## Scope of Audit

This contest focused on the Strategy portion of the codebase and the logic related to the evaluation of rebalances. This includes the following the contracts:

- `src/strategy/LMPStrategy.sol`
- `src/strategy/LMPStrategyConfig.sol`
- `src/strategy/NavTracking.sol`
- `src/strategy/ViolationTracking.sol`

Formal verification was conducted on `LMPStrategy`.

# Low Severity Issues

Issues are summarized below, follow the link for details.

## [L-01](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/1) Event Not Emitted as Indicated in `NavTracking::insert` Code Commentary

_Submitted by Pavel2202_

  The issue involves the 'NavTracking::insert' function in the Tokemak v2-core-hats project. An 'emit event' TODO is left out in the function and is not correctly executed. A proposed solution has been made to create an event and execute it at the end of the function.


## [L-02](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/4) Issue with Checking Past NAV in Pool Swaps Code Contradicting Documentation

  The issue is about a discrepancy in the contracts behaviour versus the intended behaviour as per the documentation. The point of contention is that in case all three delta values are negative, pool swaps should be paused until the NAV reaches the highest recorded value or 90 days have passed since the test, as per the document. However, as per the posted codes, the first condition is never checked, causing a difference in the expected and actual behaviour.


## [L-03](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/5) Issue with Underlying Token Decimals in getRebalanceValueStats Function

  The issue discusses an incorrect assumption in the 'getRebalanceValueStats' function where it's supposed that the underlying token for 'LMPVault' is in 18 decimals. This might not be the case as there's no enforcement in the constructor. A remedy proposed is to scale up/down 'params.amountIn/params.amountOut' based on the token decimals to achieve the right precision. A user comment suggests it's currently configured to only support WETH as the baseAsset.


## [L-04](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/10) Potential Precision Loss in LMPStrategy ReturnExPrice Calculation

  The issue highlights a potential precision loss in a line of code within the 'Tokemak/v2-core-hats' repository. The problematic part involves separate division operations during a calculation with variables 'result.baseApr', 'weightBase', 'result.feeApr', 'weightFee', 'result.incentiveApr' and 'weightIncentive'. The proposed fix suggests changing the calculation order to avoid this precision loss.


## [L-05](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/12) Issue with EIP-2612 Deadline Compliance in LMPStrategy Solidity File

  The issue highlights a discrepancy from the EIP-2612 specification that states signatures should be allowed on the exact deadline timestamp. The problem encountered in the LMPStrategy.sol file is all about timestamp validation where it's suggested to consider whether it makes more sense to include the expiration timestamp as a valid timestamp, as currently done for deadlines.


## [L-06](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/19) Inconsistency in Parameters and Absence of Constraints in Validate Function

_Submitted by lucasts95_

  The `validate` function lacks verification for certain parameters, leading to inconsistencies with the documentation. Parameters like `minInDays`, `maxInDays`, `relaxStepInDays`, `relaxThresholdInDays`, and `tightenStepInDays` as defined in the test files are not in line with their declarations. To maintain code consistency and stability, it's suggested to declare parameters with expected data values as constants. This property was identified by using Certora prover. The relevant properties can are [offsetEdges](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora-luckypatty/specs/LMPStrategy_8.spec#L133-L134), [decreaseByThree](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora-luckypatty/specs/LMPStrategy_9.spec#L147-L161), and [swapCostOffsetPeriodIncreaseByOne](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora-luckypatty/specs/LMPStrategy_10.spec#L147-L154).


## [L-07](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/22) LMPStrategyConfig.validate Inconsistently Checks for MAX_NAV_TRACKING

_Submitted by 0xRizwan_

  The issue lies in the '30-60-90 NAV Test or LookBack Test', which monitors swapping costs. It was found that the maximum number of tracked days is 91, contradicting the specified maximum of 90 days. This error occurs because 'config.navLookback.lookback3InDays' only considers values greater than 'MAX_NAV_TRACKING', thus including 91. It is recommended to replace ">" with ">=" to correctly check 'config.navLookback.lookback3InDays' against 'MAX_NAV_TRACKING'.


## [L-08](https://github.com/hats-finance/Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b/issues/23) Precision Loss in `verifyLSTPriceGap()` Due to Integer Division in Tokemak

_Submitted by MatinR1_

  The function `verifyLSTPriceGap()` in the Tokemak-0x4a2d708ea6b0c04186ecb774cfad1e50fb5efc0b project is designed to calculate the largest difference between spot & safe prices for the underlying tokens. However, due to the rounding down nature of the Solidity, the function's output suffers from precision loss leading to an inaccurate result. The function allows the execution to proceed even when it exceeds the allowed tolerance limit due to the precision issues, which could potentially pose a vulnerability threat. A refactored formula was offered to eliminate this issue.

# Mutations

## LMPStrategy

[**LMPStrategy_0.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_0.sol): Add a public function which allows anyone to tighten `_swapCostOffsetPeriod`.

[**LMPStrategy_1.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_1.sol): In `validateRebalanceParams`, fail to ensure that `destinationOut` is registered.

[**LMPStrategy_2.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_2.sol): Change `clearExpiredPause` from internal to public.

[**LMPStrategy_3.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_3.sol): In `clearExpiredPause`, set `lastPausedTimestamp` to `block.timestamp` instead of 0.

[**LMPStrategy_4.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_4.sol): In `navUpdate`, call `getDaysAgo` with 0 input, causing the strategy to pause whenever there's any NAV decay.

[**LMPStrategy_5.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_5.sol): In `verifyRebalance`, add an unchecked block around `predictedGainAtOffsetEnd` calculation, allowing an overflow.

[**LMPStrategy_6.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_6.sol): In `verifyLSTPriceGap`, replace `params.destinationOut != address(lmpVault)` with `true`, causing a DoS whenever `params.destinationOut == address(lmpVault)`.

[**LMPStrategy_7.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_7.sol): In `getRebalanceValueStats`, replace `outEthValue == 0` with `true` during slippage calculation, causing slippage to always be set to 0.

[**LMPStrategy_8.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_8.sol): In `getRebalanceValueStats`, switch local decimal definitions for `tokenIn` and `tokenOut`.

[**LMPStrategy_9.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_9.sol): In `verifyRebalance`, negate `predictedGainAtOffsetEnd`, causing high gain to be denied and negative gain to be allowed.

[**LMPStrategy_10.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_10.sol): In `verifyRebalance`, square `swapOffsetPeriod` instead of halving it when `tokenIn == tokenOut`.

[**LMPStrategy_P0.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_P0.sol): In `getRebalanceValueStats`, replace `params.destinationOut != lmpVaultAddress` with `true`, causing a DoS when `params.destinationOut == lmpVaultAddress`

[**LMPStrategy_P1.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_P1.sol): In `verifyLSTPriceGap`, fail to divide by scaler in tolerance calculation.

[**LMPStrategy_P2.sol**](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora/mutations/LMPStrategy/LMPStrategy_P2.sol): In `verifyRebalanceToIdle`, nullify all scenarios by setting `maxSlippage` to 0.

# Notable Properties

## LMPStrategy

### `lastRebalanceTimestamp` must only be updated to `block.timestamp`.

*Author:* [alexzoid-eth](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora-alexzoid-eth/specs/LMPStrategy.spec#L372-L382)

```
rule lastRebalanceTimestampTransition(env e, method f, calldataarg args) 
    filtered { f -> f.selector == sig:rebalanceSuccessfullyExecuted(IStrategy.RebalanceParams).selector } {

    uint40 before = lastRebalanceTimestamp();

    f(e, args);

    uint40 after = lastRebalanceTimestamp();

    assert(before != after => after == require_uint40(e.block.timestamp));
}
```

### `lastRebalanceTimestamp` must only be changeable by `LMPVault`.

*Author:* [0xArion](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora-Arion0x/specs/LMPStrategy.spec#L364-L373)

```
rule onlyLMPCanChangeLastRebalanceTimestamp(env e, method f, calldataarg args){

    uint40 timeBefore = lastRebalanceTimestampGhost;

    f(e, args);

    uint40 timeAfter = lastRebalanceTimestampGhost;

    assert((timeAfter != timeBefore) => callerIsLMP(e.msg.sender));
}
```

### `rebalanceSuccessfullyExecuted` must have non-reverting paths.

*Author:* [luckypatty](https://github.com/Certora/tokemak-v2-core-fv/blob/main/certora-luckypatty/specs/LMPStrategy_7.spec#L146-L150)

```
rule swapCostOffsetPeriodMaxReachable(env e){
    calldataarg args;
    rebalanceSuccessfullyExecuted(e, args);
    satisfy(_swapCostOffsetPeriodGhost == swapCostOffsetMaxInDays());
}
```

## Disclaimer


This report does not assert that the audited contracts are completely secure. Continuous review and comprehensive testing are advised before deploying critical smart contracts.


The Tokemak audit competition illustrates the collaborative effort in identifying and rectifying potential vulnerabilities, enhancing the overall security and functionality of the platform.


Hats.finance does not provide any guarantee or warranty regarding the security of this project. Smart contract software should be used at the sole risk and responsibility of users.


Certora does not provide a warranty of any kind, explicit or implied. The contents of this report should not be construed as a complete guarantee that the contract is secure in all dimensions. In no event shall Certora or any of its employees or community participants be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the results reported here. All smart contract software should be used at the sole risk and responsibility of users.