pragma solidity ^0.4.23;

import "openzeppelin-solidity/contracts/math/SafeMath.sol";
import "openzeppelin-solidity/contracts/token/ERC20/MintableToken.sol";
import "openzeppelin-solidity/contracts/token/ERC20/BurnableToken.sol";

contract ET4Token is MintableToken, BurnableToken {
    using SafeMath for uint256;

    string public symbol;
    string public  name;
    uint8 public decimals;

    /* Numerator and denominator of common fraction.
    E.g. 1 & 25 mean one twenty fifths, i.e. 0.04 = 4% */
    uint256 public escrow_fee_numerator; /* 1 */
    uint256 public escrow_fee_denominator; /* 25 */

    struct EscrowElement {
      bool exists;
      address src;
      address dst;
      uint256 value;
    }
    /* escrow_id => EscrowElement struct */
    mapping (bytes20 => EscrowElement) escrows;

    event EscrowStarted(
      bytes20 indexed escrow_id,
      EscrowElement escrow_element
    );

    event EscrowReleased(
      bytes20 indexed escrow_id,
      EscrowElement escrow_element
    );

    event EscrowCancelled(
      bytes20 indexed escrow_id,
      EscrowElement escrow_element
    );

    constructor(uint256 _initialAmount) public {
      symbol = "ET4";
      name = "Eticket4 Token";
      decimals = 18;
      totalSupply_ = _initialAmount;
      escrow_fee_numerator = 1;
      escrow_fee_denominator = 25;

      balances[owner] = totalSupply_;
      emit Transfer(address(0), owner, totalSupply_);
    }

    function startEscrow(bytes20 escrow_id, address to, uint256 value) public returns (bool) {
      require(to != address(0));
      require(value <= balances[msg.sender]);
      require(escrows[escrow_id].exists != true);

      balances[msg.sender] = balances[msg.sender].sub(value);
      EscrowElement memory escrow_element = EscrowElement(true, msg.sender, to, value);
      escrows[escrow_id] = escrow_element;

      emit EscrowStarted(escrow_id, escrow_element);

      return true;
    }

    function releaseEscrow(bytes20 escrow_id, address fee_destination) public returns (bool) {
      require(fee_destination != address(0));
      require(escrows[escrow_id].exists == true);

      EscrowElement storage escrow_element = escrows[escrow_id];

      uint256 fee = escrow_element.value.mul(escrow_fee_numerator).div(escrow_fee_denominator);
      uint256 value = escrow_element.value.sub(fee);

      require(value == 192);

      balances[escrow_element.dst] = balances[escrow_element.dst].add(value);
      balances[fee_destination] = balances[fee_destination].add(fee);

      /* Workaround because of lack of feature. See https://github.com/ethereum/solidity/issues/3577 */
      EscrowElement memory _escrow_element = escrow_element;
      emit EscrowReleased(escrow_id, _escrow_element);

      delete escrows[escrow_id];

      return true;
    }

    function cancelEscrow(bytes20 escrow_id) public returns (bool) {
      EscrowElement storage escrow_element = escrows[escrow_id];

      balances[escrow_element.src] = balances[escrow_element.src].add(escrow_element.value);

      /* Workaround because of lack of feature. See https://github.com/ethereum/solidity/issues/3577 */
      EscrowElement memory _escrow_element = escrow_element;
      emit EscrowCancelled(escrow_id, _escrow_element);

      delete escrows[escrow_id];

      return true;
    }
}
