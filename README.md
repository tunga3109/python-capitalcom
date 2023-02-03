Welcome to unofficial Python wrapper for the Capital.com exchange REST API v1. Use at your own risk.

The Capital.com API allows direct access to the latest version of our trading engine.

--- General information

Base URL: https://api-capital.backend-capital.com/ Base demo URL: https://demo-api-capital.backend-capital.com/ In order to use the endpoints a session should be launched. This can be done using the POST /session endpoint. Session is active for 10 minutes. In case your inactivity is longer than this period then an error will occur upon next request. The API covers the full range of available instruments, licences and trading functionality. Getting started

--- To use the API the following simple steps should be taken:

Create a trading account Note that a demo account can be used. Turn on Two-Factor Authentication (2FA) 2FA should be turned on prior to API key generation. Instruction for 2FA enabling. Generate an API key To generate the API key, go to Settings > API integrations > Generate new key. There you will need to enter the label of the key, set an optional expiration date, enter the 2FA code and that’s it. You are all set! Authentication

--- How to start new session?

There are 2 ways to start the session:

Using your API key, login and password details.
Using your API key, login and encrypted password details.
-- Using your API key, login and password details

Here you should simply use the POST /session endpoint and mention the received in the platform’s Settings API key in the X-CAP-API-KEY header, login and password info in the identifier and password parameters. The value of the encryptionKey parameter should be false.

-- Using your API key, login and encrypted password details

First of all you should use the GET /session/encryptionKey and mention the generated in the platform’s Settings API key in the X-CAP-API-KEY header. As a response you will receive the encryptionKey and timeStamp parameters; Using the received encryptionKey and timeStamp parameters you should encrypt your password using the AES encryption method.

Go to the POST /session endpoint, set true value for the encryptionKey parameter and mention the received in the platform’s Settings API key in the X-CAP-API-KEY header, login and prior encrypted password info in the identifier and password parameters

--- After starting the session

On starting the session you will receive the CST and X-SECURITY-TOKEN parameters in the response headers. CST is an authorization token, X-SECURITY-TOKEN shows which financial account is used for the trades. These headers should be passed on subsequent requests to the API. Both tokens are valid for 10 minutes after the last use.