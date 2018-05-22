module.exports = {
  networks: {
    development: {
      host: "localhost",
      port: 7545,
      network_id: "*" // Match any network id
    },
    live: {
      host: "127.0.0.1", // via ssh tunnel
      port: 48545,
      network_id: 4 // rinkeby
    }
  }
};
