const Web3 = require('web3');

let web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8042'));

let abi = [{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"details","outputs":[{"name":"name","type":"string"},{"name":"district","type":"string"},{"name":"age","type":"uint256"},{"name":"image","type":"string"},{"name":"orphanName","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"name","type":"bytes32"},{"indexed":false,"name":"district","type":"bytes32"},{"indexed":false,"name":"age","type":"bytes32"},{"indexed":false,"name":"orphanName","type":"bytes32"}],"name":"AddChild","type":"event"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"district","type":"string"},{"name":"age","type":"uint256"},{"name":"image","type":"string"},{"name":"orphanName","type":"string"}],"name":"addDetails","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"name","type":"string"}],"name":"getDetail","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"uint256"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}];
let adr = '0x9874887c9cabebf0a9bd63e1feb55e4f4ea127b6';
let contract = web3.eth.contract(abi).at(adr);

web3.eth.defaultAccount = web3.eth.accounts[0];

function addDetails(name, district, age, image, orphanName) {
  contract.addDetails(name, district, age, image, orphanName);
}

function getDetail(name) {
  return contract.getDetail.call('name');
}

module.exports = {
  addDetails: addDetails,
  getDetail: getDetail
};

// console.log(addDetails('test', 'test district', 8, 'etst image', 'test orphan'));
console.log(getDetail('test'));