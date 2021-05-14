#!/usr/bin/env bash

extensions=(
    acn
    acr
    alg
    aux
    bbl
    blg
    fdb_latexmk
    fls
    glg
    glo
    gls
    ist
    log
    out
    synctex.gz
    tdo
    toc
)

for i in "${extensions[@]}"; do
    rm *.$i 2>/dev/null
done
