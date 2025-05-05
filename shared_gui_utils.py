# ----------------------------------------
# CLEAR ALL WIDGETS FROM CURRENT SCREEN
# ----------------------------------------
def clear_screen(root):
    """
    Removes all widgets from the root window.
    This is used before switching to a new screen
    (e.g., login, register, admin panel) to prevent overlap.
    """
    for widget in root.winfo_children():
        widget.destroy()
