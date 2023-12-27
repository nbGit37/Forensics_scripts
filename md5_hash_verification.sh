#!/bin/bash


GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
# Vérifie si le nombre d'arguments est correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file.csv>"
    exit 1
fi

file_csv="$1"

# Lire la première ligne pour passer le noms de colonnes
IFS=';' read -r first_column_header other_col < "$file_csv"

# Boucle pour lire chaque ligne du fichier CSV
while IFS=';' read -r file provided_md5 other_hashes; do #other_hashes sert uniquement à ce que seule la colonne 2 soit lue dans hash_md5
    # Vérifie si le fichier existe
    if [ -f "$file" ]; then
        # Calcule le hash MD5 du fichier
        calculated_md5=$(openssl md5 -hex "$file" | awk '{print $2}')

        echo "FILE : $file"
        echo "Calculated Hash: $calculated_md5"
        echo "Provided Hash:   $provided_md5"

        # Compare les hash MD5
        if [ "$calculated_md5" == "$provided_md5" ]; then
            echo -e "${GREEN}$file hash matching with the one provided.${NC}"
        else
            echo -e "${RED}$file hash NOT matching with the one provided.${NC}"
        fi
    else
        if [ "$file" != "$first_column_header" ]; then
            echo "$file doesn't exist."
        fi
    fi
    echo "-----------------------------------------"
done < "$file_csv"

