# main.py
from app.utils import show_option_menu

def main():
    try:
        show_option_menu()

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
