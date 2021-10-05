{pkgs ? import ./default.nix {} }:
pkgs.stdenv.mkDerivation {
    name="hermes";
    version="v0.7.3";
    src= pkgs.fetchurl {
      url="https://github.com/informalsystems/ibc-rs/releases/download/v0.7.3/hermes-v0.7.3-x86_64-unknown-linux-gnu.tar.gz";
      sha256 = "sha256:17k9017y41zbjqywrgni0i7s1qn6v0pjc5af7xqaqa9qcsi3l9jr";
  };
    sourceRoot = ".";  
  installPhase = ''
    echo "hermes"
    echo $out
    install -m755 -D hermes $out/bin/hermes
  '';

   meta = with pkgs.lib; {    
    platforms = platforms.linux;
  };
  
 }