// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity >=0.8.7;

import "./IPlasmaPool.sol";

/**
 * @title PlasmaPool Router Base Interface
 * @notice A canonical router between PlasmaPools
 *
 * The base router is a multicall style router inspired by Uniswap v3 with built-in features for permit,
 * WETH9 wrap/unwrap, and ERC20 token pulling/sweeping/approving. It includes methods for the four mutable
 * ERC4626 functions deposit/mint/withdraw/redeem as well.
 *
 * These can all be arbitrarily composed using the multicall functionality of the router.
 *
 * NOTE the router is capable of pulling any approved token from your wallet. This is only possible when
 * your address is msg.sender, but regardless be careful when interacting with the router or ERC4626 Vaults.
 * The router makes no special considerations for unique ERC20 implementations such as fee on transfer.
 * There are no built in protections for unexpected behavior beyond enforcing the minSharesOut is received.
 */
interface IPlasmaPoolRouterBase {
    /// @notice thrown when amount of assets received is below the min set by caller
    error MinAmountError();

    /// @notice thrown when amount of shares received is below the min set by caller
    error MinSharesError();

    /// @notice thrown when amount of assets received is above the max set by caller
    error MaxAmountError();

    /// @notice thrown when amount of shares received is above the max set by caller
    error MaxSharesError();

    /**
     * @notice mint `shares` from an ERC4626 vault.
     * @param pool The PlasmaPool to mint shares from.
     * @param to The destination of ownership shares.
     * @param shares The amount of shares to mint from `vault`.
     * @param maxAmountIn The max amount of assets used to mint.
     * @return amountIn the amount of assets used to mint by `to`.
     * @dev throws MaxAmountError
     */
    function mint(
        IPlasmaPool pool,
        address to,
        uint256 shares,
        uint256 maxAmountIn
    ) external payable returns (uint256 amountIn);

    /**
     * @notice deposit `amount` to an ERC4626 vault.
     * @param pool The PlasmaPoolt to deposit assets to.
     * @param to The destination of ownership shares.
     * @param amount The amount of assets to deposit to `vault`.
     * @param minSharesOut The min amount of `vault` shares received by `to`.
     * @return sharesOut the amount of shares received by `to`.
     * @dev throws MinSharesError
     */
    function deposit(
        IPlasmaPool pool,
        address to,
        uint256 amount,
        uint256 minSharesOut
    ) external payable returns (uint256 sharesOut);

    /**
     * @notice withdraw `amount` from an ERC4626 vault.
     * @param pool The PlasmaPool to withdraw assets from.
     * @param to The destination of assets.
     * @param amount The amount of assets to withdraw from vault.
     * @param minSharesOut The min amount of shares received by `to`.
     * @return sharesOut the amount of shares received by `to`.
     * @dev throws MaxSharesError
     */
    function withdraw(
        IPlasmaPool pool,
        address to,
        uint256 amount,
        uint256 minSharesOut
    ) external payable returns (uint256 sharesOut);

    /**
     * @notice redeem `shares` shares from a PlasmaPool
     * @param pool The PlasmaPool to redeem shares from.
     * @param to The destination of assets.
     * @param shares The amount of shares to redeem from vault.
     * @param minAmountOut The min amount of assets received by `to`.
     * @return amountOut the amount of assets received by `to`.
     * @dev throws MinAmountError
     */
    function redeem(
        IPlasmaPool pool,
        address to,
        uint256 shares,
        uint256 minAmountOut
    ) external payable returns (uint256 amountOut);
}