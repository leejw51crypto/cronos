{ system ? builtins.currentSystem, pkgs ? import ./nix { inherit system; } }:
pkgs.buildGoApplication rec {
  pname = "chainmain";
  version = "0.5.2";
  src = ../chain-main;
  modules = ../chain-main/gomod2nix.toml;
  pwd = src; # needed to support replace
  subPackages = [ "../chain-main/cmd/chain-maind" ];
  CGO_ENABLED = "1";
  buildFlagsArray = ''
    -ldflags=
    -X github.com/cosmos/cosmos-sdk/version.Name=chainmain
    -X github.com/cosmos/cosmos-sdk/version.AppName=${pname}
    -X github.com/cosmos/cosmos-sdk/version.Version=${version}
  '';
}
