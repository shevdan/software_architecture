# software_architecture

to install dependency, type:

```pip install -r requirements.txt```

In order for project to work with paths okay it is advised to change cwd to src
to instantiate services you should run 

```cd src```

```python3 start_services.py --facade```
 
```python3 start_services.py --message```

Then instantiate 3 hazelcast nodes by typing in 3 distinct terminal windows:

```hz start```

Next, you can start instances of logging service on different ports of local host, which will be linked to hazelcast cluster

```python3 start_services.py --logging -n 0```

```python3 start_services.py --logging -n 1```

```python3 start_services.py --logging -n 2```

After that you can run client as follows. To create post request:

```python3 src/client.py post -m message```

To create get request:

```python3 src/client.py get```


