# BrainFood (https://www.ady.today - 현재 서비스 종료)

**Project**: BrainFood  
OpenAI API를 활용한 LLM 기반 챗봇으로, 사용자의 대화 내용을 바탕으로 소설 및 시집을 추천하고 핵심 구절을 제공하는 페이지입니다.


## Development Time
- 2025.05 ~ 2025.06 (현재 유지보수 및 업데이트 진행 중)


## Development Environment
- **Programming Language**: Python 3.10  
- **Framework**: Django, Django REST Framework (DRF)  
- **Database**: PostgreSQL  
- **Authentication**: JWT (회원 관리)  
- **Caching**: Redis (채팅 세션 캐시 저장, Channels 레이어)  
- **Task Queue**: Celery (비동기 작업 처리)  
- **WebSocket**: Django Channels (실시간 메세지 송수신)  
- **Deployment**: AWS EC2, Docker Compose, Nginx, Ubuntu  
- **Version Control**: Git, GitHub  


## Installation

1. **깃허브 클론 및 디렉터리 이동**
   ```bash
   git clone https://github.com/Jingood/BrainFood.git
   cd BrainFood

2. **환경 변수 파일 설정 (.env 생성 후 값 입력)**
3. **makemigrations 진행**
   ```bash
   python manage.py makemigrations

4. **Docker 컨테이너 실행(백그라운드)**
   ```bash
   docker compose up -d --build

5. **서버 실행 확인**
   ```bash
   웹 브라우저에서 아래 주소에 접속하여 서버가 정상적으로 실행되는지 확인
   http://localhost:8000 or http://<EC2 IP>:8000


## API Documentation
https://devjingood.tistory.com/27



## ERD
<img width="841" alt="스크린샷 2025-05-04 오후 11 49 27" src="https://github.com/user-attachments/assets/fe1b54c3-890b-407a-8e1d-53f00c5a6b62" />
