import tkinter as tk
from tkinter import simpledialog, messagebox

# Produtos disponíveis
produtos = [
    ("Camiseta", 49.90),
    ("Calça Jeans", 129.90),
    ("Jaqueta", 199.90),
    ("Tênis", 159.90),
    ("Boné", 39.90)
]

# Carrinho de compras (inicialmente vazio)
carrinho = []

def calcular_valor_parcelado(total, parcelas):
    """Calcula o valor por parcela com aumento de 3% a cada R$50,00 acima de R$100,00."""
    if parcelas > 1:
        valor_parcela = total / parcelas
        aumento = 0
        if valor_parcela > 100:
            aumento = ((valor_parcela - 100) // 50) * 0.03
        valor_parcela += valor_parcela * aumento
        return valor_parcela, aumento
    else:
        return total, 0

def solicitar_pagamento(total):
    """Solicita informações de pagamento ao usuário"""
    
    metodo_pagamento = simpledialog.askstring("Escolha o método de pagamento", "Digite 'Cartão' para Cartão de Crédito/Débito ou 'PIX' para pagamento via PIX.")

    if metodo_pagamento == "Cartão":
        forma_pagamento = simpledialog.askstring("Forma de pagamento", "Escolha:\n1 - À vista (5% de desconto)\n2 - Parcelado\n3 - Cancelar pagamento")

        if forma_pagamento == "1":
            total_com_desconto = total * 0.95
            confirmar = messagebox.askyesno("Confirmação", f"Você está prestes a pagar R${total_com_desconto:.2f} à vista. Confirmar pagamento?")
            if confirmar:
                messagebox.showinfo("Pagamento", f"Pagamento de R${total_com_desconto:.2f} aprovado com 5% de desconto!")
                return True
            else:
                messagebox.showinfo("Pagamento", "Pagamento cancelado.")
                return False

        elif forma_pagamento == "2":
            parcelas = simpledialog.askinteger("Parcelamento", "Em quantas parcelas deseja pagar? (Máximo: 12)", minvalue=1, maxvalue=12)
            if parcelas is None:
                return False
            
            valor_parcela, aumento = calcular_valor_parcelado(total, parcelas)
            total_com_aumento = valor_parcela * parcelas
            
            messagebox.showinfo("Parcelamento", f"Parcelamento em {parcelas}x de R${valor_parcela:.2f}.\nTotal final: R${total_com_aumento:.2f}.")
            
            confirmar = messagebox.askyesno("Confirmação", f"Confirmar pagamento parcelado de R${total_com_aumento:.2f}?")
            if confirmar:
                messagebox.showinfo("Pagamento", f"Pagamento parcelado aprovado!")
                return True
            else:
                messagebox.showinfo("Pagamento", "Pagamento cancelado.")
                return False

        elif forma_pagamento == "3":
            messagebox.showinfo("Pagamento", "Pagamento cancelado.")
            return False

        else:
            messagebox.showerror("Erro", "Opção inválida.")
            return False

    elif metodo_pagamento == "PIX":
        chave_pix = simpledialog.askstring("Pagamento por PIX", "Informe a chave PIX:")
        if not chave_pix:
            messagebox.showerror("Erro", "Chave PIX não pode ser vazia!")
            return False

        confirmar = messagebox.askyesno("Confirmação", f"Confirmar pagamento de R${total:.2f} via PIX?")
        if confirmar:
            messagebox.showinfo("Pagamento", f"Pagamento via PIX aprovado!")
            return True
        else:
            messagebox.showinfo("Pagamento", "Pagamento cancelado.")
            return False

    else:
        messagebox.showerror("Erro", "Método de pagamento inválido.")
        return False

# Função para adicionar produto ao carrinho
def adicionar_ao_carrinho(nome, preco):
    carrinho.append((nome, preco))
    atualizar_carrinho()

# Função para atualizar a exibição do carrinho
def atualizar_carrinho():
    carrinho_display.delete(0, tk.END)
    if len(carrinho) == 0:
        carrinho_display.insert(tk.END, "Carrinho vazio")
    else:
        for item, preco in carrinho:
            carrinho_display.insert(tk.END, f"{item} - R${preco:.2f}")

# Função para finalizar a compra
def finalizar_compra():
    total = sum(preco for _, preco in carrinho)
    if total == 0:
        messagebox.showwarning("Carrinho Vazio", "Seu carrinho está vazio. Adicione produtos antes de finalizar a compra.")
        return
    
    confirmar_pagamento = messagebox.askyesno("Confirmar Compra", f"Seu total é R${total:.2f}. Deseja prosseguir com o pagamento?")
    if confirmar_pagamento:
        if solicitar_pagamento(total):
            messagebox.showinfo("Compra Concluída", "Pagamento aprovado. Obrigado pela compra!")
            carrinho.clear()  # Limpa o carrinho após o pagamento
            atualizar_carrinho()

# Interface gráfica principal
root = tk.Tk()
root.title("Loja Virtual")
root.geometry("600x500")

# Exibir produtos disponíveis
tk.Label(root, text="Produtos Disponíveis", font=("Arial", 14, "bold")).pack(pady=10)

produtos_frame = tk.Frame(root)
produtos_frame.pack(pady=10)

for nome, preco in produtos:
    tk.Button(produtos_frame, text=f"{nome} - R${preco:.2f}", command=lambda nome=nome, preco=preco: adicionar_ao_carrinho(nome, preco)).pack()

# Exibir carrinho de compras
tk.Label(root, text="Carrinho de Compras", font=("Arial", 14, "bold")).pack(pady=10)

carrinho_frame = tk.Frame(root)
carrinho_frame.pack(pady=10)

# Lista para mostrar os itens do carrinho
carrinho_display = tk.Listbox(carrinho_frame, height=6, width=40)
carrinho_display.pack()

# Botão para finalizar a compra
checkout_button = tk.Button(root, text="Finalizar Compra", command=finalizar_compra, font=("Arial", 12, "bold"))
checkout_button.pack(pady=20)

root.mainloop()
