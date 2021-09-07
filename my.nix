{ system ? builtins.currentSystem, pkgs ? import ./nix { inherit system; } }:
pkgs.buildGoModule rec {
  pname = "chainmain";
  version = "0.1";
  src =  pkgs.fetchFromGitHub {
    owner = "crypto-org-chain";
    repo = "chain-main";
    rev = "v3.1.1";
    sha256 ="113vhzmpsnghf8ip1jj9m9i9x9lgwbyxhkr73kvqddin52fd8nsz";
  };
  
     runVend = true;
  vendorSha256 = "sha256:0m3w1aq54p46ckxkczh9yjw211lzsj70nygwmx372q2q2xrl2fhg";

  subPackages = [ "cmd/chain-maind" ];
  CGO_ENABLED = "1";
  
  buildFlagsArray = ''
    -ldflags=
    -X github.com/cosmos/cosmos-sdk/version.Name=cronos
    -X github.com/cosmos/cosmos-sdk/version.AppName=${pname}
    -X github.com/cosmos/cosmos-sdk/version.Version=${version}
  '';
}

