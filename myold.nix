{ system ? builtins.currentSystem, pkgs ? import ./nix { inherit system; } }:
pkgs.buildGoApplication rec {
  pname = "chainmain";
  version = "0.1";
  src = ../chain-main;
  subPackages = [ "../chain-main/cmd/chain-maind" ];
  CGO_ENABLED = "1";
  modules = ../chain-main/gomod2nix.toml;
  buildFlagsArray = ''
    -ldflags=
    -X github.com/cosmos/cosmos-sdk/version.Name=cronos
    -X github.com/cosmos/cosmos-sdk/version.AppName=${pname}
    -X github.com/cosmos/cosmos-sdk/version.Version=${version}
  '';
}

