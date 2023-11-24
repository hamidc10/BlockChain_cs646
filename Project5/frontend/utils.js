const messageBoardContract ="0xdC93412182b2fBf68b4282255d772d6Cd01fE8A1"
const erc20contract="0xE8582B0840303a3F70B9acc26ff05581dFe6B0bD"
const erc20ABI=
[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "subtractedValue",
				"type": "uint256"
			}
		],
		"name": "decreaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "addedValue",
				"type": "uint256"
			}
		],
		"name": "increaseAllowance",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "mint",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

const messageboardABI =
[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_mymessage",
				"type": "string"
			}
		],
		"name": "addmessage",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_size",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_newSize",
				"type": "uint256"
			}
		],
		"name": "updateMaxSize",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "getaddress",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getmaxsize",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_index",
				"type": "uint256"
			}
		],
		"name": "getmessage",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]




var myweb3;

/* To connect using MetaMask */
async function connect() {
   
   if (window.ethereum) {
    await window.ethereum.request({ method: "eth_requestAccounts" });
    window.web3 = new Web3(window.ethereum);
    myweb3= window.web3
    return myweb3;
   } 
   else{
   
   }
  }

  async function getTheMaxSize() {
        console.log("test")
        accounts = await ethereum.request({ method: 'eth_requestAccounts' });
        account = accounts[0];
    //	web3 = new Web3(window.ethereum);
        contract = new myweb3.eth.Contract(messageboardABI, messageBoardContract);
        // var value = web3.utils.toWei("1200", "ether");
        var myresult = await contract.methods.getmaxsize().call({"from":account})
        console.log(myresult);
        return myresult;
    //
 
 }
 async function getMessage(index) {

    accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    account = accounts[0];
//	web3 = new Web3(window.ethereum);
    contract = new myweb3.eth.Contract(messageboardABI, messageBoardContract);
    // var value = web3.utils.toWei("1200", "ether");
    var myresult = await contract.methods.getmessage(index).call({"from":account})
    console.log(myresult);
    return myresult;
//

}

async function getAddress(index) {

    accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    account = accounts[0];
//	web3 = new Web3(window.ethereum);
    contract = new myweb3.eth.Contract(messageboardABI, messageBoardContract);
    // var value = web3.utils.toWei("1200", "ether");
    var myresult = await contract.methods.getaddress(index).call({"from":account})
    console.log(myresult);
    return myresult;
//

}

async function updateMessage(text) {

    accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    account = accounts[0];
//	web3 = new Web3(window.ethereum);
    contract = new myweb3.eth.Contract(messageboardABI, messageBoardContract);
    // var value = web3.utils.toWei("1200", "ether");
     await contract.methods.addmessage(text).send({"from":account})
    
//

}

async function mint(){
    accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    account = accounts[0];
//	web3 = new Web3(window.ethereum);
    contract = new myweb3.eth.Contract(erc20ABI, erc20contract);
    // var value = web3.utils.toWei("1200", "ether");
    // 10000000000000000
    var val = 10000000000000000
     await contract.methods.mint(1).send({"from":account, "value":val})
}

function displayalert() {
    alert("Thank you for your purchase of the HUH token? ");
}

function displaylog(){
    console.log("This Message is in the Log")
}

function displaytextalert(){
    var element = document.getElementById("mytext");
    var text = element.value;
    alert(text);
}

function updatePage(){
    var element = document.getElementById("mytext");
    var text = element.value;
    var element2 = document.getElementById("myspan");
    element2.innerText=text
}

async function updateMaxSize(){
    var text = await getTheMaxSize();
    var element2 = document.getElementById("sizespan");
    element2.innerText=text
}

async function displayMessages(){
    var main = document.getElementById("main"); 
    for(var i = 0; i<5; i++){
        
        var mydiv2 = document.createElement("div");
        mydiv2.innerHTML= "Message From "+    await getAddress(i) + " : " +  await getMessage(i);
        main.appendChild(mydiv2);
     
    }
}
async function newMessage(){
    var element = document.getElementById("mytext");
    var text = element.value;
    await updateMessage(text)
    window.location.reload();

}
async function startup(){
    await connect();
    await updateMaxSize();
    await displayMessages();
}

startup();