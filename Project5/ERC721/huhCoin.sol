pragma solidity ^0.8.0;

import "workspaces/BlockChain_cs646/Project5/ERC721/ERC721.sol"

contract huhCoin is ERC721{
        address owner;
        uint256 cost = 10**16; //10000000000000000
    constructor() ERC721("usrname","usr"){
        owner = msg.sender;
    }
  function mint(uint256 amount)public payable  {
       uint256 val = amount * cost;
       require(val == msg.value,"incorrect amount"); 
        _mint(msg.sender, amount);
    }

    function withdraw() public payable {
        require(msg.sender == owner,"not owner");
        (bool success,) = payable (msg.sender).call{
            value:address(this).balance
        }("");
        require(success);
        }
    }