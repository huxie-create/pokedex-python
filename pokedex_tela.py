import tkinter as tk
import requests
from io import BytesIO
from PIL import Image, ImageTk


janela = tk.Tk()
janela.title("Minha Pokédex")
janela.geometry("450x600")


titulo = tk.Label(
    janela,
    text="Digite o nome ou número do Pokémon:"
)
titulo.pack(pady=10)


entrada = tk.Entry(janela, width=30)
entrada.pack()


resultado = tk.Label(
    janela,
    text="",
    justify="left"
)
resultado.pack(pady=10)


imagem_label = tk.Label(janela)
imagem_label.pack(pady=10)


def buscar_pokemon():
    nome = entrada.get().strip().lower()

    if nome == "":
        resultado.config(text="Digite um nome ou número.")
        return

    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"
    resposta = requests.get(url, timeout=10)

    if resposta.status_code != 200:
        resultado.config(text="Pokémon não encontrado.")
        imagem_label.config(image="")
        return

    dados = resposta.json()

    tipos = ", ".join(
        tipo["type"]["name"]
        for tipo in dados["types"]
    )

    resultado.config(
        text=(
            f"#{dados['id']} - {dados['name'].title()}\n"
            f"Altura: {dados['height'] / 10} m\n"
            f"Peso: {dados['weight'] / 10} kg\n"
            f"Tipos: {tipos}"
        )
    )

    url_imagem = dados["sprites"]["other"]["official-artwork"]["front_default"]
    resposta_imagem = requests.get(url_imagem, timeout=10)

    imagem = Image.open(BytesIO(resposta_imagem.content))
    imagem.thumbnail((220, 220))

    imagem_tk = ImageTk.PhotoImage(imagem)
    imagem_label.config(image=imagem_tk)
    imagem_label.image = imagem_tk


botao = tk.Button(
    janela,
    text="Buscar",
    command=buscar_pokemon
)
botao.pack(pady=10)


janela.mainloop()
