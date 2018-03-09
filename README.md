Author: Qianyi Feng

qfeng@uoregon.edu

Note:

Add the function on the previous project.

Sumbit the brevet data on 0.0.0.0:5002 first, then goto 0.0.0.0:5000/api to register the username 

and password.

Get the token on 0.0.0.0:5000/api/token?username=test2&password=123456, then the website would jump to the token.

Copy the token without the quotation mark, put on 0.0.0.0:5000/listAll?token=[the copied token] (or replace listAll to any other requests), and then the results would display.
