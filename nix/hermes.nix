{pkgs ? import ./default.nix {} }:
pkgs.stdenv.mkDerivation {
    name="hermes";
    version="v0.7.1";
    src= pkgs.fetchurl {
      url="https://github.com/leejw51crypto/ibc-rs/releases/download/v0.7.1/hermes.tar.gz";
      sha256 = "sha256:03g7vvdid8saa8ywmkdcfgvzdkx5zhivbnfav30dl43dm5x9a561";  
  };

    sourceRoot = ".";
  
  installPhase = ''
    echo "OK##########################"
    echo $out
    install -m755 -D hermes $out/bin/hermes
  '';

   meta = with pkgs.lib; {    
    platforms = platforms.linux;
  };
  
 }