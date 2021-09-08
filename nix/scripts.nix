{ pkgs
, config
, cronos ? (import ../. { inherit pkgs; })
, chainmain ? (import ../nix/chainmain.nix { inherit pkgs; })
, hermes ? (import ../nix/hermes.nix { inherit pkgs; })

}:
rec {
  start-chainmain = pkgs.writeShellScriptBin "start-chainmain" ''
    export PATH=${pkgs.pystarport}/bin:${chainmain}/bin:$PATH
    ${../scripts/start-chainmain} ${config.chainmain-config} $@
  '';
  start-cronos = pkgs.writeShellScriptBin "start-cronos" ''
    export PATH=${pkgs.pystarport}/bin:${cronos}/bin:$PATH
    ${../scripts/start-cronos} ${config.cronos-config} $@
  '';
  start-cronos2 = pkgs.writeShellScriptBin "start-cronos" ''
    export PATH=${pkgs.pystarport}/bin:${cronos}/bin:$PATH
    ${../scripts/start-cronos} ${config.cronos2-config} $@
  '';
  start-geth = pkgs.writeShellScriptBin "start-geth" ''
    export PATH=${pkgs.go-ethereum}/bin:$PATH
    ${../scripts/start-geth} ${config.geth-genesis} $@
  '';
  start-hermes = pkgs.writeShellScriptBin "start-hermes" ''
    export PATH=${hermes}/bin:$PATH
    ${../scripts/start-hermes} ${config.hermes-config} $@
  '';
  start-scripts = pkgs.symlinkJoin {
    name = "start-scripts";
    paths = [ start-cronos2 start-cronos start-geth start-chainmain  start-hermes];
  };
}
