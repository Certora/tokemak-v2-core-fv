// SPDX-License-Identifier: UNLICENSED
// Copyright (c) 2023 Tokemak Foundation. All rights reserved.

pragma solidity 0.8.17;

// solhint-disable func-name-mixedcase

import { Test } from "forge-std/Test.sol";
import { TELLOR_ORACLE, RETH_MAINNET, RETH_CL_FEED_MAINNET } from "test/utils/Addresses.sol";

import { TellorOracle, BaseOracleDenominations } from "src/oracles/providers/TellorOracle.sol";
import { ISystemRegistry } from "src/interfaces/ISystemRegistry.sol";
import { IRootPriceOracle } from "src/interfaces/oracles/IRootPriceOracle.sol";
import { Errors } from "src/utils/Errors.sol";

contract TellorOracleTest is Test {
    // Eth - usd query id
    bytes32 public constant QUERY_ID = 0x83a7f3d48786ac2667503a61e8c415438ed2922eb86a2906e4ee66d9a2ce4992;
    // 10k Eth, should never return higher as Eth has never cost this much at pinned blocks.
    uint256 public constant ETH_MAX_USD = 10_000_000_000_000_000_000_000;
    address public constant ETH = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    IRootPriceOracle private _rootPriceOracle;
    ISystemRegistry private _systemRegistry;
    TellorOracle public _oracle;

    event TellorRegistrationAdded(address token, BaseOracleDenominations.Denomination, bytes32 _queryId);
    event TellorRegistrationRemoved(address token, bytes32 queryId);

    function setUp() external {
        vm.createSelectFork(vm.envString("MAINNET_RPC_URL"));

        _rootPriceOracle = IRootPriceOracle(vm.addr(324));
        _systemRegistry = _generateSystemRegistry(address(_rootPriceOracle));
        _oracle = new TellorOracle(TELLOR_ORACLE, _systemRegistry);

        vm.makePersistent(address(_systemRegistry));
    }

    // Test `addTellorRegistration()`.
    function test_RevertNonOwnerQueryId() external {
        vm.expectRevert("Ownable: caller is not the owner");
        vm.prank(address(3));

        _oracle.addTellorRegistration(address(1), bytes32("Test Bytes"), BaseOracleDenominations.Denomination.ETH, 0);
    }

    function test_ZeroAddressRevert_AddTellorRegistration() external {
        vm.expectRevert(abi.encodeWithSelector(Errors.ZeroAddress.selector, "tokenForQueryId"));

        _oracle.addTellorRegistration(address(0), bytes32("Test Bytes"), BaseOracleDenominations.Denomination.ETH, 0);
    }

    function test_ZeroBytesRevert_AddTellorRegistration() external {
        vm.expectRevert(abi.encodeWithSelector(Errors.InvalidParam.selector, "queryId"));

        _oracle.addTellorRegistration(address(1), bytes32(0), BaseOracleDenominations.Denomination.ETH, 0);
    }

    function test_RevertAlreadySet_AddTellorRegistration() external {
        _oracle.addTellorRegistration(address(1), bytes32("Test Bytes"), BaseOracleDenominations.Denomination.ETH, 0);

        vm.expectRevert(Errors.MustBeZero.selector);

        _oracle.addTellorRegistration(address(1), bytes32("Test Bytes 2"), BaseOracleDenominations.Denomination.ETH, 0);
    }

    function test_ProperAddTellorRegistration() external {
        vm.expectEmit(false, false, false, true);
        emit TellorRegistrationAdded(address(1), BaseOracleDenominations.Denomination.ETH, bytes32("Test Byte"));

        _oracle.addTellorRegistration(address(1), bytes32("Test Byte"), BaseOracleDenominations.Denomination.ETH, 0);

        assertEq(_oracle.getQueryInfo(address(1)).queryId, bytes32("Test Byte"));
    }

    // Test `removeTellorRegistration()`
    function test_RevertZeroAddressToken_RemoveTellorRegistration() external {
        vm.expectRevert(abi.encodeWithSelector(Errors.ZeroAddress.selector, "tokenToRemoveRegistration"));

        _oracle.removeTellorRegistration(address(0));
    }

    function test_QueryIdZeroBytes_RemoveTellorRegistration() external {
        vm.expectRevert(abi.encodeWithSelector(Errors.InvalidParam.selector, "queryIdBeforeDeletion"));

        _oracle.removeTellorRegistration(address(1));
    }

    function test_ProperRemoveTellorRegistration() external {
        _oracle.addTellorRegistration(address(1), bytes32("Test Bytes"), BaseOracleDenominations.Denomination.ETH, 0);

        assertEq(_oracle.getQueryInfo(address(1)).queryId, bytes32("Test Bytes"));

        vm.expectEmit(false, false, false, true);
        emit TellorRegistrationRemoved(address(1), bytes32("Test Bytes"));

        _oracle.removeTellorRegistration(address(1));

        assertEq(_oracle.getQueryInfo(address(1)).queryId, bytes32(0));
    }

    // test `getPrice()`
    function test_GetPriceMainnet() external {
        vm.createSelectFork(vm.envString("MAINNET_RPC_URL"), 17_100_000);

        TellorOracle mainnet = new TellorOracle(TELLOR_ORACLE, _systemRegistry);
        mainnet.addTellorRegistration(ETH, QUERY_ID, BaseOracleDenominations.Denomination.ETH, 0);

        vm.prank(address(1));
        uint256 returnedPrice = mainnet.getPriceInEth(ETH);

        assertGt(returnedPrice, 0);
        assertLt(returnedPrice, ETH_MAX_USD);
    }

    function test_GetPriceOptimism() external {
        vm.createSelectFork(vm.envString("OPTIMISM_MAINNET_RPC_URL"), 90_000_000);

        TellorOracle optimism = new TellorOracle(TELLOR_ORACLE, _systemRegistry);
        optimism.addTellorRegistration(ETH, QUERY_ID, BaseOracleDenominations.Denomination.ETH, 0);

        vm.prank(address(1));

        uint256 returnedPrice = optimism.getPriceInEth(ETH);

        assertGt(returnedPrice, 0);
        assertLt(returnedPrice, ETH_MAX_USD);
    }

    function test_GetPriceArbitrum() external {
        vm.createSelectFork(vm.envString("ARBITRUM_MAINNET_RPC_URL"), 80_000_000);

        TellorOracle arbitrum = new TellorOracle(TELLOR_ORACLE, _systemRegistry);
        arbitrum.addTellorRegistration(ETH, QUERY_ID, BaseOracleDenominations.Denomination.ETH, 48 hours);

        vm.prank(address(1));

        uint256 returnedPrice = arbitrum.getPriceInEth(ETH);

        assertGt(returnedPrice, 0);
        assertLt(returnedPrice, ETH_MAX_USD);
    }

    function _generateSystemRegistry(address rootOracle) internal returns (ISystemRegistry) {
        address registry = vm.addr(327_849);
        vm.mockCall(registry, abi.encodeWithSelector(ISystemRegistry.rootPriceOracle.selector), abi.encode(rootOracle));
        return ISystemRegistry(registry);
    }
}