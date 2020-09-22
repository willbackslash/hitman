FROM node:lts-alpine as builder

WORKDIR /app/frontend
COPY . /app/frontend
RUN npm install
RUN npm run build

FROM node:lts as server
RUN npm install -g serve
WORKDIR /app
COPY --from=builder /app/frontend/build .
EXPOSE 3000
CMD ["serve", "-p", "3000", "-s", "."]
