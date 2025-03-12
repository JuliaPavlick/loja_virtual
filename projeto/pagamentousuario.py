import tkinter as tk
from tkinter import simpledialog, messagebox

# Função para calcular valor parcelado
def calcular_valor_parcelado(total, parcelas):
    if parcelas > 1:
        valor_parcela = total / parcelas
        aumento = 0
        if valor_parcela > 100:
            aumento = ((valor_parcela - 100) // 50) * 0.03
        valor_parcela += valor_parcela * aumento
        return valor_parcela, aumento
    else:
        return total, 0

# Função para escolher o tipo de cartão
def escolher_cartao():
    forma_pagamento = simpledialog.askstring("Escolha o Cartão", "Escolha o tipo de pagamento:\n1 - Débito\n2 - Crédito")
    if forma_pagamento == "1":
        return "Débito"
    elif forma_pagamento == "2":
        return "Crédito"
    else:
        messagebox.showerror("Erro", "Opção inválida. Tente novamente.")
        return None

# Função para gerenciar os produtos (somente após login)
def gerenciar_produtos():
    # Solicitar o login e a senha do usuário
    usuario = simpledialog.askstring("Login", "Digite seu nome de usuário:")
    senha = simpledialog.askstring("Senha", "Digite a senha:", show="*")

    # Verificar se o usuário e senha são válidos
    usuarios_permitidos = ["admin"]
    if usuario in usuarios_permitidos and senha == "2405":
        escolha = simpledialog.askstring("Gerenciar Produtos", "Escolha:\n1 - Adicionar\n2 - Editar\n3 - Remover")
        if escolha == "1":
            adicionar_produto()
        elif escolha == "2":
            editar_produto()
        elif escolha == "3":
            remover_produto()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos! Acesso negado.")

# Função para adicionar produto
def adicionar_produto():
    nome = simpledialog.askstring("Adicionar Produto", "Nome do produto:")
    if nome:
        preco = simpledialog.askfloat("Adicionar Produto", "Preço do produto:")
        if preco and preco > 0:
            produtos.append((nome, preco))
            atualizar_produtos_ui()
        else:
            messagebox.showerror("Erro", "Preço inválido!")

# Função para editar produto
def editar_produto():
    nomes = [nome for nome, _ in produtos]
    escolha = simpledialog.askstring("Editar Produto", "Escolha o produto para editar:\n" + "\n".join(nomes))
    for i, (nome, preco) in enumerate(produtos):
        if nome == escolha:
            novo_preco = simpledialog.askfloat("Editar Produto", f"Novo preço para {nome}:")
            if novo_preco and novo_preco > 0:
                produtos[i] = (nome, novo_preco)
                atualizar_produtos_ui()
            else:
                messagebox.showerror("Erro", "Preço inválido!")
            return
    messagebox.showerror("Erro", "Produto não encontrado!")

# Função para remover produto do estoque
def remover_produto():
    nomes = [nome for nome, _ in produtos]
    escolha = simpledialog.askstring("Remover Produto", "Escolha o produto para remover:\n" + "\n".join(nomes))
    for i, (nome, preco) in enumerate(produtos):
        if nome == escolha:
            # Pedir confirmação antes de remover
            confirmar_remocao = messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover {nome} do estoque?")
            if confirmar_remocao:
                del produtos[i]
                atualizar_produtos_ui()
                return
    messagebox.showerror("Erro", "Produto não encontrado!")

# Função para atualizar a UI do carrinho
def atualizar_carrinho_ui():
    carrinho_display.delete(0, tk.END)
    if not carrinho:
        carrinho_display.insert(tk.END, "Carrinho vazio")
        # Esconde o botão de remover item do carrinho se o carrinho estiver vazio
        remover_button.pack_forget()
    else:
        for item, preco in carrinho:
            carrinho_display.insert(tk.END, f"{item} - R${preco:.2f}")
        # Exibe o botão de remover item do carrinho se o carrinho não estiver vazio
        remover_button.pack(pady=10)

# Função para remover item do carrinho
def remover_item_carrinho():
    try:
        item_selecionado = carrinho_display.curselection()[0]
        item_remover = carrinho[item_selecionado]
        carrinho.remove(item_remover)
        atualizar_carrinho_ui()
    except IndexError:
        messagebox.showwarning("Aviso", "Nenhum item selecionado para remoção.")

# Função para atualizar a UI dos produtos
def atualizar_produtos_ui():
    for widget in produtos_frame.winfo_children():
        widget.destroy()
    for nome, preco in produtos:
        button = tk.Button(produtos_frame, text=f"{nome} - R${preco:.2f}", 
                           command=lambda nome=nome, preco=preco: carrinho.append((nome, preco)) or atualizar_carrinho_ui(), 
                           bg="#9B59B6", fg="white", activebackground="#8E44AD")
        button.pack(pady=2)

# Função para gerar a nota fiscal
def gerar_nota_fiscal(nome_cliente, produtos, metodo_pagamento, parcelas, total, total_com_desconto, total_com_aumento):
    nota = f"Nota Fiscal\n\nCliente: {nome_cliente}\n\nProdutos comprados:\n"
    
    for produto, preco in produtos:
        nota += f"{produto} - R${preco:.2f}\n"
    
    nota += f"\nTotal: R${total:.2f}\n"
    
    if metodo_pagamento == "Cartão":
        if parcelas > 1:
            nota += f"Parcelamento: {parcelas}x\nValor total com parcelamento: R${total_com_aumento:.2f}\n"
        else:
            nota += f"Pagamento à vista (com 5% de desconto): R${total_com_desconto:.2f}\n"
    else:
        nota += f"Pagamento via PIX: R${total:.2f}\n"
    
    # Criar nova janela para exibir a nota fiscal
    nota_window = tk.Toplevel(root)
    nota_window.title("Nota Fiscal")
    nota_window.geometry("400x400")
    
    nota_label = tk.Label(nota_window, text=nota, justify="left", padx=10, pady=10, bg="#f4e1f7", font=("Arial", 12))
    nota_label.pack()

# Função para realizar o pagamento
def solicitar_pagamento():
    if not carrinho:
        messagebox.showerror("Erro", "O carrinho está vazio!")
        return

    # Primeiro, o painel de administração é preenchido antes de confirmar o pagamento
    nome_cliente = simpledialog.askstring("Painel de Administração", "Nome completo:")
    endereco = simpledialog.askstring("Painel de Administração", "Endereço:")
    numero_celular = simpledialog.askstring("Painel de Administração", "Número de celular:")

    if not (nome_cliente and endereco and numero_celular):
        messagebox.showerror("Erro", "Informações de pagamento incompletas!")
        return

    # Após o preenchimento do painel de administração, a confirmação do pagamento será realizada
    total = sum([preco for _, preco in carrinho])

    # Escolha do método de pagamento
    metodo_pagamento = simpledialog.askstring("Escolha o método de pagamento", 
                                              "Digite 'Cartão' para Cartão de Crédito/Débito ou 'PIX' para pagamento via PIX.")
    if metodo_pagamento == "Cartão":
        tipo_cartao = escolher_cartao()
        if tipo_cartao is None:
            return
        forma_pagamento = simpledialog.askstring("Forma de pagamento", "Escolha:\n1 - À vista (5% de desconto)\n2 - Parcelado\n3 - Cancelar")
        if forma_pagamento == "1":
            total_com_desconto = total * 0.95
            confirmar = messagebox.askyesno("Confirmação", f"Confirmar pagamento de R${total_com_desconto:.2f} à vista?")
            if confirmar:
                messagebox.showinfo("Pagamento", f"Pagamento de R${total_com_desconto:.2f} aprovado via {tipo_cartao}!", icon="info")
                messagebox.showinfo("Agradecimento", "Obrigado pela sua compra! Esperamos vê-lo novamente!", icon="info")
                gerar_nota_fiscal(nome_cliente, carrinho, "Cartão", 1, total, total_com_desconto, 0)
                carrinho.clear()
                atualizar_carrinho_ui()
        elif forma_pagamento == "2":
            parcelas = simpledialog.askinteger("Parcelamento", "Em quantas parcelas? (Máximo 12)", minvalue=1, maxvalue=12)
            if parcelas:
                valor_parcela, aumento = calcular_valor_parcelado(total, parcelas)
                total_com_aumento = valor_parcela * parcelas
                confirmar = messagebox.askyesno("Confirmação", f"Confirmar pagamento parcelado em {parcelas}x de R${valor_parcela:.2f}?")
                if confirmar:
                    messagebox.showinfo("Pagamento", f"Pagamento de R${total_com_aumento:.2f} aprovado via {tipo_cartao}!", icon="info")
                    messagebox.showinfo("Agradecimento", "Obrigado pela sua compra! Esperamos vê-lo novamente!", icon="info")
                    gerar_nota_fiscal(nome_cliente, carrinho, "Cartão", parcelas, total, 0, total_com_aumento)
                    carrinho.clear()
                    atualizar_carrinho_ui()
        else:
            messagebox.showinfo("Pagamento", "Pagamento cancelado.", icon="info")
    elif metodo_pagamento == "PIX":
        chave_pix = simpledialog.askstring("PIX", "Informe a chave PIX:")
        if chave_pix:
            confirmar = messagebox.askyesno("Confirmação", f"Confirmar pagamento de R${total:.2f} via PIX?")
            if confirmar:
                messagebox.showinfo("Pagamento", f"Pagamento de R${total:.2f} aprovado via PIX!", icon="info")
                messagebox.showinfo("Agradecimento", "Obrigado pela sua compra! Esperamos vê-lo novamente!", icon="info")
                gerar_nota_fiscal(nome_cliente, carrinho, "PIX", 0, total, 0, 0)
                carrinho.clear()
                atualizar_carrinho_ui()
    else:
        messagebox.showerror("Erro", "Método de pagamento inválido.")

# Função para gerenciar os produtos
def iniciar_compras():
    if not hasattr(iniciar_compras, "clicado") or not iniciar_compras.clicado:
        # Mostrar os produtos e opções para adicionar ao carrinho
        produtos_frame.pack()
        atualizar_produtos_ui()

        # Botão para finalizar compra
        tk.Button(root, text="Finalizar Compra", command=solicitar_pagamento, bg="#9B59B6", fg="white", activebackground="#8E44AD").pack()

        # Botão para gerenciar produtos
        tk.Button(root, text="Gerenciar Produtos", command=gerenciar_produtos, bg="#9B59B6", fg="white", activebackground="#8E44AD").pack()

        # Botão para remover item do carrinho será exibido se houver itens no carrinho
        global remover_button
        remover_button = tk.Button(root, text="Remover Item do Carrinho", command=remover_item_carrinho, bg="#9B59B6", fg="white", activebackground="#8E44AD")
        remover_button.pack_forget()  # Inicialmente oculto

        # Marcar que o botão foi clicado
        iniciar_compras.clicado = True
    else:
        messagebox.showinfo("Aviso", "O processo de compras já foi iniciado.")

# Função para gerenciar os produtos
root = tk.Tk()
root.title("Loja Virtual de Roupas")
root.geometry("600x600")
root.configure(bg="#f4e1f7")  # Cor de fundo roxa clara

produtos = [("Camiseta", 49.90), ("Calça Jeans", 129.90), ("Jaqueta", 199.90)]
carrinho = []

produtos_frame = tk.Frame(root, bg="#f4e1f7")  # Fundo roxo claro no frame dos produtos

# Botão para iniciar o processo de compras
tk.Button(root, text="Iniciar Compras", command=iniciar_compras, bg="#9B59B6", fg="white", activebackground="#8E44AD").pack()

carrinho_display = tk.Listbox(root, height=6, width=40, bg="#f9e5f5", fg="black")
carrinho_display.pack()

root.mainloop()
