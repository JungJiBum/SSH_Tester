import paramiko
from datetime import datetime
import logging

# 서버 정보를 담고 있는 2차원 리스트
# ls = [[IP, ID, PW, ServerName], [IP, ID, PW, ServerName],
#      [IP, ID, PW, ServerName], [IP, ID, PW, ServerName]]

path = "저장될 폴더 경로"

log_today = datetime.now()
log_today = str(log_today).split(" ")[0]
log = logging.getLogger(path+str(log_today)+".log")
log.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler(path+str(log_today)+".log")
streamHandler = logging.StreamHandler()

log.addHandler(fileHandler)
log.addHandler(streamHandler)


def Extract_Status(ls):
    for i in ls:  # 서버정보를 담은 리스트를 반복
        HOST = i[0]  # i값의 0번째 인덱스(IP)
        ID = i[1]   # i값의 1번째 인덱스(Id)
        PW = i[2]   # i값의 2번째 인덱스(pw)
        NAME = i[3]

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(HOST, username=ID, password=PW)  # 접속 값 설정
            # print(f"접속 IP = {HOST}, NAME = {ID}, password = {PW}")
            print(f"{i[0]} ssh Connected.\n")

            cmds = ['hostname', 'pwd', 'df -h']  # 명령어 리스트
            log.info("날짜 : {} 서버 : {}".format(log_today, NAME))
            for i, cmd in enumerate(cmds):   # 명령어 리스트를 반복하여 수행
                # 표준콘솔입력(stdin), 표준콘솔출력(stdout), 표준에러출력(stderr) 리턴
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                # 표준콘솔출력으로 전달된 stdout로부터 readlines()를 통해 출력 결과를 라인으로 읽어들이고 출력함
                text = ''.join(ssh_stdout.readlines())
                log.info("커맨드 : {} 정보 : \n{}".format(cmd, text))

            ssh.close()  # close()를 통해 연결을 종료한다.
        except Exception as err:
            print(err)  # 접속 실패시 ssh 관련 에러 메시지 출력(Authentication failed.)


# Extract_Status(ls)
