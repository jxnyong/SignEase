# SignEase React - AI Sign Interepreter Website

## SignEase React - Installation

You'll need to install Node.js >=v14.16+ (Recommended Version) (NPM comes along with it) and TailAdmin uses **Vite** for frontend tooling, to peform installation and building production version, please follow these steps from below:

- Use terminal and navigate to the react project (SignEase\React-SignEase).

- Then run the following codes below: 
  - <code>npm install</code>

- If there are some missing dependencies, run the following codes below: 
  - <code>npm install react-hook-form</code>
  - <code>npm install react-select</code>
  - <code>npm install axios</code>
  - <code>npm install react-webcam</code>

- Before running, navigate into the server folder (SignEase\server).
- Next, locate the server.py file and run it.
  - (test) C:\GitHub\SignEase> <code>cd server</code>
  - (test) C:\GitHub\SignEase\server> <code> c:/VirtualEnv/test/Scripts/python.exe c:/GitHub/SignEase/server/server.py </code>
- Lastly, navigate back to the react project (SignEase\React-SignEase) and run the following code :
  - <code>npm run dev</code>

Now, in the browser go to <code>localhost:5173</code>

**For Production Build**
Run : <code>npm run build</code>

Default build output directory: /dist

This command will generate a dist as build folder in the root of your template that you can upload to your server.

### Python Dependencies
- In the react project (SignEase\React-SignEase) directory, run the following command:
  - <code>pip install -r requirements.txt</code>


