# PipelineBI_P1

## Step on the root

```console
foo@bar:~$ python3 -m venv .venv
foo@bar:~$ source .venv/bin/activate
foo@bar:~$ python3 -m pip install -r requirements.txt
```
## To run the server
```console
foo@bar:~$ uvicorn main:app --reload
