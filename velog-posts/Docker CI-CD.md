# Docker CI/CD
📅 2024-09-23

<h1 id="docker-hub-repository-생성하기">Docker Hub Repository 생성하기</h1>
<p><a href="https://hub.docker.com/">https://hub.docker.com/</a></p>
<h1 id="docker-설치">Docker 설치</h1>
<p>EC2에 연결하여, 아래 명령어로 Docker를 설치해줍니다. </p>
<pre><code>curl -fsSL https://get.docker.com/ | sudo sh
</code></pre><p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/799c3cc6-984d-44f3-95b9-15a5f22d4c85/image.png" /></p>
<h1 id="github-actions-secrets-설정하기">Github Actions Secrets 설정하기</h1>
<p>깃허브 레포지토리의 Settings 탭 &gt; Security &gt; Secrets and variables &gt; Actions 탭 &gt; New repository secrets</p>
<p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/90022e7f-86ae-424b-8321-753d28c20b3c/image.png" /></p>
<ul>
<li>APPLICATION: application.yml 내용</li>
<li>DOCKER_USERNAME: Docker Hub 계정 아이디</li>
<li>DOCKER_PASSWORD: Docker Hub 계정 패스워드</li>
<li>DOCKER_REPO: Docker 리포지토리 </li>
<li>HOST: EC2의 IPv4</li>
<li>KEY: EC2 pem key (*참고: vscode로 pem 파일을 열고 내용 전체를 복붙)</li>
<li>USERNAME: EC2 username (ubuntu)</li>
</ul>
<h1 id="dockerfile-작성하기">Dockerfile 작성하기</h1>
<p>프로젝트 루트 위치(build.gradle있는 곳)에 Dockerfile 이라는 파일을 생성 후, 아래 내용을 입력해줍니다. </p>
<pre><code>FROM openjdk:17-slim // x86_64 (AMD64)용 이미지

ARG JAR_FILE=build/libs/*.jar
COPY ${JAR_FILE} app.jar

ENTRYPOINT [&quot;java&quot;,&quot;-jar&quot;,&quot;-Duser.timezone=Asia/Seoul&quot;,&quot;/app.jar&quot;]
</code></pre><h1 id="deployyml-작성하기">deploy.yml 작성하기</h1>
<p>프로젝트 구조 참고용 사진
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/e50634ca-7fff-418b-9a83-9b6c78ce0fec/image.png" />
위의 구조는 deploy.yml 위치가 이상한데 깃허브 액션이 작동하긴 했습니다.
(아마 AWS EC2 CI/CD 가 되면서 한번에 된듯?)
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/16f4ccc1-5a27-4134-bfe1-601e76534fc1/image.png" />
일반적으로 GitHub Actions에서 사용하는 deploy.yml 파일은 루트 디렉토리에 있는 .github/workflows/ 폴더에 위치합니다. </p>
<p>deploy.yml에 아래의 내용을 작성하고 커밋해주면 됩니다.
(<strong>{프로젝트루트}</strong>, <strong>{브랜치명}</strong> 엔 적절한 값 입력)</p>
<pre><code class="language-YAML">name: CI/CD with Docker


on:
  push:
    branches: [ &quot;{브랜치명}&quot; ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: 17
          distribution: 'zulu'

      - name: Make application.yml
        run: |
          # mkdir ./{프로젝트루트}/src/main/resources # 디렉토리를 무조건 생성
          mkdir -p ./{프로젝트루트}/src/main/resources # 디렉토리가 없으면 생성
          cd ./{프로젝트루트}/src/main/resources
          touch ./application.yml
          echo &quot;${{ secrets.APPLICATION }}&quot; &gt; ./application.yml

      - name: Gradle Caching
        uses: actions/cache@v3
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            ${{ runner.os }}-gradle-

      - name: Build with Gradle
        run: |
          cd ./{프로젝트루트}
          chmod +x ./gradlew
          ./gradlew build -x test

      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Docker build &amp; push
        uses: docker/build-push-action@v2
        with:
          context: ./{프로젝트루트}
          file: ./{프로젝트루트}/Dockerfile
          push: true
          platforms: linux/amd64 # EC2 아키텍쳐에 맞게 (x86 = amd64, arm = arm64)
          tags: ${{ secrets.DOCKER_REPO }}:latest

      - name: Deploy to Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          envs: GITHUB_SHA
          script: |
            sudo docker rm -f $(sudo docker ps -qa)
            sudo docker pull ${{ secrets.DOCKER_REPO }}:latest
            sudo docker run -d -p 8080:8080 ${{ secrets.DOCKER_REPO }}:latest
            sudo docker image prune -f
</code></pre>
<h1 id="docker-관련-에러">Docker 관련 에러</h1>
<h2 id="exec-usrlocalopenjdk-17binjava-exec-format-error">exec /usr/local/openjdk-17/bin/java: exec format error</h2>
<p><code>sudo docker ps</code> 명령어를 입력했을 때 컨테이너가 나오질 않아서, 
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/813ba19f-65c0-440e-9ff7-ee134a79e5e9/image.png" />
<code>sudo docker ps -a</code> 명령어로 이전에 생성된 컨테이너를 확인한 결과, 컨테이너가 종료되어있는 상태였습니다.
<code>sudo docker logs {CONTAINER ID}</code> 로 로그를 살펴보니
exec /usr/local/openjdk-17/bin/java: exec format error 에러가 발생한 걸 확인할 수 있었습니다.
<img alt="" src="https://velog.velcdn.com/images/8w8u8/post/1718e107-a301-4762-ab8e-62cb9384394b/image.png" /></p>
<p>찾아보니, 문제는 이미지를 Ubuntu 서버에 올릴 때 발생한 것 같습니다. 
Ubuntu와 같은 운영체제는 x86_64 아키텍쳐를 사용하므로 도커 이미지를 사용하고자 하는 운영체제에 맞춰 빌드를 진행해야 합니다. </p>
<pre><code>docker buildx build --push --platform linux/amd64 -t {도커 사용자명}/{레포지토리 이름}:latest.</code></pre><p><img alt="" src="https://velog.velcdn.com/images/8w8u8/post/7320c3e0-4606-46d4-9d15-d1c7f9f4d30c/image.png" />
성공적으로 동작하는 걸 이제 볼 수 있습니닷</p>