Dog Nanny Cam utilizing flask UI. This has a has an authentication process so you can make your streams more private. Works great with cloudflare tunnels. Receives camera streams over the local network and display it to the browser. Allowing you to stream your picamera apis to the internet privately.

Requirements: Docker, Docker-Compose, Postgres.

STEP 1: Change .example_env to .env  and adjust the sample parameters provided. (Providing picamera server code in seperate repo soon)

SECRET <- Secret for registration
SECRET_KEY <- Flask Secret Key
DATABASE <- Database URI
STREAMS  <- Pass in streaming API URLs as a dictionary with integer key values.

Step 2: Run schema.sql on your POSTGRES db.

Step 3: Run docker-compose up
