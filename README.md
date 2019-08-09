Pangea Network Admin Dashboard

# To run this app:

1. Clone the repository:

    `git clone https://github.com/elixirlabsinc/pangeanetwork.git`
    
    `cd pangeanetwork`
    
## Backend setup

2. Create and activate a virtual environment:

    `virtualenv env -p python3`
    
    `source env/bin/activate`

3. Install requirements:

    `pip install -r 'requirements.txt'`

4. Run the application:

    `python3 app.py`

    The backend will run at `localhost:5000`. The first time you run this example, a sample sqlite database gets populated automatically. To suppress this behaviour, comment the following lines in app.py:

        if not os.path.exists(database_path):
            build_sample_db()
        
 
 ## Frontend setup
 
 5. In a new tab, navigate to `pangeanetwork/web` directory
 
 6. Run `npm start`
 
 7. View the UI at `localhost:3000`



## Testing with Africa's Talking API

1. Install [ngrok](https://ngrok.com/download)

2. With backend server running, run `./ngrok http 5000` in a new tab

3. From your Africa's Talking account, navigate to SMS > SMS Callback URLs > Incoming Messages and fill in the forwarding url from ngrok in the URL form.

4. From your Africa's Talking account, navigate to Settings > API Key to generate an API Key. Store this in your local environment variables as `AT_API_KEY`.

5. Open the Sandbox by clicking on `Launch Simulator` from your Africa's Talking account and there you can test sending/receiving SMS messages to/from your local running instance of the app.
