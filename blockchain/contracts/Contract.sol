pragma solidity ^0.4.17;

contract Contract {
    struct ChildInfo {
        string name;
        string district;
        uint age;
        string image;
        string orphanName;
    }

    ChildInfo[] public details;

   event AddChild(bytes32 name, bytes32 district, bytes32 age, bytes32 orphanName);

    function addDetails(string name, string district, uint age, string image, string orphanName) public {
        details.push(ChildInfo({
            name: name,
            district: district,
            age: age,
            image: image,
            orphanName: orphanName
        }));
    }

    function getDetail(string name) public view returns (string, string, uint,
                                                    string, string) {
        for (uint i = 0; i < details.length; i++) {
            if (keccak256(name) == keccak256(name)) {
                return (
                    details[i].name, details[i].district, details[i].age, details[i].image, details[i].orphanName
                );
            }
        }
    }
}