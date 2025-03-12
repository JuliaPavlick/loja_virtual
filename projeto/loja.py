import tkinter as tk
from tkinter import simpledialog, messagebox

# Função para calcular valor parcelado com aumento
def calcular_valor_parcelado(total, parcelas):
    """Calcula o valor da parcela com aumento de 3% a cada R$50,00 acima de R$100,00"""
    if parcelas > 1:
        valor_parcela = total / parcelas
        aumento = ((valor_parcela - 100) // 50) * 0.03 if valor_parcela > 100 else 0
        valor_parcela += valor_parcela * aumento
        return valor_parcela, aumento
    return total, 0

# Função para solicitar informações de pagamento
def solicitar_pagamento(total):
    """Solicita as informações de pagamento e aplica desconto ou aumento"""
    metodo_pagamento = messagebox.askquestion("Pagamento", "Pagar com Cartão de Crédito/Débito? (Sim) ou PIX (Não)?", icon='question')
    
    if metodo_pagamento == 'yes':  
        forma_pagamento = simpledialog.askstring("Forma de pagamento", "1 - À vista\n2 - Parcelado\n3 - Cancelar")
        
        if forma_pagamento == "1":
            total_com_desconto = total * 0.95
            if messagebox.askyesno("Confirmação", f"Confirmar pagamento de R${total_com_desconto:.2f} à vista?"):
                messagebox.showinfo("Pagamento", f"Pagamento de R${total_com_desconto:.2f} aprovado!")
                return True
            messagebox.showinfo("Pagamento", "Pagamento cancelado.")
            return False

        elif forma_pagamento == "2":
            parcelas = simpledialog.askinteger("Parcelamento", "Número de parcelas (Máx: 12)", minvalue=1, maxvalue=12)
            if parcelas:
                valor_parcela, aumento = calcular_valor_parcelado(total, parcelas)
                total_com_aumento = valor_parcela * parcelas
                msg = f"Parcelado em {parcelas}x de R${valor_parcela:.2f}.\nTotal: R${total_com_aumento:.2f}."
                if aumento > 0:
                    msg += f"\nAumento de {aumento * 100:.1f}% por parcela."
                if messagebox.askyesno("Confirmação", msg + "\nConfirmar pagamento?"):
                    messagebox.showinfo("Pagamento", f"Pagamento de R${total_com_aumento:.2f} aprovado!")
                    return True
            messagebox.showinfo("Pagamento", "Pagamento cancelado.")
            return False

        elif forma_pagamento == "3":
            messagebox.showinfo("Pagamento", "Pagamento cancelado.")
            return False

    else:  
        chave_pix = simpledialog.askstring("PIX", "Informe a chave PIX:")
        if chave_pix:
            if messagebox.askyesno("Confirmação", f"Pagar R${total:.2f} com PIX?"):
                messagebox.showinfo("Pagamento", f"Pagamento de R${total:.2f} via PIX aprovado!")
                return True
        messagebox.showinfo("Pagamento", "Pagamento cancelado.")
        return False

# Função para adicionar item ao carrinho
def adicionar_ao_carrinho_ui(nome, preco):
    """Adiciona item ao carrinho"""
    carrinho.append((nome, preco))
    atualizar_carrinho_ui()

# Função para atualizar exibição do carrinho
def atualizar_carrinho_ui():
    """Atualiza a exibição do carrinho"""
    carrinho_display.delete(0, tk.END)  # Limpa a lista
    
    if not carrinho:
        carrinho_display.insert(tk.END, "Carrinho vazio")
    else:
        for index, (item, preco) in enumerate(carrinho):
            carrinho_display.insert(tk.END, f"{item} - R${preco:.2f}")
    
    # Atualiza o total do carrinho
    total = obter_total()
    carrinho_display.insert(tk.END, f"Total: R${total:.2f}")
    
    # Atualiza botões de remoção
    for widget in carrinho_frame.winfo_children():
        if isinstance(widget, tk.Button):  
            widget.destroy()
    
    for index, (item, preco) in enumerate(carrinho):
        remover_button = tk.Button(carrinho_frame, text="Remover", command=lambda i=index: remover_item_ui(i))
        remover_button.grid(row=index, column=1, padx=5, pady=2)

# Função para remover item do carrinho
def remover_item_ui(index):
    """Remove item do carrinho"""
    if 0 <= index < len(carrinho):
        carrinho.pop(index)
        atualizar_carrinho_ui()

# Função para obter o total do carrinho
def obter_total():
    """Calcula o total do carrinho"""
    return sum(preco for _, preco in carrinho)

# Função para limpar o carrinho após pagamento
def limpar_carrinho():
    """Limpa o carrinho após o pagamento"""
    carrinho.clear()
    atualizar_carrinho_ui()

# Interface gráfica principal
root = tk.Tk()
root.title("Loja Virtual")
root.geometry("500x550")

# Lista de produtos disponíveis
produtos = [("Camiseta", 49.90), ("Calça Jeans", 129.90), ("Jaqueta", 199.90), ("Tênis", 159.90), ("Boné", 39.90)]
carrinho = []

# Exibir produtos
tk.Label(root, text="Produtos", font=("Arial", 14, "bold")).pack()
produtos_frame = tk.Frame(root)
produtos_frame.pack(pady=10)

for nome, preco in produtos:
    tk.Button(produtos_frame, text=f"{nome} - R${preco:.2f}", 
              command=lambda nome=nome, preco=preco: adicionar_ao_carrinho_ui(nome, preco)).pack()

# Exibir carrinho
tk.Label(root, text="Carrinho de Compras", font=("Arial", 14, "bold")).pack(pady=5)
carrinho_frame = tk.Frame(root)
carrinho_frame.pack(pady=5)

carrinho_display = tk.Listbox(carrinho_frame, height=6, width=40)
carrinho_display.pack()

# Botão para finalizar compra
checkout_button = tk.Button(root, text="Finalizar Compra", command=lambda: limpar_carrinho() if solicitar_pagamento(obter_total()) else None, font=("Arial", 12, "bold"))
checkout_button.pack(pady=20)

# Iniciar a interface gráfica
root.mainloop()
