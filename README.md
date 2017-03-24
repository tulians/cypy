# cypy
`cypy` is a tool developed in pure Python 3 that allows you to store credentials in a server using the *Vigenere* cypher scheme. These credentials can be added, retrieved or deleted, using a simple web interface

### Usage
Clone `cypy` using
```sh
$ git clone https://github.com/tulians/cypy
$ cd cypy
$ python3 cypy/server.py [-port]
```
#### Add credential
In a browser search for
```
<your_server's_ip>:<selected_port>/add
```
which will present a form in screen, asking for a *username*, *password* and a *keyword*. The first two are the credentials itself, while the latter is the private key used for encryption.

#### Retrieve credential
Given the credential username, you can retrieve the associated password by searching in a browser for
```
<your_server's_ip>:<selected_port>/add
```
which will present a form in screen. This form must be filled with the username of the credential and the keyword used when creating the credential.

#### Delete credential
Similar to the previous case, a credential can be deleted by searching in a browser for
```
<your_server's_ip>:<selected_port>/del
```
and filling the form with the credential's username and associated keyword.

### Todos
- Improve the web interface graphics.
- Create a site for the "/" which uses Ajax to render the form given the options.
- Add a credential description.

### Contact
This project is under development, so if you found any aspect that can be optimized or found a bug that must be fixed, please open an issue. Alternatively, you can contact me by e-mail on jtulians@gmail.com.

### License
MIT
