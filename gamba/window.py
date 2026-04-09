import tkinter as tk
import random
from tkinter import scrolledtext
from tkinter import ttk
import casino
import time

class GameGUI:
    def __init__(self, root):
        # --- State Variables ---
        self.root = root
        self.is_rolling = False
        self.chest_labels = {}
        self.balance_var = tk.StringVar(value="0.00 $")
        self.result_var = tk.StringVar(value="Welcome! Open a chest to start.")

        self.shop_buttons = {}

        # --- Root Configuration ---
        self.root.title("Casino")
        self.root.geometry("1400x877")
        self.root.configure(bg="#121212")

        # --- Style ---
        self._setup_styles()

        # --- Main Layout Structure ---
        self._build_main_containers()
        
        # --- Content Screens (The Switching System) ---
        self._build_content_frames()

        # --- Initialize Components ---
        self._setup_header()
        self._setup_left_menu()
        self._setup_right_menu()
        self._setup_console()
        
        # Start on Inventory/Loot screen
        self.show_frame(self.inventory_frame)

    # ==========================================
    # LAYOUT & UI CONSTRUCTION
    # ==========================================

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", padding=6, relief="flat", background="#333333", foreground="white")
        self.style.map("TButton", background=[('active', '#454545')])

    def _build_main_containers(self):
        # Header
        self.header_frame = tk.Frame(self.root, pady=20, bg="#f0f0f0")
        self.header_frame.pack(side="top", fill="x")

        # Footer Console
        self.console_frame = tk.Frame(self.root, height=150, bg="black")
        self.console_frame.pack(side="bottom", fill="x")
        self.console_frame.pack_propagate(False)

        # Body
        self.body_frame = tk.Frame(self.root, bg="#121212")
        self.body_frame.pack(side="top", fill="both", expand=True)

        # Sidebars
        self.left_menu = tk.Frame(self.body_frame, width=150, padx=10, relief="groove", borderwidth=1, bg="#121212")
        self.left_menu.pack(side="left", fill="y")
        
        self.right_menu = tk.Frame(self.body_frame, width=250, padx=10, relief="groove", borderwidth=1, bg="#121212")
        self.right_menu.pack(side="right", fill="y")

        # Center Content Container (Where screens are swapped)
        self.center_container = tk.Frame(self.body_frame, bg="#121212")
        self.center_container.pack(side="left", fill="both", expand=True)

    def _build_content_frames(self):
        """Creates the different screens for navigation."""
        self.inventory_frame = tk.Frame(self.center_container, bg="#121212")
        self.shop_frame = tk.Frame(self.center_container, bg="#121212")

        for f in (self.inventory_frame, self.shop_frame):
            f.grid(row=0, column=0, sticky="nsew")
            self.center_container.grid_rowconfigure(0, weight=1)
            self.center_container.grid_columnconfigure(0, weight=1)

        self._setup_inventory_screen()
        self._setup_shop_screen()

    def _setup_header(self):
        self.balance_label = tk.Label(self.header_frame, textvariable=self.balance_var, 
                                     font=("Arial", 28, "bold"), bg="#f0f0f0")
        self.balance_label.pack()

    def _setup_console(self):
        self.console = scrolledtext.ScrolledText(self.console_frame, bg="black", fg="#FFFFFF",
                                                font=("Consolas", 10), state="disabled")
        self.console.pack(fill="both", expand=True)

    def _setup_left_menu(self):
        tk.Label(self.left_menu, text="MENU", font=("Arial", 12, "bold"), bg="#121212", fg="white").pack(pady=10)
        self.add_menu_button(self.left_menu, "Shop", self.onNavigateShop)
        self.add_menu_button(self.left_menu, "Inventory", self.onNavigateInventory)
        self.add_menu_button(self.left_menu, "Bank", self.onNavigateInventory)

    def _setup_right_menu(self):
        tk.Label(self.right_menu, text="CHESTS", font=("Arial", 12, "bold"), bg="#121212", fg="white").pack(pady=10)
        self.chest_labels["basic"] = self.add_chest_row("Basic Chest", "basic", casino.player.basicChests)
        self.chest_labels["ultra"] = self.add_chest_row("Ultra Chest", "ultra", casino.player.ultraChests)
        self.chest_labels["premium"] = self.add_chest_row("Premium Chest", "premium", casino.player.premiumChests)

    def _setup_inventory_screen(self):
        """Builds the main loot/chest rolling area."""
        tk.Label(self.inventory_frame, text="Loot Result", font=("Arial", 10, "italic"), bg="#121212", fg="gray").pack(pady=5)
        self.result_label = tk.Label(self.inventory_frame, textvariable=self.result_var, font=("Arial", 16), 
                                     wraplength=300, fg="blue", bg="#121212")
        self.result_label.pack(expand=True)

        self.spinner_canvas = tk.Canvas(self.inventory_frame, width=600, height=150, bg="#121212", highlightthickness=0)
        self.spinner_canvas.pack(expand=True)


    def _setup_shop_screen(self):
        # --- Scrollable Setup (Same as before) ---
        container = tk.Frame(self.shop_frame, bg="#121212")
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg="#121212", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#121212")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1300) 
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Header
       

        # --- PART 1: 2-Column Grid for Items ---
        items_grid = tk.Frame(scrollable_frame, bg="#121212")
        items_grid.pack(fill="x", padx=(20,200))
        # Configure 2 equal columns
        items_grid.columnconfigure(0, weight=1)
        items_grid.columnconfigure(1, weight=1)

        items_data = [
            ("vip", casino.shop.vip), ("energy", casino.shop.energy),
            ("cigs", casino.shop.cigs), ("vodka", casino.shop.vodka),
            ("drugs", casino.shop.drugs), ("prostitute", casino.shop.prostitute),
            ("russian", casino.shop.russian)
        ]

        for i, (key, obj) in enumerate(items_data):
            row = i // 2
            col = i % 2
            # Use the helper to get the frame and the button
            item_frame, item_btn = self.add_shop_item(items_grid, obj)
            item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.shop_buttons[key] = item_btn

        # --- PART 2: Quick Buy Chests (Full Width) ---
        buy_frame = tk.Frame(scrollable_frame, bg="#121212", pady=40)
        buy_frame.pack(fill="x")

        tk.Label(buy_frame, text="QUICK BUY BASIC CHESTS", font=("Arial", 14, "bold"), 
                bg="#121212", fg="white").pack(pady=10)

        buttons_container = tk.Frame(buy_frame, bg="#121212")
        buttons_container.pack()

        self.quick_buy_labels = {}
        quick_buys = [("1", 1), ("25", 25), ("10k", 10000)]

        for text, amount in quick_buys:
            f = tk.Frame(buttons_container, bg="#121212")
            f.pack(side="left", padx=30)
            btn = tk.Button(f, text=text, command=lambda a=amount: self.onQuickBuy(a),
                            width=10, height=5, bg="#222", fg="white", font=("Arial", 16, "bold"))
            btn.pack()
            lbl = tk.Label(f, text="0.00 $", bg="#121212", fg="#00ff99", font=("Consolas", 11))
            lbl.pack(pady=5)
            self.quick_buy_labels[amount] = lbl
        
    # ==========================================
    # NAVIGATION
    # ==========================================

    def show_frame(self, frame):
        frame.tkraise()

    def onNavigateShop(self):
        # 1. Hide the right sidebar
        self.right_menu.pack_forget()
        
        # 2. Hide the entire bottom console layout
        self.console_frame.pack_forget()
        
        # 3. Show the shop
        self.show_frame(self.shop_frame)
        self.print_w("Console hidden for Shop view.")

    def onNavigateInventory(self):
        # 1. Re-show the console at the bottom
        self.console_frame.pack(side="bottom", fill="x")
        
        # 2. Re-show the sidebar on the right
        # Use 'before' to ensure it doesn't shift the center container
        self.right_menu.pack(side="right", fill="y", before=self.center_container)
        
        # 3. Show the inventory
        self.show_frame(self.inventory_frame)

    def onNavigateBank(self):
        # Using shop frame as placeholder per original code
        self.show_frame(self.shop_frame)

    # ==========================================
    # HELPERS & UI BUILDERS
    # ==========================================

    def handle_purchase(self, buy_func):
        
        success = buy_func.buy()
        
        if success:
            self.print_w("Purchase successful!")
            # 2. Execute the update/refresh logic
            self.onUpdate() 
        else:
            self.print_w("Transaction failed: Not enough money.")

    def print_w(self, text):
        self.console.config(state="normal")
        self.console.insert(tk.END, f"> {text}\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")

    def add_menu_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, width=15, pady=5)
        btn.pack(pady=5)

    def add_chest_row(self, label_text, chest_id, initial_count):
        row = tk.Frame(self.right_menu, bg="#181818")
        row.pack(fill="x", pady=5, padx=10)
        lbl_count = tk.Label(row, text=f"{initial_count}x", width=5, bg="#181818", fg="#00ff99", font=("Consolas", 10, "bold"))
        lbl_count.pack(side="left")
        btn_open = ttk.Button(row, text=f"OPEN {label_text.upper()}", command=lambda: self.onChestOpen(chest_id, "single"))
        btn_open.pack(side="left", expand=True, fill="x", padx=5)
        btn_all = ttk.Button(row, text="ALL", width=5, command=lambda: self.onChestOpen(chest_id, "all"))
        btn_all.pack(side="left")
        return lbl_count

    def add_shop_item(self, parent, item_obj):
        # Reduced pady/padx for a slimmer look
        frame = tk.Frame(parent, bg="#1c1c1c", pady=5, padx=10, 
                        highlightthickness=1, highlightbackground="#333")

        # Left Side: Text Container
        text_container = tk.Frame(frame, bg="#1c1c1c")
        text_container.pack(side="left", fill="both", expand=True)

        # Name and Description
        tk.Label(text_container, text=item_obj.name, font=("Arial", 10, "bold"), 
                bg="#1c1c1c", fg="white").pack(anchor="w")

        # Lowered wraplength since we are in 2 columns
        tk.Label(text_container, text=item_obj.description, font=("Arial", 8), 
                bg="#1c1c1c", fg="#888", justify="left", wraplength=250).pack(anchor="w")
        
        # Right Side: Buy Button
        # ttk.Buttons can be bulky; standard tk.Buttons allow for more size control
        btn = tk.Button(frame, text=f"BUY ({item_obj.price:.2f} $)", 
                        command=lambda: self.handle_purchase(item_obj),
                        bg="#333", fg="white", font=("Arial", 9, "bold"),
                        padx=10, pady=2, relief="flat", activebackground="#444")
        btn.pack(side="right", padx=5)

        return frame, btn

    # ==========================================
    # GAME LOGIC & CALLBACKS
    # ==========================================

    def onUpdate(self):
        casino.newRound()

        self.update_chest_counts()
        self.set_balance(casino.player.money)
        items = {
            "vip": casino.shop.vip,
            "energy": casino.shop.energy,
            "cigs": casino.shop.cigs,
            "vodka": casino.shop.vodka,
            "drugs": casino.shop.drugs,
            "prostitute": casino.shop.prostitute,
            "russian": casino.shop.russian
        }

        
        for key, item_obj in items.items():
            if key in self.shop_buttons:
                self.shop_buttons[key].config(text=f"BUY ({item_obj.price:.2f} $)")

        base_price = casino.basicChest.cost
        quick_amounts = [1, 25, 10000]
        for amt in quick_amounts:
            if amt in self.quick_buy_labels:
                total = base_price * amt
                self.quick_buy_labels[amt].config(text=f"{total:,.2f} $")
        

    def onStart(self):
        self.onUpdate()

    def set_balance(self, amount):
        self.balance_var.set(f"{amount:,.2f} $")

    def onQuickBuy(self, amount):
        """Custom callback for bulk buying chests."""
        # Calculate total cost (assuming basic chest price is in casino.shop.basic_price)
        unit_price = 10.0 # Or use casino.shop.basic_price if it exists
        total_cost = unit_price * amount

        if casino.player.money >= total_cost:
            casino.player.money -= total_cost
            casino.player.basicChests += amount
            self.print_w(f"Bulk Purchase: Bought {amount} Basic Chests for {total_cost:.2f}$")
            self.onUpdate()
        else:
            self.print_w(f"Failed: You need {total_cost:.2f}$ to buy {amount} chests.")

    def update_chest_counts(self):
        self.chest_labels["basic"].config(text=f"{casino.player.basicChests}x")
        self.chest_labels["ultra"].config(text=f"{casino.player.ultraChests}x")
        self.chest_labels["premium"].config(text=f"{casino.player.premiumChests}x")

    def onChestOpen(self, chest_id, mode):
        if mode == "single":
            if chest_id == "basic": 
                self.onOpenBasic()
            elif chest_id == "ultra": 
                pass # onOpenUltra logic
            elif chest_id == "premium": 
                pass # onOpenPremium logic
        self.onUpdate()

    def onOpenBasic(self):
        if self.is_rolling:
            return
        if casino.player.basicChests > 0:
            rs, rr = casino.basicChest.open()
            self.is_rolling = True
            casino.player.basicChests -= 1
            
            def on_finish():
                casino.player.addFunds(rs)
                self.set_balance(casino.player.money)
                self.print_w(f"You won {rr}! Total: {rs}$")
                self.is_rolling = False 

            self.roll_chest(rr, rs, casino.player.openWait, callback=on_finish) # Changed duration to 3s for better feel

    def roll_chest(self, winning_rarity, amount, duration, callback):
        canvas = self.spinner_canvas
        canvas_width = 600
        tile_width = 90
        pointer_x = canvas_width // 2
        RARITY_COLORS = {0: "#505050", 1: "#206a32", 2: "#00ccff", 3: "#fbff07", 4: "#ff0019", 5: "#ff00ff"}

        num_tiles = 45
        strip = [casino.chances.globalChances.rollOne() for _ in range(num_tiles)]
        strip.append(winning_rarity)
        strip.extend([casino.chances.globalChances.rollOne() for _ in range(10)])

        start_time = time.time()
        total_dist = (num_tiles * tile_width) + (tile_width // 2)

        def animate():
            now = time.time()
            elapsed = now - start_time
            progress = elapsed / duration
            if progress > 1: 
                progress = 1

            ease_progress = 1 - pow(1 - progress, 4)
            current_offset = ease_progress * total_dist
            canvas.delete("all")
            canvas.create_rectangle(0, 10, canvas_width, 80, fill="#181818", outline="#333")

            for i, rarity_idx in enumerate(strip):
                x_pos = (i * tile_width) - current_offset + pointer_x - (tile_width // 2)
                if -tile_width < x_pos < canvas_width + tile_width:
                    color = RARITY_COLORS.get(rarity_idx, "#FFFFFF")
                    canvas.create_rectangle(x_pos + 2, 15, x_pos + tile_width - 2, 75, fill=color, outline="#222", tags="tile")

            canvas.create_line(pointer_x, 5, pointer_x, 85, fill="#ff4444", width=4)
            
            if progress < 1:
                self.root.after(10, animate)
            else:
                winner_color = RARITY_COLORS.get(winning_rarity, "#FFFFFF")
                canvas.create_text(pointer_x, 115, text=f"+ {amount:,.2f} $", fill=winner_color, font=("Segoe UI", 22, "bold"))
                if callback: 
                    callback()
                self.print_w(f"Landed on rarity {winning_rarity}! Prize: {amount}$")
                self.root.after(3000, lambda: canvas.delete("all"))

        animate()

gui = None
def runWindow():
    root = tk.Tk()
    app = GameGUI(root)
    app.onStart()
    root.mainloop()

