{ system ? builtins.currentSystem, pkgs ? import ./nix { inherit system; } }:
let
  released = (import (builtins.fetchTarball "https://github.com/crypto-org-chain/chain-main/archive/v3.1.0.tar.gz") { }).chain-maind;
  
  
in pkgs.mkShell rec {
  name = "chainmain";
  buildInputs = [
    released
  ];
}