Pangea Network Admin Dashboard

To run this app:

1. Clone the repository:

    git clone https://github.com/elixirlabsinc/pangeanetwork.git
    cd pangeanetwork

2. Create and activate a virtual environment:

    virtualenv env -p python3
    source env/bin/activate

3. Install requirements:

    pip install -r 'requirements.txt'

4. Run the application:

    python3 app.py

The first time you run this example, a sample sqlite database gets populated automatically. To suppress this behaviour,
comment the following lines in app.py:

    if not os.path.exists(database_path):
        build_sample_db()
