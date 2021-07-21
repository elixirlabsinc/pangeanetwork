# pull official base image
FROM node:12.12-stretch

# Setup a Development User
RUN useradd -ms /bin/bash pangea

# Make the workdir with the right permissions
RUN mkdir /opt/app
RUN chown pangea /opt/app

# set working directory
WORKDIR /opt/app

# Swap to pangea user
USER pangea

# add `/opt/app/node_modules/.bin` to $PATH
ENV PATH /opt/app/node_modules/.bin:$PATH

# install app dependencies
COPY --chown=pangea package.json ./
RUN npm install --silent

# add app
COPY --chown=pangea . ./
EXPOSE 3000

# start app
CMD ["npm", "start"]