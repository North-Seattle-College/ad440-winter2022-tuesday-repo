# Instructions to use Certbot to enable HTTPS connection

This document is created to provide a guide on how SSL certificates were set up using Certbot

## Steps followed
1. Download and install Certbot in your local system
(https://certbot.eff.org/)).
3. Once Cerbot is installed, run `certbot certonly --manual --preferred-challenges dns -d api.holodium.com` in the terminal.
4. Save the URL and STRING shown in terminal.
5. Do NOT press `ENTER` yet. Communicate the file to whoever has access create a DNS      (Toddy in this case)
   IF 'ENTER' is pressed before DNS Manager approves you will have to start over from    step 3.
	Example: DNS TXT name: _acme-challenge.api.holodium.com.
        Content of file: 2eM7VwLx7K8HcVV1FFGqb6bjWSu_1KaZX-Fu54XbiN0
6. Create a DNS.
  a. Type = "TXT"
  b. Name will be the URL obtained from Certbot
  c. Value will be the STRING obtained from Certbot
  d. TTL can be left at "Default"

7. Once this is done, come back to terminal and press `enter`
8. Save the certificate and key files locally.
9. A confirmation should display with the file location of the `Certificate` and `Key` .pem files.
10. Open this file directory from step 9 and save the files to a secure location of your choosing.
11. Go to API AWS gateway and upload the files from step 10 by _"Importing Certificate"_

PS:-Steps 5 and 6 will require assistance from the DNS manager.
