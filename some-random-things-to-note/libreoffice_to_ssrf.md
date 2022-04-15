If the server uses LibreOffice (version 5.1.15) to convert documents into PDF format, It might lead to some issue. bcs:
- LibreOffice process listening on TCP:8100 runs as root user, although www-data can access all neccesary files
- LibreOffice ODT XML can include file from disk into the document

Ex:

 if we create a ``text:section`` tag that reference to ``/flag`` in the ``content.xml`` after unzip ``.odt`` file with sth like this:  
 ```
 <text:section text:name="string"><text:section-source xlink:href="file:///flag" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/></text:section>
 ```
 (remember to zip the files again into ``.odt`` and then upload)

This will force LibreOffice to include the file specified in XML into the document when ``ODT`` to ``PDF`` conversion takes placce in server.
