MrLee Demo
===

서버는 아래와 같이 켤 수 있습니다.

    $ cd /home/mrlee/mrleedemo/
    $ gunicorn server:MrLee -b leeee.kr:80

종료할 때는 이렇게 하세요.

    $ ps -ax | grep gunicorn
    $ kill -9 pid(smallest)