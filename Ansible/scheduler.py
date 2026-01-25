import json
import time
import random
import subprocess
import multiprocessing 

############
## CONSTS ##
############
ANSIBLE_TIMEOUT = 60  # Timeout di sicurezza per evitare che Ansible blocchi il processo se la rete cade
ACTION_MIN = 180      # Minimo tempo di azione (3 minuti)
ACTION_MAX = 240      # Massimo tempo di azione (4 minuti)

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Impossibile leggere {filepath}: {e}")
        return {}

def create_ansible_inventory(hosts_data, inventory, linux_user, windows_user):
    linux_hosts = []
    windows_hosts = []

    for host in hosts_data:
        ip = host.get('ip')
        os_type = host.get('os', 'linux').lower()
        
        if os_type == 'windows':
            windows_hosts.append(ip)
        else:
            linux_hosts.append(ip)

    try:
        with open(inventory, 'w') as f:
            # Gruppo LINUX
            f.write("[workers_linux]\n")
            for ip in linux_hosts:
                f.write(f"{ip} ansible_user={linux_user} ansible_ssh_common_args='-o StrictHostKeyChecking=no'\n")
            
            # Gruppo WINDOWS
            if windows_hosts:
                f.write("\n[workers_windows]\n")
                for ip in windows_hosts:
                    f.write(f"{ip} ansible_user={windows_user} ansible_ssh_common_args='-o StrictHostKeyChecking=no'\n")
    except Exception as e:
        print(f"[ERROR] Errore scrittura inventario {inventory}: {e}")
            
    return len(windows_hosts) > 0

def run_ansible_command(url, action_type, duration, has_windows, inventory, linux_user, linux_path, windows_bat_path):
    # Aggiungi 'duration' (convertito a int) al comando
    duration_int = int(duration)
    
    cmd_linux_text = (
        f"export DISPLAY=:0 && "
        f"export TMPDIR=/home/{linux_user}/tmp_firefox && "
        # Passiamo duration come TERZO argomento
        f"{linux_path}/venv/bin/python {linux_path}/smart_worker.py {url} {action_type} {duration_int}"
    )
    
    cmd_linux = [
        "ansible", "workers_linux",
        "-i", inventory,
        "-m", "shell",
        "-a", f"nohup sh -c '{cmd_linux_text}' > /dev/null 2>&1 &"
    ]

    # --- COMANDO PER WINDOWS ---
    cmd_win = []
    if has_windows:
        cmd_win = [
            "ansible", "workers_windows",
            "-i", inventory,
            "-m", "raw",
            # Aggiungiamo {duration_int} anche qui. Il BAT si aspetta: URL ACTION DURATION
            "-a", f"{windows_bat_path} {url} {action_type} {duration_int}"
        ]

    # ESECUZIONE CON TIMEOUT
    try:
        subprocess.run(cmd_linux, capture_output=True, text=True, timeout=ANSIBLE_TIMEOUT)
    except subprocess.TimeoutExpired:
        print(f"[WARN {inventory}] Timeout Ansible Linux scaduto!")
    except Exception as e:
        print(f"[ERROR {inventory}] Linux cmd: {e}")

    if has_windows:
        try:
            subprocess.run(cmd_win, capture_output=True, text=True, timeout=ANSIBLE_TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"[WARN {inventory}] Timeout Ansible Windows scaduto!")
        except Exception as e:
            print(f"[ERROR {inventory}] Windows cmd: {e}")
        
    print(f"[OK {inventory}] Comandi inviati -> {url} ({action_type}) per {duration_int}s")

def web_simulation(args, duration):
    vlan, registration, websites, inventory, linux_user, linux_path, windows_user, windows_bat_path = args
    print(f"--- AVVIO SIMULAZIONE WEB: {vlan} ---")
    print(f"--- Tempo netto assegnato: {duration:.1f} secondi ---")
    
    reg_config = load_json(registration)
    web_config = load_json(websites)
    
    # Gestione Hosts
    if 'HOSTS_LIST' in reg_config:
        hosts_data = reg_config['HOSTS_LIST']
    elif 'HOSTS_IP_ADDRESS' in reg_config:
        hosts_data = [{'ip': ip, 'os': 'linux'} for ip in reg_config['HOSTS_IP_ADDRESS']]
    else:
        print(f"[FATAL {vlan}] Nessuna lista host trovata.")
        return

    raw_entries = [site['url'] for site in web_config.get('IT', [])]
    if not raw_entries:
        print(f"[WARN {vlan}] Nessun URL trovato nel file websites.")
        return

    has_windows_hosts = create_ansible_inventory(hosts_data, inventory, linux_user, windows_user)
    
    # --- CALCOLO TEMPO NETTO ---
    start_time = time.time()
    end_time = start_time + duration
    
    try:
        # Loop finché non scade il tempo assegnato
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                break

            full_entry = random.choice(raw_entries)
            parts = full_entry.split()
            target_url = parts[0]
            action_type = parts[1] if len(parts) > 1 else "generic"

            # Calcoliamo la durata di QUESTA singola azione
            sleep_time = min(random.randint(ACTION_MIN, ACTION_MAX), remaining_time)

            run_ansible_command(target_url, action_type, sleep_time, has_windows_hosts, inventory, linux_user, linux_path, windows_bat_path)
            
            print(f"[WAIT {vlan}] Navigazione in corso... (prossima azione tra {sleep_time:.0f}s)")
            time.sleep(sleep_time)

        print(f"[DONE {vlan}] Tempo simulazione WEB scaduto.")
            
    except KeyboardInterrupt:
        print(f"\n[STOP {vlan}] Simulazione interrotta.")
    except Exception as e:
        print(f"[CRITICAL {vlan}] Errore nel loop: {e}")
        

def run_pdf_command(pdf_path, action_type, duration, has_windows, inventory, linux_user, linux_path, windows_bat_path):
    """
    Lancia il comando PDF con TIMEOUT.
    """
    duration_int = int(duration)
    # --- COMANDO PER LINUX ---
    log_file = f"/home/{linux_user}/worker_pdf.log"
    cmd_linux_text = (
        f"export DISPLAY=:0 && "
        # Passiamo duration come SECONDO argomento (come si aspetta pdf_worker)
        f"{linux_path}/venv/bin/python {linux_path}/pdf_worker.py {pdf_path} {duration_int}"
    )
    
    cmd_linux = []
    if pdf_path and not pdf_path.startswith("C:"):
        cmd_linux = [
            "ansible", "workers_linux",
            "-i", inventory,
            "-m", "shell",
            "-a", f"nohup sh -c '{cmd_linux_text}' > {log_file} 2>&1 &"
        ]

    # --- COMANDO PER WINDOWS ---
    cmd_win = []
    if has_windows and pdf_path and pdf_path.startswith("C:"):
        cmd_win = [
            "ansible", "workers_windows",
            "-i", inventory,
            "-m", "raw",
            # Passiamo PATH, ACTION(pdf), DURATION. Il .bat gestirà i token.
            "-a", f"{windows_bat_path} {pdf_path} pdf {duration_int}"
        ]

    if cmd_linux:
        try:
            subprocess.run(cmd_linux, capture_output=True, text=True, timeout=ANSIBLE_TIMEOUT)
            print(f"[OK {inventory}] Linux PDF start: {pdf_path} ({duration_int}s)")
        except subprocess.TimeoutExpired:
            print(f"[WARN {inventory}] Timeout Ansible Linux PDF!")
        except Exception as e:
            print(f"[ERROR {inventory}] Linux PDF cmd: {e}")

    if cmd_win:
        try:
            subprocess.run(cmd_win, capture_output=True, text=True, timeout=ANSIBLE_TIMEOUT)
            print(f"[OK {inventory}] Windows PDF start: {pdf_path} ({duration_int}s)")
        except subprocess.TimeoutExpired:
            print(f"[WARN {inventory}] Timeout Ansible Windows PDF!")
        except Exception as e:
            print(f"[ERROR {inventory}] Windows PDF cmd: {e}")


def pdf_simulation(args, duration):
    vlan, registration, pdf_json_path, inventory, linux_user, linux_path, windows_user, windows_bat_path = args
    print(f"--- AVVIO SIMULAZIONE PDF: {vlan} ---")
    print(f"--- Tempo netto assegnato: {duration:.1f} secondi ---")
    
    reg_config = load_json(registration)
    pdf_config = load_json(pdf_json_path)
    
    if 'HOSTS_LIST' in reg_config:
        hosts_data = reg_config['HOSTS_LIST']
    elif 'HOSTS_IP_ADDRESS' in reg_config:
        hosts_data = [{'ip': ip, 'os': 'linux'} for ip in reg_config['HOSTS_IP_ADDRESS']]
    else:
        print(f"[FATAL {vlan}] Nessuna lista host trovata.")
        return

    pdfs_linux = pdf_config.get('linux', [])
    pdfs_windows = pdf_config.get('windows', [])

    has_windows_hosts = create_ansible_inventory(hosts_data, inventory, linux_user, windows_user)
    
    # --- CALCOLO TEMPO NETTO ---
    start_time = time.time()
    end_time = start_time + duration

    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                break
            
            sleep_time = min(random.randint(ACTION_MIN, ACTION_MAX), remaining_time)

            # 1. LANCIO SU LINUX
            if pdfs_linux:
                target_pdf = random.choice(pdfs_linux)
                # CORREZIONE: Inserito sleep_time come 3° argomento
                run_pdf_command(target_pdf, "pdf", sleep_time, False, inventory, linux_user, linux_path, "")
            
            # 2. LANCIO SU WINDOWS
            if has_windows_hosts and pdfs_windows:
                target_pdf = random.choice(pdfs_windows)
                # CORREZIONE: Inserito sleep_time come 3° argomento
                run_pdf_command(target_pdf, "pdf", sleep_time, True, inventory, "", "", windows_bat_path)

            print(f"[WAIT {vlan}] Lettura PDF in corso... (prossimo cambio tra {sleep_time:.0f}s)")
            time.sleep(sleep_time)

        print(f"[DONE {vlan}] Tempo simulazione PDF scaduto.")
            
    except KeyboardInterrupt:
        print(f"\n[STOP {vlan}] Simulazione PDF interrotta.")
    except Exception as e:
        print(f"[CRITICAL {vlan}] Errore nel loop PDF: {e}")


def run_print_command(pdf_path, has_windows, inventory, windows_bat_path):
    if not has_windows:
        return

    cmd_win = [
        "ansible", "workers_windows",
        "-i", inventory,
        "-m", "raw",
        "-a", f"{windows_bat_path} {pdf_path} print"
    ]

    try:
        subprocess.run(cmd_win, capture_output=True, text=True, timeout=ANSIBLE_TIMEOUT)
        print(f"[OK {inventory}] Stampa inviata: {pdf_path}")
    except subprocess.TimeoutExpired:
        print(f"[WARN {inventory}] Timeout Stampa!")
    except Exception as e:
        print(f"[ERROR {inventory}] Print cmd: {e}")

def print_simulation(args, duration):
    vlan, pdf_json_path, inventory, windows_bat_path = args
    print(f"--- AVVIO SIMULAZIONE STAMPA: {vlan} ---")
    print(f"--- Tempo netto assegnato: {duration:.1f} secondi ---")
    
    pdf_config = load_json(pdf_json_path)
    pdfs_windows = pdf_config.get('windows', [])
    
    if not pdfs_windows:
        print(f"[WARN {vlan}] Nessun PDF Windows trovato per la stampa.")
        return

    has_windows = True
    
    # --- CALCOLO TEMPO NETTO ---
    start_time = time.time()
    end_time = start_time + duration

    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                break
            
            target_pdf = random.choice(pdfs_windows)
            run_print_command(target_pdf, has_windows, inventory, windows_bat_path)
            

            # Le stampe sono rare. Aspettiamo un tempo più lungo.
            sleep_time = min(random.randint(ACTION_MIN, ACTION_MAX), remaining_time)
            print(f"[WAIT {vlan}] Attesa post-stampa... ({sleep_time:.0f}s)")
            time.sleep(sleep_time)
            
        print(f"[DONE {vlan}] Tempo simulazione STAMPA scaduto.")

    except KeyboardInterrupt:
        print(f"\n[STOP {vlan}] Simulazione Stampa interrotta.")
    except Exception as e:
        print(f"[CRITICAL {vlan}] Errore loop Stampa: {e}")

def run_mail_command(has_windows, inventory, windows_bat_path):
    if not has_windows:
        return

    cmd_win = [
        "ansible", "workers_windows",
        "-i", inventory,
        "-m", "raw",
        "-a", f"{windows_bat_path} gmail mail"
    ]

    try:
        subprocess.run(cmd_win, capture_output=True, text=True, timeout=ANSIBLE_TIMEOUT)
        print(f"[OK {inventory}] Mail avviata su Windows")
    except subprocess.TimeoutExpired:
        print(f"[WARN {inventory}] Timeout Mail!")
    except Exception as e:
        print(f"[ERROR {inventory}] Mail cmd: {e}")


def read_mail_simulation(args, duration):
    vlan, inventory, windows_bat_path = args
    print(f"--- AVVIO SIMULAZIONE MAIL: {vlan} ---")
    print(f"--- Tempo netto assegnato: {duration:.1f} secondi ---")
    
    has_windows = True 
    
    # --- CALCOLO TEMPO NETTO ---
    start_time = time.time()
    end_time = start_time + duration

    try:
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                break
            
            run_mail_command(has_windows, inventory, windows_bat_path)
            
            # La mail si legge per molto tempo
            sleep_time = min(remaining_time, duration) # Dorme tutto il tempo rimanente o un blocco unico
            print(f"[WAIT {vlan}] Consultazione mail... ({sleep_time:.0f}s)")
            time.sleep(sleep_time)

        print(f"[DONE {vlan}] Tempo simulazione MAIL scaduto.")
            
    except KeyboardInterrupt:
        print(f"\n[STOP {vlan}] Simulazione Mail interrotta.")
    except Exception as e:
        print(f"[CRITICAL {vlan}] Errore nel loop Mail: {e}")


# --- CONFIGURAZIONI ARGOMENTI ---
args_c1_web = (
        "Classroom1", 
        "configs/registration_10.json", 
        "configs/websites_10.json", 
        "configs/hosts_10", 
        "student", 
        "/home/student/user_behavior_generation/worker", 
        "Student", 
        "C:\\Users\\Student\\user_behavior_generation\\worker\\browser_task.bat"
    )
args_c1_pdf = (
         "Classroom1",
         "configs/registration_10.json",
         "configs/pdf_10.json", 
         "configs/hosts_10", 
         "student",
         "/home/student/user_behavior_generation/worker",
         "Student",
         "C:\\Users\\Student\\user_behavior_generation\\worker\\browser_task.bat"
     )

args_c2_web = (
        "Classroom2", 
        "configs/registration_20.json", 
        "configs/websites_20.json", 
        "configs/hosts_20", 
        "student", 
        "/home/student/user_behavior_generation/worker", 
        "", 
        ""
    )
args_c2_pdf = (
         "Classroom2",
         "configs/registration_20.json",
         "configs/pdf_20.json", 
         "configs/hosts_20", 
         "student",
         "/home/student/user_behavior_generation/worker",
         "",
         ""
     )

args_sec_web = (
        "Secretary", 
        "configs/registration_40.json", 
        "configs/websites_40.json", 
        "configs/hosts_40", 
        "", 
        "", 
        "Secretary", 
        "C:\\Users\\Secretary\\user_behavior_generation\\worker\\browser_task.bat"
    )
     
args_sec_pdf = (
         "Secretary",
         "configs/registration_40.json",
         "configs/pdf_40.json", 
         "configs/hosts_40", 
         "",
         "",
         "Secretary",
         "C:\\Users\\Secretary\\user_behavior_generation\\worker\\browser_task.bat"
     )
args_sec_mail = (
        "Secretary",
        "configs/hosts_40",      
        "C:\\Users\\Secretary\\user_behavior_generation\\worker\\browser_task.bat"
    )
args_sec_print = (
         "Secretary",
         "configs/print_pdf_40.json", 
         "configs/hosts_40", 
         "C:\\Users\\Secretary\\user_behavior_generation\\worker\\browser_task.bat"
     )


def pick_secretary_task():
    roll = random.randint(1, 100)
    if roll <= 80:
        if random.choice([True, False]):
            return web_simulation, args_sec_web
        else:
            return pdf_simulation, args_sec_pdf
    elif roll <= 90:
        return read_mail_simulation, args_sec_mail
    else:
        return print_simulation, args_sec_print


def main():
    print("--- [MAIN 1] AVVIO SCHEDULER OTTIMIZZATO (TIME-BOUNDED) ---", flush=True)
    
    sequence_steps = ["CLASSROOM1", "SECRETARY", "CLASSROOM2", "SECRETARY"]
    step_index = 0 
    active_processes = []

    try:
        while True:
            current_actor = sequence_steps[step_index]
            
            target_func = None
            target_args = None

            if current_actor == "CLASSROOM1":
                task_type = random.choice(["WEB", "PDF"])
                if task_type == "WEB":
                    target_func = web_simulation
                    target_args = args_c1_web
                else:
                    target_func = pdf_simulation
                    target_args = args_c1_pdf

            elif current_actor == "CLASSROOM2":
                task_type = random.choice(["WEB", "PDF"])
                if task_type == "WEB":
                    target_func = web_simulation
                    target_args = args_c2_web 
                else:
                    target_func = pdf_simulation
                    target_args = args_c2_pdf

            elif current_actor == "SECRETARY":
                target_func, target_args = pick_secretary_task()

            # Calcolo Tempi
            duration_minutes = random.uniform(5, 7)
            duration_seconds = duration_minutes * 60
            
            if target_func == read_mail_simulation or target_func == print_simulation:
                duration_seconds = duration_seconds / 2
                print(f"[MASTER] Attività breve ({target_func.__name__}): Tempo dimezzato.", flush=True)

            overlap_time = duration_seconds * 0.8
            
            print(f"\n[MASTER] ------------------------------------------------", flush=True)
            print(f"[MASTER] Step {step_index + 1}/{len(sequence_steps)}: {current_actor}", flush=True)
            print(f"[MASTER] Task: {target_func.__name__}", flush=True)
            print(f"[MASTER] Durata Processo: {duration_seconds:.0f}s. Attesa Main: {overlap_time:.0f}s", flush=True)

            if target_func:
                p = multiprocessing.Process(target=target_func, args=(target_args, duration_seconds))
                p.start()
                active_processes.append(p)
            else:
                print(f"[ERROR] Nessuna funzione assegnata per {current_actor}!", flush=True)

            # Pulizia processi finiti
            active_processes = [proc for proc in active_processes if proc.is_alive()]
            print(f"[MASTER] Processi attivi: {len(active_processes)}", flush=True)

            step_index = (step_index + 1) % len(sequence_steps)
            time.sleep(overlap_time)

    except KeyboardInterrupt:
        print("\n[MASTER] Stop ricevuto. Termino i processi...", flush=True)
        for p in active_processes:
            if p.is_alive():
                p.terminate()
        print("[MASTER] Terminato.", flush=True)

if __name__ == "__main__":
    main()