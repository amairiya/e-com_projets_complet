FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html


# FROM nginx:1.26-alpine

# # Créer l’utilisateur nginx (si pas déjà présent)
# RUN addgroup -S nginx1 && adduser -S -G nginx nginx

# # Donner les droits nécessaires
# RUN chown -R nginx:nginx \
#     /usr/share/nginx/html \
#     /var/cache/nginx \
#     /var/run \
#     /var/log/nginx

# # Config nginx
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# # Contenu statique
# COPY . /usr/share/nginx/html

# USER nginx

# EXPOSE 80
