FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci --silent

COPY . /app

RUN npm run build


FROM nginx:1.25-alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN chmod -R a+rX /usr/share/nginx/html && chown -R nginx:nginx /usr/share/nginx/html

EXPOSE 80