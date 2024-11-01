import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2

# Conectar a la base de datos PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='budget',
            user='postgres',
            password='12345',
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Recuperar datos de la tabla `budget_table`
def fetch_budget_data():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM budget_table;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    else:
        return []

# Recuperar datos de la tabla `accounting`
def fetch_accounting_data():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM accounting;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    else:
        return []

# Insertar datos en la tabla `budget_table`
def insert_budget_data(category, estimated_budget, achieved_budget):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO budget_table (categories, estimated_budget, achieved_budget) VALUES (%s, %s, %s);"
        cursor.execute(query, (category, estimated_budget, achieved_budget))
        conn.commit()
        conn.close()
        refresh_budget_data()

# Insertar una fila con ceros en la tabla `budget_table`
def insert_zero_budget_data():
    insert_budget_data('Nueva Categoría', 0.0, 0.0)

# Actualizar datos en la tabla `budget_table`
def update_budget_data(id, column, new_value):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = f"UPDATE budget_table SET {column} = %s WHERE id = %s;"
        cursor.execute(query, (new_value, id))
        conn.commit()
        conn.close()
        refresh_budget_data()
        refresh_results_data()

# Eliminar una fila de la tabla `budget_table`
def delete_budget_data():
    selected_item = tree_budget.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna fila")
        return

    item_values = tree_budget.item(selected_item)['values']
    if not item_values:
        return

    id = item_values[0]
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM budget_table WHERE id = %s;"
        cursor.execute(query, (id,))
        conn.commit()
        conn.close()
        refresh_budget_data()
        refresh_results_data()

# Actualizar datos en la tabla `accounting`
def update_accounting_data(id, column, new_value):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = f"UPDATE accounting SET {column} = %s WHERE id = %s;"
        cursor.execute(query, (new_value, id))
        conn.commit()
        conn.close()
        refresh_accounting_data()
        refresh_results_data()

# Refrescar los datos en la tabla `budget_table`
def refresh_budget_data():
    for row in tree_budget.get_children():
        tree_budget.delete(row)
    data = fetch_budget_data()
    for i, row in enumerate(data):
        tree_budget.insert('', tk.END, values=(row[0], *row[1:]))

# Refrescar los datos en la tabla `accounting`
def refresh_accounting_data():
    for row in tree_accounting.get_children():
        tree_accounting.delete(row)
    data = fetch_accounting_data()
    for i, row in enumerate(data):
        tree_accounting.insert('', tk.END, values=(row[0], *row[1:]))

# Refrescar los resultados en la pestaña de resultados
def refresh_results_data():
    estimated_total = sum(float(tree_budget.item(row)['values'][2]) for row in tree_budget.get_children())
    achieved_total = sum(float(tree_budget.item(row)['values'][3]) for row in tree_budget.get_children())
    total_assets = sum(float(tree_accounting.item(row)['values'][3]) for row in tree_accounting.get_children())
    total_expenses = sum(float(tree_accounting.item(row)['values'][2]) for row in tree_accounting.get_children())
    difference = total_assets - total_expenses

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Total Presupuesto Estimado: {estimated_total}\n")
    result_text.insert(tk.END, f"Total Presupuesto Alcanzado: {achieved_total}\n")
    result_text.insert(tk.END, f"Diferencia Activos - Gastos: {difference}\n")

# Guardar resultados en un archivo de texto
def save_results_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(result_text.get(1.0, tk.END))
        messagebox.showinfo("Guardar", "Resultados guardados exitosamente.")

# Manejar la edición de celdas en la tabla `budget_table`
def on_double_click_budget(event):
    item = tree_budget.identify_row(event.y)
    column = tree_budget.identify_column(event.x)
    if not item or not column:
        return

    column_index = int(column.replace('#', '')) - 1
    column_name = tree_budget['columns'][column_index]
    if column_name == 'ID':
        return

    x, y, width, height = tree_budget.bbox(item, column)
    value = tree_budget.set(item, column_name)

    edit_window = tk.Toplevel(root)
    edit_window.geometry(f"{width}x{height}+{tree_budget.winfo_rootx() + x}+{tree_budget.winfo_rooty() + y}")
    edit_window.overrideredirect(True)

    edit_entry = tk.Entry(edit_window)
    edit_entry.insert(0, value)
    edit_entry.focus()
    edit_entry.select_range(0, tk.END)
    edit_entry.pack(fill=tk.BOTH, expand=True)

    def save_edit(event=None):
        new_value = edit_entry.get()
        edit_window.destroy()
        id = tree_budget.item(item)['values'][0]
        update_budget_data(id, column_name, new_value)

    edit_entry.bind("<Return>", save_edit)
    edit_entry.bind("<FocusOut>", save_edit)

# Manejar la edición de celdas en la tabla `accounting`
def on_double_click_accounting(event):
    item = tree_accounting.identify_row(event.y)
    column = tree_accounting.identify_column(event.x)
    if not item or not column:
        return

    column_index = int(column.replace('#', '')) - 1
    column_name = tree_accounting['columns'][column_index]
    if column_name == 'ID':
        return

    x, y, width, height = tree_accounting.bbox(item, column)
    value = tree_accounting.set(item, column_name)

    edit_window = tk.Toplevel(root)
    edit_window.geometry(f"{width}x{height}+{tree_accounting.winfo_rootx() + x}+{tree_accounting.winfo_rooty() + y}")
    edit_window.overrideredirect(True)

    edit_entry = tk.Entry(edit_window)
    edit_entry.insert(0, value)
    edit_entry.focus()
    edit_entry.select_range(0, tk.END)
    edit_entry.pack(fill=tk.BOTH, expand=True)

    def save_edit(event=None):
        new_value = edit_entry.get()
        edit_window.destroy()
        id = tree_accounting.item(item)['values'][0]
        update_accounting_data(id, column_name, new_value)

    edit_entry.bind("<Return>", save_edit)
    edit_entry.bind("<FocusOut>", save_edit)

# Crear interfaz gráfica
def display_data():
    global tree_budget, tree_accounting, result_text, root
    root = tk.Tk()
    root.title("Gestión de Presupuestos y Contabilidad")
    root.geometry('640x380')

    # Crear el menú
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Guardar Resultados", command=save_results_to_file)
    menubar.add_cascade(label="Archivo", menu=file_menu)
    root.config(menu=menubar)

    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill=tk.BOTH)

    tab_control = ttk.Notebook(main_frame)

    # Pestaña de presupuesto
    budget_tab = ttk.Frame(tab_control)
    tab_control.add(budget_tab, text='Presupuestos')

    tree_budget = ttk.Treeview(budget_tab, columns=('ID', 'categories', 'estimated_budget', 'achieved_budget'), show='headings')
    tree_budget.heading('ID', text='ID')
    tree_budget.heading('categories', text='Categoría')
    tree_budget.heading('estimated_budget', text='Presupuesto Estimado')
    tree_budget.heading('achieved_budget', text='Presupuesto Alcanzado')
    tree_budget.pack(expand=True, fill=tk.BOTH)

    button_frame_budget = tk.Frame(budget_tab)
    button_frame_budget.pack(pady=10)

    add_zero_button = tk.Button(button_frame_budget, text="Agregar Fila con Ceros", command=insert_zero_budget_data)
    add_zero_button.pack(side=tk.LEFT, padx=5)

    delete_button = tk.Button(button_frame_budget, text="Eliminar Fila", command=delete_budget_data)
    delete_button.pack(side=tk.LEFT, padx=5)

    # Pestaña de contabilidad
    accounting_tab = ttk.Frame(tab_control)
    tab_control.add(accounting_tab, text='Contabilidad')

    tree_accounting = ttk.Treeview(accounting_tab, columns=('ID', 'income', 'expenses', 'assets', 'liabilities', 'main_account'), show='headings')
    tree_accounting.heading('ID', text='ID')
    tree_accounting.heading('income', text='Ingresos')
    tree_accounting.heading('expenses', text='Gastos')
    tree_accounting.heading('assets', text='Activos')
    tree_accounting.heading('liabilities', text='Pasivos')
    tree_accounting.heading('main_account', text='Cuenta Principal')
    tree_accounting.pack(expand=True, fill=tk.BOTH)

    # Pestaña de resultados
    results_tab = ttk.Frame(tab_control)
    tab_control.add(results_tab, text='Resultados')

    result_text = tk.Text(results_tab, height=10)
    result_text.pack(expand=True, fill=tk.BOTH)

    tab_control.pack(expand=True, fill=tk.BOTH)

    # Asociar doble clic para edición
    tree_budget.bind("<Double-1>", on_double_click_budget)
    tree_accounting.bind("<Double-1>", on_double_click_accounting)

    refresh_budget_data()
    refresh_accounting_data()
    refresh_results_data()
    root.mainloop()

# Ejecutar la aplicación
display_data()