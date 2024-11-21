import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class BitcoinGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Bitcoin Game')
        self.root.geometry("500x600")  # Set the window size
        self.bitcoins = [
            {"name": "Bitcoin", "price": 7500, "amount": 0},
            {"name": "Ethereum", "price": 7000, "amount": 0},
            {"name": "Litecoin", "price": 7000, "amount": 0},
            {"name": "Bitcoin Cash", "price": 7500, "amount": 0},
            {"name": "Cardano", "price": 7500, "amount": 0},
            {"name": "Stellar", "price": 7000, "amount": 0},
            {"name": "EOS", "price": 7500, "amount": 0},
            {"name": "Monero", "price": 5000, "amount": 0},
            {"name": "Dogecoin", "price": 7500, "amount": 0},
            {"name": "Shiba Inu", "price": 7500, "amount": 0},
        ]
        self.balance = 100000
        self.transactions = []
        self.bitcoinLabels = []
        self.balanceLabel = tk.Label(self.root, text=f"Balance: {self.balance:,}", font=("Arial", 12, "bold"))  # Increased font size
        self.balanceLabel.pack()
        
        # Create a frame to hold the bitcoin table
        self.bitcoinFrame = tk.Frame(self.root)
        self.bitcoinFrame.pack()
        
        # Create a table header
        tk.Label(self.bitcoinFrame, text="", font=("Arial", 12, "bold")).grid(row=0, column=0)
        tk.Label(self.bitcoinFrame, text="이름", font=("Arial", 12, "bold")).grid(row=0, column=1)
        tk.Label(self.bitcoinFrame, text="갯수", font=("Arial", 12, "bold")).grid(row=0, column=2)
        tk.Label(self.bitcoinFrame, text="값어치", font=("Arial", 12, "bold")).grid(row=0, column=3)
        tk.Label(self.bitcoinFrame, text="현재 가격", font=("Arial", 12, "bold")).grid(row=0, column=4)
        
        # Create a table row for each bitcoin
        for i, bitcoin in enumerate(self.bitcoins):
            label = tk.Label(self.bitcoinFrame, text=f"{i+1}", font=("Arial", 12, "bold"))
            label.grid(row=i+1, column=0)
            label = tk.Label(self.bitcoinFrame, text=bitcoin['name'], font=("Arial", 12, "bold"))
            label.grid(row=i+1, column=1)
            label = tk.Label(self.bitcoinFrame, text=f"{bitcoin['amount']:,}", font=("Arial", 12, "bold"))
            label.grid(row=i+1, column=2)
            label = tk.Label(self.bitcoinFrame, text=f"{bitcoin['amount'] * bitcoin['price']:,}", font=("Arial", 12, "bold"))
            label.grid(row=i+1, column=3)
            label = tk.Label(self.bitcoinFrame, text=f"{bitcoin['price']:,}", font=("Arial", 12, "bold"))
            label.grid(row=i+1, column=4)
            self.bitcoinLabels.append(label)
        
        self.bitcoinIndexEntry = tk.Entry(self.root, font=("Arial", 12, "bold"))  # Increased font size
        self.bitcoinIndexEntry.pack()
        self.amountEntry = tk.Entry(self.root, font=("Arial", 12, "bold"))  # Increased font size
        self.amountEntry.pack()
        self.buyButton = tk.Button(self.root, text="Buy", command=self.buyBitcoin, font=("Arial", 12, "bold"))  # Increased font size
        self.buyButton.pack()
        self.sellButton = tk.Button(self.root, text="Sell", command=self.sellBitcoin, font=("Arial", 12, "bold"))  # Increased font size
        self.sellButton.pack()
        self.root.after(1000, self.updateBitcoinPrices)
        self.root.mainloop()

    def buyBitcoin(self):
        bitcoin_index = int(self.bitcoinIndexEntry.get()) - 1
        amount = int(self.amountEntry.get())
        if bitcoin_index >= 0 and bitcoin_index < len(self.bitcoins):
            bitcoin = self.bitcoins[bitcoin_index]
            price = bitcoin["price"]
            total_cost = price * amount
            if total_cost <= self.balance:
                self.balance -= total_cost
                self.transactions.append({"type": "buy", "bitcoin": bitcoin["name"], "amount": amount, "price": price})
                bitcoin["amount"] += amount
                print(f"Bought {amount} {bitcoin['name']} for {total_cost:,}")
                # Update the amount label in the table
                self.bitcoinLabels[bitcoin_index].config(text=f"{bitcoin['amount']:,}", font=("Arial", 12, "bold"))

    def sellBitcoin(self):
        bitcoin_index = int(self.bitcoinIndexEntry.get()) - 1
        amount = int(self.amountEntry.get())
        if bitcoin_index >= 0 and bitcoin_index < len(self.bitcoins):
            bitcoin = self.bitcoins[bitcoin_index]
            price = bitcoin["price"]
            total_revenue = price * amount
            if amount <= bitcoin["amount"]:
                self.balance += total_revenue
                self.transactions.append({"type": "sell", "bitcoin": bitcoin["name"], "amount": amount, "price": price})
                bitcoin["amount"] -= amount
                print(f"Sold {amount} {bitcoin['name']} for {total_revenue:,}")
                # Update the amount label in the table
                self.bitcoinLabels[bitcoin_index].config(text=f"{bitcoin['amount']:,}", font=("Arial", 12, "bold"))

    def updateBitcoinPrices(self):
        for i, bitcoin in enumerate(self.bitcoins):
            # Update the price with a random change
            change = random.uniform(-0.30, 0.37)
            bitcoin["price"] *= (1 + change)
            # Ensure the price does not go below 50
            if bitcoin["price"] < 50:
                bitcoin["price"] = 50
            
            # Update the price label with percentage change
            change_percentage = round(change * 100, 2)
            if change > 0:
                change_text = f"+{change_percentage}%"
                self.bitcoinLabels[i].config(
                    text=f"{bitcoin['price']:,.0f} ({change_text})", 
                    font=("Arial", 12, "bold"), 
                    fg="red"
                )
            else:
                change_text = f"-{change_percentage}%"
                self.bitcoinLabels[i].config(
                    text=f"{bitcoin['price']:,.0f} ({change_text})", 
                    font=("Arial", 12, "bold"), 
                    fg="blue"
                )

            # Update the value column (amount * price)
            value_label = self.bitcoinFrame.grid_slaves(row=i + 1, column=3)[0]  # Find the "value" label
            value_label.config(
                text=f"{bitcoin['amount'] * bitcoin['price']:,.0f}", 
                font=("Arial", 12, "bold")
            )
        
        # Update the balance
        self.balanceLabel.config(
            text=f"Balance: {self.balance:,.0f}", 
            font=("Arial", 12, "bold")
        )
        
        # Calculate the total value
        total_value = self.balance + sum(bitcoin['amount'] * bitcoin['price'] for bitcoin in self.bitcoins)
        
        # Check for win/lose conditions
        if total_value == 0:
            print("Game Over! Your balance and total bitcoin value have reached 0.")
            self.restart_game()
        elif self.balance >= 300000:
            print("Congratulations! You have reached a balance of 300,000 or more. You win!")
            self.restart_game()
        
        # Schedule the next price update
        self.root.after(1000, self.updateBitcoinPrices)


    def restart_game(self):
        self.root.destroy()
        game = BitcoinGame()

if __name__ == '__main__':
    game = BitcoinGame()
