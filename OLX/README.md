
# Multiple vulnerabilities in OLX Android application


## 1. Advisory Information

**Title:** Multiple vulnerabilities in OLX Android application

**Advisory ID:** STIC-2014-0401

**Advisory URL:** [http://www.fundacionsadosky.org.ar/publicaciones-2](http://www.fundacionsadosky.org.ar/publicaciones-2)

**Date published:** 2015-11-30

**Date of last update:** 2014-7-14

**Vendors contacted:** OLX

**Release mode:** Unilateral release



## 2. Vulnerability Information

**Class:** Information Exposure Through Sent Data [[http://cwe.mitre.org/data/definitions/201.html](http://cwe.mitre.org/data/definitions/201.html)], Authentication Bypass by Spoofing [[http://cwe.mitre.org/data/definitions/290.html](http://cwe.mitre.org/data/definitions/290.html)], Insufficiently Protected Credentials [[http://cwe.mitre.org/data/definitions/522.html](http://cwe.mitre.org/data/definitions/522.html)]

**Impact:** Data loss, Security bypass

**Remotely Exploitable:** Yes

**Locally Exploitable:** No

**CVE Identifier:** N/A



## 3. Vulnerability Description

OLX operates local online classifieds marketplaces accessible through the internet and through native apps on smartphones. As of November 2015, their Android application had between 50 to 100 million installation worldwide [1].
 
OLX Android application has had two major different versions, each one has their own API used to communicate with the OLX servers. Both of these application versions and their corresponding APIs are currently working and have multiple vulnerabilities that would allow an attacker compromise remotely and locally users accounts.   


## 3.1. Login bypass: Access accounts of users who log in using Facebook
 
Users can login to the application using their Facebook account. When this happens, the Facebook access token and the Facebook user ID are sent to the server to authenticate the user. The server fails to verify if the access token is valid. As a result, an attacker can access any OLX account from users who have logged in using Facebook by just providing their Facebook user ID and a fake access token.


## 3.2. Login bypass: Access accounts of any user
 
The older OLX application's API also suffers fro another server validation problem. When sending a register using Facebook request containing a email address from a already registered victim account, but a valid access token from an unrelated Facebook account (for example one from an account controlled by the attacker), the server responds with the unsalted MD5 hash from the password of the victim's account. This hash could be used by an attacker to impersonate the victim using any of OLX's Android APIs or be employed to perform offline cracking attacks (e.g use sites like Crackstation [2]) to try finding the user's actual password. 


## 3.3. Insecure login procedure in OLX newer API
 
The newer OLX application's API uses a challenge and a response authentication to obtain a session key employed later to authenticate user requests. There are several problems with this authentication process. 

The first is that the challenge is predictable. The second one is that the challenge is sent as a response to the server along with a hash of the user email and password but the hash does not depend on the challenge at all, making it obsolete. Finally, the session key a user obtains is also predictable since it's a base64 from the user ID concatenated with a timestamp.

An attacker can capture the hash of the user email and password to later reuse to login as the user or directly obtain a challenge for the victim account from just their email or username and use this challenge to forge the victim's session key. 


## 3.4. Insufficient Transport Layer Protection
 
Android devices running OLX communicate to the OLX server using HTTP. Therefore, attackers in the same network can capture sensitive information when the user is using the application. For examples, they could obtain the user site credentials when new users register to the site, when they changes their password, also steal the Facebook access token used to log in, session keys (in OLX newer application) and more.    


## 4. Vulnerable packages

* OLX Android version 4.35.2 and below.

## 5. Vendor Information, Solutions and Workarounds

Vendor fixed Login bypass for all accounts was fixed when the old API Login with Facebook feature was disabled. Last version (4.35.2) as of 30 of November of 2015 remains vulnerable to login bypass because of deterministic sessions and insecure login procedure. Also, application is still vulnerable to Login bypass for users that used Login with Facebook and continues to use HTTP to communicate with OLX server allowing an attacker to capture sensitive information and hijack sessions.


## 6. Credits

This vulnerability was discovered and researched by Joaquín Manuel Rinaudo. The publication of this advisory was coordinated by Programa Seguridad en TIC. 

## 7. Technical Description


## 7.1. Login bypass: Access accounts of users who used Login with Facebook
 
When a user signs in using Facebook, OLX application uses the Oauth protocol via Facebook's SDK for Android to ask the user to grant OLX access to their Facebook account. If the user authorizes the access, the application is provided with an access token that can be used to retrieve personal information or perform actions on behalf of the user.  
 
The older API also uses Oauth to communicate with the OLX server. It uses Oauth-signpost as a library to do so. If the user logs in with a username and password, OLX uses the user name as the consumer key and a MD5 hash of the user password as the consumer secret to sign the requests.

The consumer secret is obtained from the server when user's login via Facebook. When a user clicks the "Login with Facebook" a POST request is made to _api.olx.com/iphone/user/facebook/[USER-ID]/connect_ with the Facebook access token specified as a field parameter to obtain this secret. If the user account already exists, the server doesn't validate if the access token is valid, therefore an attacker can obtain the user's consumer secret by only specifying the correct Facebook user ID of the user and providing a fake or empty access token. The server will then respond with a json object with the user's ID, email address and consumer secret for the account related to the Facebook user ID specified. The consumer secret is actually encrypted with a hardcoded key ("0395a67c9aa847a756daa8535917e805") and zeroed IV, these values can be found in the class _com.olx.olx.util.OlxCryptoUtil_.

In the newer API, the application needs to obtain the session key to authenticate user requests. To do so, it sends a GET request to _api-v2.olx.com/users/facebook/[USER-ID]_ providing the Facebook access token as an URL parameter. Again, an attacker can send an invalid access token and still obtain the user's session key. This session key can then be employed to perform any of the requests exposed by the new API. The API request list can be found in the _com.olx.smaug.api.AuthenticatedContract_ interface class. Application versions running the newer API are using the library retrofit [3] to turn that Java Interface into the API used to communicate with the server.


## 7.2. Login bypass: Access accounts of any user
 
When a user registers using Facebook for the first time in the older OLX's API, a POST request is sent to _api.olx.com/iphone/user/facebook/[USER-ID]/signup_ specifying the access token obtained from Facebook, the email address related to that Facebook account along with the user's full name and a country ID. The server responds this request the same way as when a user logs in with a created account, with a key to be used as the consumer secret among other values. 

If an attacker changes the email address to one of a existing user account (maintaining the same Facebook account access token), the server responds with the generated key that when decrypted (with the key specified at [Sec. 7.1]) corresponds to an unsalted MD5 hash of that user's password. This allows a way for attackers to remotely obtain any OLX user's hashed password. This hashed password can be used as a consumer secret for the older OLX API or even be used to generate a valid hash for the challenge and response mechanism of the newer API. An attacker can also try to crack the hash offline to obtain the password in plaintext. 

The following proof-of-concept python script shows it is possible to obtain the MD5 hash of the password from any account just by providing the user's email address. A valid access token for the application with its corresponding Facebook user ID are needed also as argument. These values can be obtained by logging in to OLX using Facebook with an account and sniffing the application traffic to capture the access token when it's being sent to the server:


```
import sys
import urllib
import urllib2
import json
import traceback
import base64
from Crypto.Cipher import AES

def obtain_md5(email,access_token,fb_id):
  url = 'http://api.olx.com/iphone/user/facebook/%s/signup' %fb_id 
  data = '''accessToken=%s&email=%s&fullName=Victim&countryId=2''' %(access_token,email)
  req = urllib2.Request(url, data,headers={"User-Agent" : "OLX android 3.3.8 build 338"})
  response = urllib2.urlopen(req)
  jsonobject = json.loads(response.read())
  return jsonobject['response']['password']

def decrypt_hash(hashed_password):
  key = "0395a67c9aa847a756daa8535917e805"
  iv = "0000000000000000"
  decryptor = AES.new(key, AES.MODE_CBC, iv)
  return decryptor.decrypt(base64.b64decode(hashed_password))[:32]

if __name__ == '__main__':
  if len(sys.argv) < 1: 
    print "No email specified"
    exit(0) 
  encrypted =obtain_md5(sys.argv[1],sys.argv[2],sys.argv[3])
  try:
    hashed_password  = decrypt_hash(encrypted)  
    print "User md5 password is %s" %hashed_password
  except:
    traceback.print_exc()
    print "Failed accessing user's account"
    pass

      
```


## 7.3. Insecure login procedure in OLX newer API
 
In newer versions of the application, authentication consist in first requesting a challenge to _api-v2.olx.com/users/challenge_ with the username as a parameter. Once the challenge is obtained, then the application performs a SHA512 hash over the concatenation of the MD5 hash of the password with the username (i.e SHA512(MD5(password)+username or email) ). Then both the challenge and the SHA512 hash are sent to the server as URL parameters (_c_ and _h_ respectively) to _api-v2.olx.com/users/login_ so the application can then obtain a session key. 

There are several problems with this authentication procedure. The server challenge is predictable since it's a base64 encode of the username (encoded using Ceasar Cipher), the user ID and a timestamp. It can then be spoofed by an attacker. 

Also, the challenge is not being used by the SHA512 hash to modify the application response so if an attacker can capture the hash, he can then reuse it to log in by requesting the challenge and then providing the captured hash and requested challenge. An interesting note is that the challenge is probably predictable and includes the user ID because the server needs a way to know who's the hash from so it (without saving any state) so it can then recalculate the hash with the username and password to match it to the user's provided one. 

Finally, the session key obtained from the server by the authentication mechanism is actually a base64 encoding of the user ID with a timestamp. This predictable session key allows an attacker to skip the login procedure by generating a valid session key by simply requesting a challenge to the server for the victim account, then decoding it as a base64, deleting the user name and the first delimiter ('|') and then encoding it again.


## 7.4. Insufficient Transport Layer Protection
 
Last but not least, all the communication in both API versions between the application and the server is performed over HTTP. Then an attacker in the same network or in the route to the server could capture much sensitive information. For example, in both OLX's applications, the following requests containing user sensitive information could be captured:

* Obtain username and password by capturing the request when a new user is registering. The older API uses a PUT method request to _api.olx.com/iphone/user_ while in the newer the request is a POST to _api-v2.olx.com/users_. 

* Acquire username, session key and Facebook access token from the Login with Facebook request by capturing traffic intended to the URLs commented in [Sec. 7.1].
 
And in the second API version the user session key could be captured from any of the request from _AuthenticatedContract_ interface.


## 8. Report Timeline

* **2015-06-14:** Programa Seguridad en TIC Requested for a security contact.
        
* **2015-06-14:** 
         OLX provided with contact information.
        
* **2014-07-11:** 
          Technical details of the vulnerabilities sent to the vendor.
        
* **2014-07-14:** 
           The vendor acknowledged the vulnerability and assured that the problem was being addressed.

* **2015-11-30:** 
         Version 4.35.2 was released but vulnerabilities mentioned in sections 7.1, 7.3 and 7.4 weren't resolved. 
* **2015-11-30:** 
         Advisory was released. 

## 9. References

[1] [https://play.google.com/store/apps/details?id=com.olx.olx](https://play.google.com/store/apps/details?id=com.olx.olx)

[2] [https://crackstation.net/](https://crackstation.net/)

[3] [http://square.github.io/retrofit/](http://square.github.io/retrofit/)

## 10. About Fundación Dr. Manuel Sadosky

The Dr. Manuel Sadosky Foundation is a mixed (public / private) institution whose goal is to promote stronger and closer interaction between industry and the scientific-technological system in all aspects related to Information and Communications Technology (ICT). The Foundation was formally created by a Presidential Decree in 2009. Its Chairman is the Minister of Science, Technology, and Productive Innovation of Argentina; and the Vice-chairmen are the chairmen of the country’s most important ICT chambers: The Software and Computer Services Chamber (CESSI) and the Argentine Computing and Telecommunications Chamber (CICOMRA). For more information visit: [http://www.fundacionsadosky.org.ar](http://www.fundacionsadosky.org.ar)

## 11. Copyright Notice

The contents of this advisory are copyright (c) 2014 Fundación Sadosky and are licensed under a Creative Commons Attribution Non-Commercial Share-Alike 4.0 License: [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)
