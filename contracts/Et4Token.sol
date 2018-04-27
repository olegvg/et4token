pragma solidity ^0.4.23;

import "openzeppelin-solidity/contracts/math/SafeMath.sol";
import "openzeppelin-solidity/contracts/token/ERC20/MintableToken.sol";
import "openzeppelin-solidity/contracts/token/ERC20/BurnableToken.sol";

contract ET4Token is MintableToken, BurnableToken {
    using SafeMath for uint;

    string public symbol;
    string public  name;
    uint8 public decimals;

    constructor(uint256 _initialAmount) public {
      symbol = "ET4";
      name = "Eticket4 Token";
      decimals = 18;
      totalSupply_ = _initialAmount;
      balances[owner] = totalSupply_;
      /* emit Transfer(address(0), owner, totalSupply_); */
    }
}
