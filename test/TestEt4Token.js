var Et4Token = artifacts.require("Et4Token");

contract('Et4Token test', async (accounts) => {
  var account1 = accounts[1];
  var account2 = accounts[2];
  var account3 = accounts[3];
  var account4 = accounts[4];
  var account5 = accounts[5];
  var account6 = accounts[6];
  var account7 = accounts[7];
  var account8 = accounts[8];
  var account9 = accounts[9];

  it("should put 10000000 ET4 coins in total supply", async () => {
    let instance = await Et4Token.deployed();

    let balance = await instance.totalSupply.call();
    assert.equal(balance.valueOf(), 10000000, "10000000 wasn't supplied in total");
  });

  it("should put 20000 ET4 tokens on account2", async () => {
    let instance = await Et4Token.deployed();

    await instance.transfer(account2, 20000);

    let balance = await instance.balanceOf.call(account2);
    assert.equal(balance.valueOf(), 20000, "20000 wasn't put");
  });

  it("should put 200 ET4 tokens from account2 to escrow in favor of address3 then release escrow", async () => {
    let instance = await Et4Token.deployed();

    await instance.startEscrow('1234567', account3, 200, {from: account2});
    let balance2 = await instance.balanceOf.call(account2);
    assert.equal(balance2.valueOf(), 19800, "balance of a source account2 must be exactly 19800");

    await instance.releaseEscrow('1234567', account9);
    let balance3 = await instance.balanceOf.call(account3);
    assert.equal(balance3.valueOf(), 192, "balance of a target account3 must be exactly 192");
    let balance9 = await instance.balanceOf.call(account9);
    assert.equal(balance9.valueOf(), 8, "balance of a fee account9 must be exactly 8");
  });

  it("should put 400 ET4 tokens from account2 to escrow in favor of address4 then cancel escrow", async () => {
    let instance = await Et4Token.deployed();

    await instance.startEscrow('7654321', account4, 400, {from: account2});
    let balance2 = await instance.balanceOf.call(account2);
    assert.equal(balance2.valueOf(), 19400, "balance of a source account2 must be exactly 19400");

    await instance.cancelEscrow('7654321');
    balance2 = await instance.balanceOf.call(account2);
    assert.equal(balance2.valueOf(), 19800, "balance of a source account2 must be exactly 19800");
    let balance4 = await instance.balanceOf.call(account4);
    assert.equal(balance4.valueOf(), 0, "balance of a fee account4 must be exactly 0");
  });
});
