# 1단계: Vue 빌드
FROM node:20-slim AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# 2단계: Nginx 배포
FROM nginx:stable-alpine AS production-stage

# Vue 빌드 결과 복사
COPY --from=build-stage /app/dist /usr/share/nginx/html

# nginx 설정 복사
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

