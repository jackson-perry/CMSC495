# CMSC495
group project for CMSC 495 Capstone project


Group members:
Carl Blocker
Jackson Perry
Elizabeth Bloss
Jonah Kiplimo
Tyler Wade

I set up a basic project, made an account with a currency API service and built a test flask app tthat can calculte USD conversions to many currencies

to pull and run the coantainer locally:
```bash 
docker pull ghcr.io/jackson-perry/cmsc495:latest
```


to run the container create a .env file with:

APP_ID=your-api-key-here

then use docker compose:

```bash
docker compose up -d
```
or run from the command line as

```bash
docker run -p 8080:8080 \
  -e APP_ID=your-api-key-here \
  ghcr.io/jackson-perry/cmsc495:latest
```