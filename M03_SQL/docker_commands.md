## 1- Construindo a imagem Web_Apache
docker build -t web_apache .

## 2 -Listando imagens disponíveis
docker image ls

## 3 -Executar um container 
docker run -d -p 80:80 web_apache

## 4- Exibir containers ativos
docker ps

## 5 -Parar um container
docker stop <container_id>

## 6- Subir um banco de dados com o compose
docker-compose up <service_name> (Sobe todos os serviços se não for espeficado)