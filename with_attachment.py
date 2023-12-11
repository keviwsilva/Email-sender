import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from colorama import Fore, Style, init
from art import text2art
import os


#Setup port number and server name

smtp_port = 587
smtp_server = "smtp.gmail.com"


print(text2art("EMAIL-SENDER"))
email_from = input("        Digite o seu email (remetente): ")

def read_password_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            password = file.read().strip()
        return password
    except FileNotFoundError:
        print(f"{Fore.RED}Arquivo de senha não encontrado. Por favor, crie um arquivo 'config.txt' com a senha.{Style.RESET_ALL}")
        exit()

def write_password_to_file(file_path, password):
    with open(file_path, 'w') as file:
        file.write(password)

pswd_file_path = "pws.txt"
pswd = read_password_from_file(pswd_file_path)

init()

def read_emails_and_subjects(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        email_list = [line.strip() for line in lines[::2]]  # Every other line is an email address
        subjects = [line.strip() for line in lines[1::2]]   # The remaining lines are subjects
    return email_list, subjects


def append_email_and_subject(file_path, new_email, new_subject):
    with open(file_path, 'a') as file:
        file.write(f"{new_email}\n{new_subject}\n")


def delete_email_and_subject(file_path, email_to_delete):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the index of the email to delete
    try:
        index = lines.index(email_to_delete + '\n')
        print(f"        {Fore.GREEN}Email deletado com sucesso!{Style.RESET_ALL}")
        print()
    except ValueError:
        print(f"{Fore.RED}The email '{email_to_delete}' was not found.{Style.RESET_ALL}")
        return

    # Remove the email and subject
    del lines[index:index+2]

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)


def send_emails(email_list, subjects, file_path):
    try:
        for person, subject in zip(email_list, subjects):
            

            msg = MIMEMultipart()
            msg["From"] = email_from
            msg['To'] = person
            msg['Subject'] = subject

            filename = "CurriculoKevinWillians.pdf"

            attachment = open(file_path, 'rb')

            attachment_package = MIMEBase('aplication', 'octet-stream')
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', 'attachment; filename= '+ filename)
            msg.attach(attachment_package)

            text = msg.as_string()
            print(f"        {Fore.GREEN}Connecting to server...{Style.RESET_ALL}")
            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls()
            TIE_server.login(email_from, pswd)
            print(f"        {Fore.GREEN}Connected to server :-){Style.RESET_ALL}")
            print()

            print(f"        {Fore.YELLOW}Sending email to: {person}{Style.RESET_ALL}")
            TIE_server.sendmail(email_from, person, text)
            print(f"        {Fore.GREEN}Email sent to: {person}...{Style.RESET_ALL}")
            print()

        TIE_server.quit()
    except smtplib.SMTPAuthenticationError:
        print(f"{Fore.RED}Erro de autenticação. Verifique se a senha está correta ou o email remetente esta correto.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Ocorreu um erro ao enviar os e-mails: {e}{Style.RESET_ALL}")


def list_emails_and_subjects(file_path):
    email_list, subjects = read_emails_and_subjects(file_path)

    print(f"        {Fore.CYAN}Emails and Subjects:{Style.RESET_ALL}")
    for i, (email, subject) in enumerate(zip(email_list, subjects), start=1):
        print(f"        {i}. {email}: {subject}")
        print()


def add_new_email_and_subject(file_path):
    new_email = input("     Digite o novo email: ")
    new_subject = input("       Digite o novo assunto: ")
    append_email_and_subject(file_path, new_email, new_subject)
    print(f"        {Fore.GREEN}Email e assunto adicionados com sucesso.{Style.RESET_ALL}")


def delete_email_by_number(file_path):
    email_list, _ = read_emails_and_subjects(file_path)
    list_emails_and_subjects(file_path)

    try:
        number_to_delete = int(input("      Digite o número do email que deseja excluir: "))
        # Convertendo para índice (subtraindo 1 porque a enumeração começa em 1)
        number_to_delete -= 1
        email_to_delete = email_list[number_to_delete]
        delete_email_and_subject(file_path, email_to_delete)
    except ValueError:
        print(f"{Fore.RED}Por favor, digite um número válido.{Style.RESET_ALL}")


def send_all_emails(file_path):
    email_list, subjects = read_emails_and_subjects(file_path)
    file_path = choose_file()
    send_emails(email_list, subjects, file_path)
    print(f"        {Fore.GREEN}Emails enviados.{Style.RESET_ALL}")


def exit_program():
    print(text2art("    Saindo"))
    print(f"        {Fore.YELLOW}Saindo do programa. Até mais!{Style.RESET_ALL}")
    exit()


def set_password():
    new_password = input("    Digite a nova senha: ")
    write_password_to_file(pswd_file_path, new_password)
    print(f"    {Fore.GREEN}Senha atualizada com sucesso.{Style.RESET_ALL}")


def save_file_path_to_config(file_path):
    with open("config.txt", "w") as config_file:
        config_file.write(file_path)

def choose_file():
    # Verifica se há um caminho de arquivo salvo
    if os.path.exists("config.txt"):
        with open("config.txt", "r") as config_file:
            saved_file_path = config_file.read().strip()
            print(f"    Caminho do arquivo salvo: {saved_file_path}")
            choice = input("    Deseja usar este caminho? (S/N): ").upper()
            if choice == "S":
                return saved_file_path

    while True:
        file_path = input("    Digite o caminho do arquivo que deseja enviar: ")
        if os.path.exists(file_path):
            save_file_path_to_config(file_path)
            return file_path
        else:
            print(f"    {Fore.RED}Arquivo não encontrado. Digite um caminho de arquivo válido.{Style.RESET_ALL}")


def main_menu():
    file_path = "emails_and_subjects.txt"
    options = {
        '1': lambda: list_emails_and_subjects(file_path),
        '2': lambda: add_new_email_and_subject(file_path),
        '3': lambda: delete_email_by_number(file_path),
        '4': lambda: send_all_emails(file_path),
        '5': set_password,
        '6': lambda: choose_file(),
        '0': exit_program
    }

    while True:
        print("     Menu:")
        print(f"        1. {Fore.YELLOW}Listar emails e assuntos{Style.RESET_ALL}")
        print(f"        2. {Fore.YELLOW}Adicionar novo email e assunto{Style.RESET_ALL}")
        print(f"        3. {Fore.YELLOW}Excluir email por número{Style.RESET_ALL}")
        print(f"        4. {Fore.YELLOW}Enviar emails{Style.RESET_ALL}")
        print(f"        5. {Fore.YELLOW}Definir/Alterar Senha{Style.RESET_ALL}")
        print(f"        6. {Fore.YELLOW}Escolher arquivo para enviar{Style.RESET_ALL}")
        print(f"        0. {Fore.YELLOW}Sair{Style.RESET_ALL}")


        choice = input("        Escolha uma opção (0-5): ")
        print()
        if choice in options:
            if choice == '0':
                options[choice]()
                break
            elif choice == '6':
                file_path = options[choice]()
            else:
                options[choice]()
        else:
            print(f"        {Fore.RED}Opção inválida. Por favor, escolha uma opção válida.{Style.RESET_ALL}")



if __name__ == "__main__":
    main_menu()


