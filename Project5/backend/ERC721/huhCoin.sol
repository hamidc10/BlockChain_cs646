pragma solidity ^0.8.0;

import "workspaces/BlockChain_cs646/Project5/ERC721/ERC721.sol"

contract huhCoin is ERC721{
        address owner;
        uint256 cost = 10**16; //10000000000000000
    constructor() ERC721("usrname","usr"){
        owner = NFT.holder;
    }
  function mint(uint256 amount)public payable  {
       uint256 val = amount * cost;
       require(val == NFT.value,"incorrect amount"); 
        _mint(NFT.holder, amount);
    }

    function withdraw() public payable {
        require(NFT.holder == owner,"not owner");
        (bool success,) = payable (NFT.holder).call{
            value:address(this).balance
        }("");
        require(success);
        }
    }