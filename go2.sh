NETWORK=testnet COSMOS_BUILD_OPTIONS=rocksdb make build
cp ./build/cronosd $HOME/.local/bin
install_name_tool -add_rpath $HOME/.local/lib/ $HOME/.local/bin/cronosd
