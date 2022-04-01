// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;

interface IUserProxyFactory {
    function createAndGetUserProxy(address) external returns (address);

    function oxLensAddress() external view returns (address);

    function userProxyByAccount(address) external view returns (address);

    function userProxyByIndex(uint256) external view returns (address);

    function userProxyInterfaceAddress() external view returns (address);

    function userProxiesLength() external view returns (uint256);

    function isUserProxy(address) external view returns (bool);
}
