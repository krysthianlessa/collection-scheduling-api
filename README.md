# Collection Scheduling

# Development
We need create a copy of `.env.example` on root and a copy of `.env.example` in `scripts` folder.

To start the application with all services in development mode, just run `make run-dev`

# Production
In production, we need make deploy in cloud (database and backend) and in On-Primise (pooling and wahtsapp-api)

The .env.example on root directory has all environments variables to use in cloud. We need only get the correct values. And inside of scripts folder we have another .env.example to add the environments variables of On-Primise (just create a copy named `.env`)

So, just run `make deploy-local` in your host machine.