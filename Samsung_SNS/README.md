
# Vulnerabilities in the Samsung SNS Provider application for Android


## 1. Advisory Information

**Title:** Vulnerabilities in the Samsung SNS Provider application for Android

**Advisory ID:** STIC-2014-0511

**Advisory URL:** [http://www.fundacionsadosky.org.ar/publicaciones/#seguridad-en-tic](http://www.fundacionsadosky.org.ar/publicaciones/#seguridad-en-tic)

**Date published:** 2015-3-11

**Date of last update:** 2015-3-11

**Vendors contacted:** Samsung

**Release mode:** Coordinated release



## 2. Vulnerability Information

**Class:**  Incorrect Permission Assignment for Critical Resource [[http://cwe.mitre.org/data/definitions/732.html](http://cwe.mitre.org/data/definitions/732.html)]

**Impact:** Data loss

**Remotely Exploitable:** No

**Locally Exploitable:** Yes

**CVE Identifier:** N/A



## 3. Vulnerability Description

The Samsung Social Networking Service Provider application ("SNS Provider") is used to manage the user's accounts on social network sites such as Facebook, Twitter, Google+, Linkedin and Foursquare; it acts as an internal service so other applications, such as Calendar and Gallery3d, can obtain information about the user's profile and content stored on such sites. The application comes pre-installed in many Samsung devices. For example, the Android Census project [1] identified a subset of devices on which the application is installed . According to statistics about Facebook applications provided by Factets.com[2] the "SNS Provider" app, listed as "Samsung Galaxy" in Facebook, had about 41 million monthly active users, 17 million weekly active users and 5 million daily users as of February 17th, 2015.

When a user logs in to Facebook or Twitter on a Samsung device that has "SNS Provider" installed, the application immediately requests the user to grant it full access to the account. If the user complies, an access token to the user's account on the social network is obtained and stored in a local shared preference file so it can be passed on to other applications that request it. In devices running Android 4.4 and newer, "SNS Provider" also supports management of user accounts on Google+, LinkedIn and Foursquare social networks.
 
"SNS Provider" implements several services used for management and syncing of user's social network accounts (Facebook, Twitter or Fourquare and Google+ in newer devices). These services aren't protected by any permissions. As a result, malicious third party applications installed on the device could use these unprotected services to directly obtain photos, statuses, feeds, location and other type of information from the user's social Facebook or Twitter accounts as well as post new content to it. 

"SNS Provider" also includes services that allow other applications to request the access token to the user's Twitter and Facebook accounts. These services are protected by custom permissions defined by the vendor that don't include proper protection level tags. As a result any application can request permission to access these services and users aren't notified by default when this happens. Furthermore, the custom-defined permissions don't have proper labels or descriptions that let users understand what is being requested. A malicious application that is granted these permissions could then connect to these services and obtain the credentials required to access a users's social network account content permanently. For example, such an application could access the user's private messages on Facebook using the access token provided by the corresponding SNS Provider service.

In devices running Android 4.3 and below "SNS Provider" also includes content providers with custom-defined permissions declared as "normal", so any application running on those devices can request access to these content providers and read any information stored in them.


## 4. Vulnerable packages

* SNS Provider version older than 1.1.1 on Samsung devices running Android 4.1
* SNS Provider version older than 1.1.6 on Samsung devices running Android 4.2
* SNS Provider version older than 1.2.1 on Samsung devices running Android 4.3
* SNS Provider version older than 1.3.5 on Samsung devices running Android 4.4
* SNS Provider version older than 1.3.5 on Samsung devices running Android 5.0

## 5. Vendor Information, Solutions and Workarounds
 
Samsung disabled the App ID assigned to "SNS Provider" on Facebook (listed as "Samsung Galaxy") and Twitter on Feb 17th, 2015 and issued fixed versions of the app with a new App ID. This automatically protects user's from malware that use the access tokens obtained from the prior, vulnerable versions of "SNS Provider", but does not prevent exfiltration of content already stored in the content providers on the device.

As a consequence of disabling "SNS Provider" on Facebook and Twitter, users still using the vulnerable versions will see notifications on their devices with messages stating "Try Single Sign On again" or "Facebook/Twitter Session Expired". 

Users are advised to update to the latest version of "SNS Provider" from the Galaxy Apps market using the guidelines published by the vendor at [3] and to clear the all the stored application data. 


## 6. Credits

This vulnerability was discovered and researched by Joaquín Manuel Rinaudo. The publication of this advisory was coordinated by Programa de Seguridad en TIC. 

## 7. Technical Description

All the vulnerable versions of the "SNS Provider" application implement two services that are exported so other applications can obtain information or interact with Facebook and Twitter social networks, named _SNSFbService_ and _SNSTwService_ respectively. These services allows an application to access the user's information (such as statuses, photos, events, likes, etc in Facebook or get the access token in the Twitter related service) and even post content on behalf of the user. Since they aren't protected by any permission, any malicious application can connect to them.
 
A third exported service  _SNSFbServiceForAuthToken_ allows an application to obtain the Facebook account credentials (access token) but its protected by a custom permission: _com.sec.android.SNS3.permission.SNS_FB_ACCESS_TOKEN_. In devices running versions of Android greater than 4.1, the same happens for Twitter and it's protected service _SNSTwServiceForAuthToken_ and the corresponding permission _com.sec.android.SNS3.permission.SNS_TW_ACCESS_TOKEN_.

The protection level [4] of these custom permissions is set to "normal" so any third party application can request them. When a third party, potentially malicious, application requires the  user to grant these permissions, they will not be shown in the short list of permission presneted to the user at installation time. They will only appear if the user
clicks on the UI button to show the lsit of all requested permissions. Furthermore, when the entire list of permissions requested is shown, these custom defined permissions will appear to be named "Default" with a description consisting of the default string "string resource". Therefore, it is likely that unsuspecting users will simply grant these permissions to any third party application that requests them.

In order to connect to these services, an attacker would need to know their interface. The AIDL files can be reconstructed by reverse engineering the application and observing the generated proxies and stubs. The interfaces for the Twitter related service are in _com.sec.android.SNS3.svc.sp.twitter.api_ and the Facebook ones are in _com.sec.android.SNS3.svc.sp.facebook.api_ and _com.sec.android.SNS3.svc.sp.facebook.auth.api_. 
 
The source code and corresponding binary APK file of a proof of concept application that demonstrates explotiaiton of these vulnerbailities found in [5]. The application requests SNS Provider's custom-defined permissions to communicate with SNS Provider's Facebook and Twitter protected services and successfully connects to its exported Facebook services (the protected and the unprotected one) and the protected Twitter service. The UI has three buttons. When clicking the first one, the application obtains the user's access token to Twitter (if SNS Provider has been granted one) using a method exported via AIDL from the service _SNSTwitterServiceForAuthToken_. This works on devices running versions of "SNS Provider" greater than 1.1.1. When clicking the second button, the application does the same for Facebook using _SNSFbServiceForAuthToken_. Lastly, the third button calls one of the methods from the unprotected _SNSFbService_ (no permission is required to connect to it) to posts a new feed with the text "Hackers o dominados" in the user's Facebook timeline.
 
This third button should no longer work since Feb 17. 2015 when Facebook disable the SamsSNS app. 

In devices running Android 4.4 or greater, LinkedIn, GooglePlus and Foursquare can also be connected to "SNS Provider". The last two also have unprotected exported services named _SNSGpService_ and _SNSFsService_ respectively. Their interfaces can be found in _com.sec.android.SNS3.svc.sp.googleplus.api_ and _com.sec.android.SNS3.svc.sp.foursquare.api_.
However the Google+ API only allows access to public content [6] and the Foursquare components that alSNS to manage a user's Foursquare account are disabled, so these components pose no effective risk to users.
SNS Provider doesn't request access automatically when it detects a user has logged in to any of those social networks. Nevertheless, an attacker could launch SNS Provider's exported activities that ask the user to give the app access to the user's account by sending intents with the actions _com.sec.android.SNS3.RETRY_SSO_GOOGLEPLUS_ for Google+ and _com.sec.android.SNS3.RETRY_SSO_FOURSQUARE_ for Foursquare. If granted, the attacker could then abuse the exported services to obtain the user profile, feeds and places nearby.

In many older devices (running Android 4.3 or prior), the information saved in the app's ContentProviders could be exfiltrated by a malicious app that requested the permission _com.sec.android.SNS3.permission.RSNS_DB_[7] and queried stored photos and feeds from Facebook social network. Attackers could also update the information contained by the provider by sending a broadcast signal to either _SNSFbWidgetUpdatePhotoStreamReceiver_ or _SNSFbTickerUpdateFeedsReceiver_.


## 8. Report Timeline

* **2014-11-20:** Programa de Seguridad en TIC notified Samsung's mobile security team of discovered vulnerabilities in an application pre-installed on several mobile devices and requested PGP key to coordinate the report and disclosure process further.
        
* **2014-11-21:** 
         The Samsung mobile security team sent their PGP public key to continue communications over encrypted email.
        
* **2014-11-25:** Programa de Seguridad en TIC sent an preliminary report about the security issues in SamsSNS and notified that the initial publication date was set to December 2, 2014.
        
* **2014-11-26:** 
          Samsung mobile security team requested to hold off the disclosure and asked to provide a POC of the exploit.
        
* **2014-11-26:** Programa de Seguridad en TIC informed the vendor that the publication date was established in case the report wasn't acknowledged or that the vendor indicated it had no plan to fix the issues. Since the vendor acknowledged the report and did not seem reluctant to address the problems, publication of the security advisory was postponed to December 16, 2014. Also,  Programa de Seguridad en TIC attached a proof-of-concept APK that demonstrated how an attacker could abuse the services exportedSNS application.
        
* **2014-11-29:** 
          Samsung Mobile security team confirmed the security issues and agreed to contact the coordinator later next week to work together in determining the disclosure date.
        
* **2014-12-02:** Programa de Seguridad en TIC asked for vulnerable device models and software versions to be able to provide the user population with precise information and agreed to push back publication of the advisory to December 16th, 2014. 
        
* **2014-12-12:** 
         Samsung mobile security team noted that an update would require coordination between Samsung SNS vendors and service carriers to resolve the issues properly and requested permission to disclose the identity of the reporting organization to SNS vendors (Facebook, Twitter). The vendor indicated that it was already testing the application update fixing all the reported problems. Because of the associated complexity, the vendor asked to hold off disclosure the issue until the update was released, estimated to take 6 months since it would require coordination of the release schedule with the service carriers. It also informed that determining the lists of vulnerable device models and software versions would take a while given the wide range of devices manufactured by the vendor.
        
* **2014-15-15:** 
          Samsung mobile security team requested to confirm the previous mail regarding the disclosure date.
        
* **2014-12-15:** Programa de Seguridad en TIC acknowledged having received the mail and agreed to postpone the publication but informed the vendor that the additional 6 months requested were considered an excessive timespan. A new deadline would be discussed internally along with alternative solutions.
        
* **2015-1-2:** 
          Samsung mobile security team informed that it now estimated that the patch would take much longer than 6 months because of complexities in Android software ecosystem, inability to auto-update the application and problems updating the software to some models due to carrier policies.
        
* **2015-1-9:** Programa de Seguridad en TIC agreed with the complications to provide a patch to a pre-installed application for which there is no auto-update capability. Alternative solutions where proposed such as: 1) informing the users so they disable the SNS Provider app from their Facebook accounts or 2) That Samsung invalidates the SNS Provider's App ID on Facebook or 3) That Samsung used one of its installed auto-updateable applications to the deliver the update to SNS Provider requesting the appropriate permission to install it or 4) That Samsung used its existing app protection/sandboxing technology to prevent malicious third party apps from accessing the exposed services.  Programa de Seguridad en TIC informed that it would postpone publication of the advisory to the first week of February 2015 pending further analysis of possible mitigations.
        
* **2015-1-26:** 
         Samsung mobile security team informed that is was talking to Facebook and Twitter to address the issue and asked to disclose to them the name of the organizaiton that reported the bugs. It indicated thatit may take another month or so to prepare the invalidation of the App ID due to the necessary internal QA process.
        
* **2015-1-27:** Programa de Seguridad en TIC agreed to inform Facebook and Twitter of it's identity and contact info and also requested precise estimate for a new deadline in order to postpone the publication.
        
* **2015-2-4:** 
          Samsung mobile security team informed they decided to disable the old App ID from the social network server side (Facebook and Twitter) since this action would protect user instantly and notified that the results of this action were being tested. The vendor said that it expected to take action on February 13th, 2015 but that it required two additional weeks to get clearance for the disclosure from their own and SNS vendor's PR departments. 
        
* **2015-2-11:** Programa de Seguridad en TIC asked for a status and if the app was being invalidated on February 13.
        
* **2015-2-11:** 
          Samsung mobile security team informed they where waiting for the QA team to finish testing.
        
* **2015-2-13:** 
          Samsung mobile security team expected to finish testing by February 17, 2015 and to invalidate the apps from the server side once the testing was done successfully. 
        
* **2015-2-14:** Programa de Seguridad en TIC rescheduled the publication to February 18th, 2015 and requested an official statement to include in the report. 
        
* **2015-2-16:** 
          Samsung mobile security team requested to push back publication of the advisory to March 10, 2015 due to new year celebrations between 18~22 of February and the need to monitor user experience for a week after invalidating the app ID and to allow the Public Relations department to review the statement to be included in the advisory.
        
* **2015-2-26:** 
          Samsung mobile security team informed that an update was release on February 17th, 2015 and that they had disabled the old Twitter App ID. On February 20 it restricted API's for Facebook for syncing. They also requested a draft of the security advisory.
        
* **2015-3-3:** Programa de Seguridad en TIC sent the report and also confirmed the mitigations for the now deprecated Facebook and Twitter app IDs but indicated that since content already downloaded would be accessible through content provider, users should be advised to update the application or disable it AND delete all the stored data, and asked Samsung if fixes for Google+ and Foursquare services were implemented SNS on newer devices. 
        
* **2015-3-3:** 
          Samsung mobile security team assured that Foursquare components were disabled in all versions and that now both Google+ and Foursquare components were being protected by a "signatureOrSystem" permission. Also that since Google+ API placed restrictions to only allow public content, a number of the APIs (e.g feeds) were blocked so no private information could be leaked from the exported service. It also indicated that although the LinkedIn activity could be launched by a third party app, SNS Provider does not have the capability to add an account and it does not store any data. 
        
* **2015-3-10:** Programa de Seguridad en TIC sent the final version of the security advisory to the vendor.
        
* **2015-3-11:** 
          The vendor sent an email asking us to use a common convention to refer to the application as "SNS Provider". Also indicated that the advisory was missleading since it confused the "Samsung Galaxy App", which is a marketplace app similar to Google Play, with the SNS Provider application and included incorrect statistics. Requested to correct the error.
        
* **2015-3-11:** Programa de Seguridad en TIC replied that following the common convention, SNS provider  will be used throughout the bulletin. Regarding, the second comment, indicated that Facebook lists the SNS Provider app as "Samsung Galaxy" and that's the FAcebook App name the users are requested to give permissions to. As far as the reporters knew, the Samsung Galaxy Apps marketplace application is not a Facebook application and therefore its no listed in the Facebook Apps statistics page published by Factets.com. Requested the vendor to confirm or refute the above explanation as soon as possible. 
        

## 9. References

[1] [http://census.tsyrklevich.net/content_providers/com.sec.android.SNS3.sp.facebook](http://census.tsyrklevich.net/content_providers/com.sec.android.SNS3.sp.facebook)

[2] [http://www.factets.com/application/samsung-galaxy-dfNWi8eIS](http://www.factets.com/application/samsung-galaxy-dfNWi8eIS)

[3] [http://www.samsung.com/levant/support/skp/faq/1072595](http://www.samsung.com/levant/support/skp/faq/1072595)

[4] [http://developer.android.com/guide/topics/manifest/permission-element.html](http://developer.android.com/guide/topics/manifest/permission-element.html)

[5] [https://github.com/programa-stic/SNS-thief/](https://github.com/programa-stic/SNS-thief/)

[6] [https://developers.google.com/+/api/](https://developers.google.com/+/api/)

[7] [http://census.tsyrklevich.net/permissions/com.sec.android.SNS3.permission.RSNS_DB](http://census.tsyrklevich.net/permissions/com.sec.android.SNS3.permission.RSNS_DB)

## 10. About Fundación Dr. Manuel Sadosky

The Dr. Manuel Sadosky Foundation is a mixed (public / private) institution whose goal is to promote stronger and closer interaction between industry and the scientific-technological system in all aspects related to Information and Communications Technology (ICT). The Foundation was formally created by a Presidential Decree in 2009. Its Chairman is the Minister of Science, Technology, and Productive Innovation of Argentina; and the Vice-chairmen are the chairmen of the country’s most important ICT chambers: The Software and Computer Services Chamber (CESSI) and the Argentine Computing and Telecommunications Chamber (CICOMRA). For more information visit: [http://www.fundacionsadosky.org.ar](http://www.fundacionsadosky.org.ar)

## 11. Copyright Notice

The contents of this advisory are copyright (c) 2014 Fundación Sadosky and are licensed under a Creative Commons Attribution Non-Commercial Share-Alike 4.0 License: [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)
