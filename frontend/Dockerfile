# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
COPY package.json /app/
COPY next.config.js /app/
COPY tailwind.config.js /app/
COPY postcss.config.js /app/
COPY src /app/src
COPY public /app/public
COPY styles /app/styles
RUN npm install --legacy-peer-deps
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "start"]
