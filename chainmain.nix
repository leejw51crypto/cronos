{ system ? builtins.currentSystem, pkgs ? import ./nix { inherit system; } }:
pkgs.buildGoApplication rec {
  pname = "chain-main";
  version = "0.0.0";
  src = ./integration_tests/chain-main;
  modules = ./integration_tests/chain-main/gomod2nix.toml;
  pwd = src; # needed to support replace
  subPackages = [ "cmd/chain-maind" ];
  CGO_ENABLED = "1";
  buildFlagsArray = ''
    -ldflags=
    -X github.com/cosmos/cosmos-sdk/version.Name=chainmain
    -X github.com/cosmos/cosmos-sdk/version.AppName=${pname}
    -X github.com/cosmos/cosmos-sdk/version.Version=${version}
  '';
}
