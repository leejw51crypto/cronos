{pkgs ? import ./default.nix {} }:
pkgs.stdenv.mkDerivation {
    name="hermes";
    version="v0.7.1";
    src= pkgs.fetchurl {
      url="https://github.com/leejw51crypto/ibc-rs/releases/download/v0.7.1/hermes.tar.gz";
      sha256 = "sha256:0whb2ynrjil7hymbyd3wqr7jv6ifhavbfnm45z9v64k0i4m5ks3l";  
  };
    sourceRoot = ".";  
  installPhase = ''
    echo "hermes OK##########################"
    echo $out
    install -m755 -D hermes $out/bin/hermes
  '';

   meta = with pkgs.lib; {    
    platforms = platforms.linux;
  };
  
 }