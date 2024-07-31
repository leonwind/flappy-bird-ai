{ pkgs ? import <nixpkgs> {} }:
let 
    python = pkgs.python3;
    python-packages = python.withPackages (p: with p; [
        pygame
        numpy
    ]);
in pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
        python-packages
    ];
}

