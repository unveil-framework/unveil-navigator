FROM node:18.20.8-bullseye AS build

ENV NODE_OPTIONS=--openssl-legacy-provider

WORKDIR /src/nav-app
COPY ./nav-app/package*.json ./
RUN npm ci

COPY ./nav-app/ ./

WORKDIR /src
COPY layers/*.md ./layers/
COPY *.md ./

WORKDIR /src/nav-app
RUN npm run build -- --configuration production

FROM nginx:1.27-alpine

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/nav-app/dist/ /usr/share/nginx/html/

EXPOSE 4200

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://127.0.0.1:4200/ >/dev/null || exit 1
