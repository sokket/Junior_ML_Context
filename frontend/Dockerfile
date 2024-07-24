FROM node:22

WORKDIR /app

COPY ./package-lock.json /app/
COPY ./package.json /app/

RUN npm install

EXPOSE 5173

CMD [ "npm", "run", "dev" ]