# 🎓 User Behavior Simulation - GNS3 Network Testing

---

## 📂 Ansible Machines

| Zona | Hostname / OS | IP Address | Utente OS | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Classroom 1** | Kali Linux | `10.0.10.52` | `student` | Linux Worker |
| | Windows 10 | `10.0.10.53` | `Student` | Usa `browser_task_student_and_lab.bat` |
| | Lubuntu | `10.0.10.56` | `student` | Linux Worker |
| **Classroom 2** | Ubuntu | `10.0.20.54` | `student` | Linux Worker |
| | Lubuntu | `10.0.20.55` | `student` | Linux Worker |
| **Secretary** | Windows 10 | `10.0.40.51` | `Secretary` | Usa `browser_task_secretary.bat` |
| **Laboratory** | Windows 10 | `10.0.50.51` | `Student` | Usa `browser_task_student_and_lab.bat` |

---

## 🚀 Manual Test Commands

### Classroom 1

#### **CL1-Kali (`10.0.10.52`)**
* **Web (Google):**
  ```bash
  ssh student@10.0.10.52 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/smart_worker.py 'https://www.google.com' generic 60"
  ```
* **PDF:**
  ```bash
  ssh student@10.0.10.52 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/pdf_worker.py /home/student/user_behavior_generation/worker/BDD.pdf 60"
  ```

#### **CL1-Windows (10.0.10.53)**
* **Web (Google):**
  ```bash
  ansible all -i 10.0.10.53, -m raw -a "C:\Users\Student\user_behavior_generation\worker\browser_task_student_and_lab.bat https://www.google.com generic 60" -u Student -e "ansible_shell_type=cmd ansible_connection=ssh"
  ```
* **PDF:**
  ```bash
  ansible all -i 10.0.10.53, -m raw -a "C:\Users\Student\user_behavior_generation\worker\browser_task.bat C:\Users\Student\user_behavior_generation\worker\BDD.pdf pdf 60" -u Student -e "ansible_shell_type=cmd ansible_connection=ssh"
  ```

#### **CL1-Lubuntu (`10.0.10.56`)**
* **Web (Google):**
  ```bash
  ssh student@10.0.10.56 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/smart_worker.py 'https://www.google.com' generic 60"
  ```
* **PDF:**
  ```bash
  ssh student@10.0.10.56 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/pdf_worker.py /home/student/user_behavior_generation/worker/BDD.pdf 60"
  ```

### Classroom 2

#### **CL2-Ubuntu (`10.0.20.54`)**
* **Web:**
  ```bash
  ssh student@10.0.20.54 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/smart_worker.py 'https://www.wikipedia.org' generic 60"
  ```
* **PDF:**
  ```bash
  ssh student@10.0.20.54 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/pdf_worker.py /home/student/user_behavior_generation/worker/expert.pdf 60"
  ```

#### **CL2-Lubuntu (`10.0.20.55`)**
* **Web (Google):**
  ```bash
  ssh student@10.0.20.55 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/smart_worker.py 'https://www.google.com' generic 60"
  ```
* **PDF:**
  ```bash
  ssh student@10.0.20.55 "export TMPDIR=/home/student/tmp_firefox && /home/student/user_behavior_generation/worker/venv/bin/python /home/student/user_behavior_generation/worker/pdf_worker.py /home/student/user_behavior_generation/worker/BDD.pdf 60"
  ```

### Secretary

#### **Sec-PC (`10.0.40.51`)**
* **Web:**
  ```bash
  ansible all -i 10.0.40.51, -m raw -a "C:\Users\User\user_behavior_generation\worker\browser_task.bat 'https://www.unisa.it' generic 60"
  ```
* **PDF:**
  ```bash
  ansible all -i 10.0.40.51, -m raw -a "C:\Users\User\user_behavior_generation\worker\browser_task.bat C:\Users\User\user_behavior_generation\worker\examhall.pdf pdf 60"
  ```
* **Mail:**
  ```bash
  ansible all -i 10.0.40.51, -m raw -a "C:\Users\User\user_behavior_generation\worker\browser_task.bat gmail mail 60"
  ```
* **Print:**
  ```bash
  ansible all -i 10.0.40.51, -m raw -a "C:\Users\User\user_behavior_generation\worker\browser_task.bat C:\Users\User\user_behavior_generation\worker\BDD.pdf print 60"
  ```

### Lab

#### **Sec-PC (`10.0.50.51`)**
* **Web:**
  ```bash
  ansible all -i 10.0.50.51, -m raw -a "C:\Users\LabUser1\user_behavior_generation\worker\browser_task.bat 'https://www.stackoverflow.com' generic 60"
  ```
* **PDF:**
  ```bash
  ansible all -i 10.0.50.51, -m raw -a "C:\Users\LabUser1\user_behavior_generation\worker\browser_task.bat C:\Users\LabUser1\user_behavior_generation\worker\expert.pdf pdf 60"
  ```