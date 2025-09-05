# Use an official Node.js runtime as a parent image
FROM node:24-slim

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy the rest of the application code
COPY . .

# Define environment variable
ENV NODE_ENV=production

# Run the application
CMD ["node", "main.js"]