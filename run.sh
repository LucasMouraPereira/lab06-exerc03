#! /bin/bash

read -p "Você deseja instalar com NPM ou YARN (npm/yarn)? " choice

if [[ -e '.env' ]]; then
    case "$choice" in
        npm ) 
            if [[ -e './node_modules' ]]; then
                npm install
                npm run dev
                echo 'planilha lab03 gerada dentro pasta out'
            else
                npm run dev
                echo 'planilha lab03 gerada dentro pasta out'
            fi; 
            break;;
        yarn ) 
            if [[ -e './node_modules' ]]; then
                yarn
                yarn dev
                echo 'planilha lab03 gerada dentro pasta out'
            else
                yarn dev
                echo 'planilha lab03 gerada dentro pasta out'
            fi; 
            exit;;
        *)  echo "Favor responda npm ou yarn."
            ;;
    esac
else
    touch '.env'
    API_URL='API_URL=https://api.github.com/graphql'
    echo $API_URL>> ".env"

    read -p "Digite seu personal access token gerado no github e validado no git explore: " API_KEY
    echo 'API_KEY'=$API_KEY>> ".env"

    case "$choice" in
        npm ) 
            if [[ -e './node_modules' ]]; then
                npm install
                npm run dev
                echo 'planilha lab03 gerada dentro pasta out'
            else
                npm run dev
                echo 'planilha lab03 gerada dentro pasta out'
            fi; 
            break;;
        yarn ) 
            if [[ -e './node_modules' ]]; then
                yarn
                yarn dev
                echo 'planilha lab03 gerada dentro pasta out'
            else
                echo 'entrou'
                yarn dev
                echo 'planilha lab03 gerada dentro pasta out'
            fi; 
            exit;;
        * ) echo "Favor responda npm ou yarn."
            ;;
    esac
fi; 