// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SecureMessaging {

    struct User {
        string publicKey;
        bool exists;
    }

    struct MessageLog {
        address sender;
        address receiver;
        string hash;
        uint256 timestamp;
    }

    mapping(address => User) public users;
    MessageLog[] public logs;

    event UserRegistered(address user);
    event MessageLogged(address sender, address receiver, string hash);

    function registerUser(string memory _publicKey) public {
        require(!users[msg.sender].exists, "Already registered");
        users[msg.sender] = User(_publicKey, true);
        emit UserRegistered(msg.sender);
    }

    function logMessage(address _receiver, string memory _hash) public {
        require(users[msg.sender].exists, "Sender not registered");
        require(users[_receiver].exists, "Receiver not registered");

        logs.push(MessageLog(msg.sender, _receiver, _hash, block.timestamp));
        emit MessageLogged(msg.sender, _receiver, _hash);
    }

    function getMessageCount() public view returns (uint256) {
        return logs.length;
    }
}
