Dog Nanny Cam utilizing flask UI. This has a has an authentication process so you can make your streams more private. Works great with cloudflare tunnels. Receives camera streams over the local network and display it to the browser. Allowing you to stream your picamera apis to the internet privately.

Requirements: Docker, Docker-Compose, Postgres.

STEP 1: Create a .env file with the following parameters and configure accordingly.

SECRET <- Secret for registration
SECRET_KEY <- Flask Secret Key
DATABASE <- Database URI
STREAM_#  <- Streaming API URL. Need to modify video.py camera_streams dictionary dependent on number of streams.

Step 2: Run schema.sql on your POSTGRES db.

Step 3: Run docker-compose up
