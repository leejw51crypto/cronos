{pkgs ? import ./default.nix {} }:
let
  released = (import (builtins.fetchTarball "https://github.com/crypto-org-chain/chain-main/archive/v3.1.1.tar.gz") { }).chain-maind;
in
 pkgs.symlinkJoin {
    name = "chainmain";
    paths = [ released ];
 }