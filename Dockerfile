# /surin_django_study/Dockerfile
FROM python:3.8  # 생성하는 docker의 python 버전 -> 내 파이썬 버전

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim # docker 안에서 vi 설치 안해도됨

RUN mkdir /surin_django_study # docker안에 docker-server 폴더 생성
ADD . /surin_django_study # 현재 디렉토리를 docker-server 폴더에 복사

WORKDIR /surin_django_study # 작업 디렉토리 설정

RUN pip install --upgrade pip # pip 업글
RUN pip install -r requirements.txt # 필수 패키지 설치

EXPOSE 8000 # 8000번으로 주겠다?? -> 8000번 포트를 열어놓겠다.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "soul_prj.wsgi.develop:application"]
