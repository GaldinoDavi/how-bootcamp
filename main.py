# %%
# imports
import random
import backoff
from logging import exception
from unittest import expectedFailure
import requests
import json

# %%
url = 'https://economia.awesomeapi.com.br/json/daily/USD-BRL'
ret = requests.get(url)

# %%
if ret:
    print(ret)
else:
    print('Falhouuuu')

# %%
print(ret.text)
dolar = json.loads(ret.text)


# %%
dolar = dolar[0]
# %%
print(f" 20 Dólares equivale a {float(dolar['bid']) * 20}")

# %%


def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/daily/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)
    dolar = dolar[0]
    print(f"{valor} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")


# %%
cotacao(20, 'USD-BRL')
# %%
""" Tratando Erros com Try"""
try:
    cotacao(20, 'USD-BRL')
    # 1/0
except Exception as e:
    print(e)
else:
    print('Ok')

# %%


def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/daily/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)
    print(f"{valor} hoje custam {float(dolar[0]['bid']) * valor}")


# %%
multi_moedas(20, 'USD-BRL')
# %%


def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func


@error_check
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/daily/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)
    print(f"{valor} hoje custam {float(dolar[0]['bid']) * valor}")


multi_moedas(20, 'USD-BRL')
multi_moedas(20, 'EUR-BRL')
multi_moedas(20, 'BTC-BRL')
multi_moedas(20, 'RPM-BRL')
multi_moedas(20, 'JPY-BRL')

# %%


@backoff.on_exception(backoff.expo, (ConnectionAbortedError,
                                     ConnectionRefusedError, ConnectionRefusedError, TimeoutError), max_tries=2)
def test_func(*args, **kargs):
    rnd = random.random()
    print(f"""
            RND:{rnd}
            args:{args if args else 'sem args'}
            kargs:{kargs if kargs else 'sem kargs'}
    """)
    if rnd < .2:
        raise ConnectionAbortedError('Conexão foi finalizada')
    elif rnd < .4:
        raise ConnectionRefusedError('Conexão foi recusada')
    elif rnd < .6:
        raise ConnectionRefusedError('Tempo de espera excedido')
    else:
        return 'OK!'


# %%
test_func(42, 51, nome='Fuck')
# %%
