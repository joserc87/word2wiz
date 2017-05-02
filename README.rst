# Word2Wiz

Command line tool and web application to convert Word documents to Document
Wizard configurations.

### Requirements

For the command line tool:

- python3
- pip
- spell

To create a server:

- vagrant

To use the converter from the command line you can install the necessary
dependencies with pip:

```
pip install -r requirements.txt
```

To create a server you can run a virtual machine with vagrant (vagrant and
virtualbox are needed):

```
vagrant up
vagrant provision
```

This will download the OS and install dependencies inside that virtual machine.

If you don't want to create a virtual machine, you can also just use the _very
limited_ flask server, runing

```
python3 server.py
```

### How to run it

To run the converter form the 

### How it works

This tool parses an input docx document, looking for text between the marks `«`
and `»`. Then, it generates a Spell file, generating questions based on those
matches. Finally, the spell file is compiled ang an XML is generated with the
Wizard Configuration.

In the case of the web interface, the output will be a zip file containing the
wizard configuration XML, the intermediate Spell and a TXT with the link
between the questions and the metadatas.

### TODO:

- [ ] Remove the zip files after the session is closed.
- [ ] Handle colisions in the uploaded files. Two files can have the same name.
