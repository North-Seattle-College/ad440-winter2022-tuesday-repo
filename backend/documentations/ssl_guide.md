# Instructions to use Certbot to enable HTTPS connection

This document is created to provide a guide on how SSL certificates were set up using Certbot

## Steps followed
1. Download and install Certbot in your local system
2. Once Cerbot is installed, run `certbot certonly --manual --preferred-challenges dns -d api.holodium.com` in the terminal.
3. Save the URL and STRING shown in Command prompt
4. Communicate the file to whoever has access create a DNS (Toddy in this case)
5. Create a DNS.
  a. Type = "TXT"
  b. Name will be the URL obtained from Certbot
  c. Value will be the STRING obtained from Certbot
  d. TTL can be left at "Default"

6. Once this is done, come back to terminal and press `enter`
7. Save the certificate and key files locally
8. Upload these certificates on the API gateway.
