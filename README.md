## Inspiration
We were inspired by hobby lifters who wanted to track the analytics of their weightlifting workouts and were seeking a fitness community.

## What it does
The product records and analyzes key data for users during lifting sessions, such as reps. The device is connected to a web-based app to deliver visualization of the analytic data and encourages users to create or participate in challenges with peers, fostering a vibrant workout community. The LIFT app enhances users’ fitness journeys by enabling them to engage in various challenges, compete on the leaderboard, and complete daily tasks.

## How we built it
We used an MPU 6050 sensor to measure the acceleration during a dumbbell curl then ran the data through a processor serial port to convert the values into angles (on the x, y, and z planes). When the dumbbell was curled past a certain angle, our code would recognize it and increase a counter by one. \
\
We use Next.js to build the front-end web view and Flask as the main backend server to perform requests to the database. Node.js with Express is used to communicate with the MKR1010 hardware. The database is coded using PostgreSQL, and it holds all the user and game (challenges) data. User authentication is served by Firebase.
