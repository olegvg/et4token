var SafeMath = artifacts.require("openzeppelin-solidity/contracts/math/SafeMath");
var Et4Token = artifacts.require("Et4Token");

module.exports = function(deployer) {
  deployer.deploy(SafeMath);
  deployer.link(SafeMath, Et4);
  deployer.deploy(Et4Token, 10000000);
};
