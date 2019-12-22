# EcoJourney

## Setup Instructions for AndroidApp_Flutter

> You should have __flutter__ already installed on your system.

Open __Flutter Console__ in the directory __\AndroidApp_Flutter__, then run following commands sequentially.

- flutter pub get
- flutter build apk
- flutter install

## Setup Instructions for Database_BlockChain

> You should have __npm__ already installed on your system.

Open __Command Prompt__ in the directory __\Database_BlockChain__, then run following commands sequentially.

- npm install package.json
- npm audit fix
- npm start

> BlockChainAPI will be hosted on __https://localhost:3002/contact__ with POST request

## Setup Instructions for IntentAPI_ML

> You should have __python (ver >= 3.6)__ already installed on your system.

Open __Command Prompt__ in the directory __\IntentAPI_ML__, then run following commands sequentially.

- pip install rasa
- rasa run --enable-api --cors "*"

> IntentAPI will be hosted on __https://localhost:5005/model/parse__ with POST request