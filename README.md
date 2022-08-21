## Modified Mercle-Patricia Tree
This repository is a python implementation of a MPT. Most the used code was copied from [here](https://github.com/popzxc/merkle-patricia-trie/blob/master/LICENSE) under [MIT licence]('\\docs'). 

IMPORTANT: This code is by no means secure, I am not a software developer or security specialist. If you see any security issues or want to improve the code, please create an issue or a pull-request if you know a good fix. If you have ideas for new functions you can also create a new issue. I do not garantie that I will solve the issues because this is a hobby project and I don't always have the time, but all help is welcome.

### Explanations
It took me quite a while to understand what a MPT is and how it can be used.
These are some usefull guides
- [Data structure in Ethereum | Episode 1+: Compact (Hex-prefix) encoding.](https://medium.com/coinmonks/data-structure-in-ethereum-episode-1-compact-hex-prefix-encoding-12558ae02791)
- [Data structure in Ethereum | Episode 2: Radix trie and Merkle trie.](https://medium.com/coinmonks/data-structure-in-ethereum-episode-2-radix-trie-and-merkle-trie-d941d0bfd69a)
- [Data structure in Ethereum | Episode 3: Patricia trie.](https://medium.com/coinmonks/data-structure-in-ethereum-episode-3-patricia-trie-b7b0ccddd32f)
- [MPT implementation](https://medium.com/codechain/modified-merkle-patricia-trie-how-ethereum-saves-a-state-e6d7555078dd)

### Installation
The biggest chance for a stable library is using one of the releases on the releases branch. If there are no releases or none that fit you, try the nightly releases or build your own wheel file with the provided files in the repo. Watch out when using nightly releases, this branch is used for adding experimental functions and may not work as expected.

### Licence
[Licence](https://github.com/Nynra/pympt/blob/nightly/LICENSE)

### Sources
This repo is heavily inspired by other MPT projects:
- [popzxc/merkle-patricia-trie](https://github.com/popzxc/merkle-patricia-trie)
- [Tierion/pymerkletools](https://github.com/Tierion/pymerkletools)
