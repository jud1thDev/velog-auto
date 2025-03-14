import feedparser
import git
import os
from datetime import datetime

# 벨로그 RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@8w8u8'

# 깃허브 레포지토리 경로
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    # 날짜 변환
    published_tuple = entry.published_parsed  # 튜플 형태의 시간 데이터
    published_date = datetime(*published_tuple[:6]).date()  # datetime 객체 변환
    date_str = published_date.strftime("%Y-%m-%d")

    # 파일 이름에서 유효하지 않은 문자 제거 또는 대체
    file_name = entry.title
    file_name = file_name.replace('/', '-')  # 슬래시를 대시로 대체
    file_name = file_name.replace('\\', '-')  # 백슬래시를 대시로 대체

    # 필요에 따라 추가 문자 대체
    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    # 새 글이 있을 때만 파일 생성
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {entry.title}\n")
            file.write(f"📅 {date_str}\n\n")
            file.write(entry.description)  # 글 내용을 파일에 작성
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {date_str}\n{entry.title}')

repo.git.push()
