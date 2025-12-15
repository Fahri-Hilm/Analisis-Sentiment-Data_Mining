FROM node:18-alpine

WORKDIR /app

# Install Python for ML processing
RUN apk add --no-cache python3 py3-pip

# Copy and install Python requirements
COPY requirements-minimal.txt ./
RUN pip3 install -r requirements-minimal.txt

# Copy dashboard source
COPY dashboard-next ./dashboard-next
WORKDIR /app/dashboard-next

# Install Node dependencies and build
COPY dashboard-next/package*.json ./
RUN npm ci --only=production && npm run build

# Back to root and copy data
WORKDIR /app
COPY data ./data
COPY src ./src

# Expose ports
EXPOSE 3000

# Start Next.js application
CMD ["sh", "-c", "cd dashboard-next && npm start"]
