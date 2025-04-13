Dog Nanny Cam utilizing flask UI. This has a has an authentication process so you can make your streams more private. Works great with cloudflare tunnels. Receives camera streams over the local network and display it to the browser. Allowing you to stream your picameras to the internet privately.

Step 1: Clone to server

Step 2: create a virtual environment in peepin_pup directory using python3 -m venv .venv

Step 3: Activate virtual environment

Step 4: pip install flask and waitress
 
Step 5: Edit auth.py and __init__.py secrets.

Step 6: Run - flask --app peepin_pup init-db to initalize database instance

Step 7: Run - waitress-serve --call "peepin_pup:create_app"

Step 8: This will serve the application on port 8080
