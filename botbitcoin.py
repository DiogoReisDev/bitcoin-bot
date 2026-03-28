import ssl
import json

import websocket
import bitstamp.client

import credenciais

def client():
    return bitstamp.client.Trading(username=credenciais.USERNAME,
                                   key=credenciais.KEY,
                                   secret=credenciais.SECRET)

def comprar(quantidade):
    trading_client = client()
    trading_client.buy_market_order(quantidade)
def vender(quantidade):
    trading_client = client()
    trading_client.sell_market_order(quantidade)

def ao_abrir(ws):
    print("Abriu a conexão")

    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
"""
    ws.send(json_subscribe)


def ao_fechar(ws):
    print("Fechando conexão")

def erro(ws, erro):
    print("Deu erro")
    print(erro)




def mensagem_recebida(ws, mensagem):
    resposta_servidor = json.loads(mensagem)
    data = resposta_servidor.get('data',{})

    price = data.get('price')
    amount = data.get('amount_str')

    print(f"Alguém comprou {amount} BTC por U${price}")

    if price > 9000:
        vender()
    elif price < 8000:
        comprar()
    else:
        print("Aguarde a lógica de compra e venda")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                 on_open=ao_abrir,
                 on_close=ao_fechar,
                 on_message=mensagem_recebida,
                 on_error=erro)

    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

