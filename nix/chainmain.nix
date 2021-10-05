{pkgs ? import ./default.nix {} }:
let
  released = (import (builtins.fetchTarball "https://github.com/crypto-org-chain/chain-main/archive/v2.1.2.tar.gz") { }).chain-maind;
in
 pkgs.symlinkJoin {
    name = "chainmain";
    paths = [ released ];
 }