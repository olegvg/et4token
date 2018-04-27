var Et4Token = artifacts.require("Et4Token");

contract('Et4Token', function(accounts) {
  it("should put 10000000 MetaCoin in total supply", function() {
    return Et4Token.deployed().then(function(instance) {
      return instance.totalSupply.call();
    }).then(function(balance) {
      assert.equal(balance.valueOf(), 10000000, "10000000 wasn't supplied in total");
    });
  })});
